"""
MkDocs LLM AutoDoc Plugin

This plugin automatically generates multi-level documentation for C++ projects using LLMs.
"""

import os
import logging
import threading
import time
from pathlib import Path
from typing import Any, Dict, List
from concurrent.futures import ThreadPoolExecutor, as_completed

from mkdocs.config import config_options
from mkdocs.plugins import BasePlugin
from mkdocs.structure.files import Files
from mkdocs.structure.pages import Page
from mkdocs.config.defaults import MkDocsConfig

try:
    from tqdm import tqdm
    TQDM_AVAILABLE = True
except ImportError:
    TQDM_AVAILABLE = False
    # Fallback: Simple progress indicator
    class tqdm:
        def __init__(self, iterable=None, total=None, desc=None, **kwargs):
            self.iterable = iterable
            self.total = total or (len(iterable) if iterable else 0)
            self.desc = desc
            self.n = 0
            if desc:
                print(f"{desc}: 0/{self.total}")

        def __iter__(self):
            for item in self.iterable:
                yield item
                self.update(1)

        def update(self, n=1):
            self.n += n
            if self.desc and self.n % max(1, self.total // 20) == 0:  # Update every 5%
                print(f"{self.desc}: {self.n}/{self.total}")

        def __enter__(self):
            return self

        def __exit__(self, *args):
            if self.desc:
                print(f"{self.desc}: {self.n}/{self.total} - Complete!")

from .agents.high_level_agent import HighLevelAgent
from .agents.mid_level_agent import MidLevelAgent
from .agents.detailed_level_agent import DetailedLevelAgent
from .agents.overview_agent import HighLevelOverviewAgent
from .parsers.cpp_parser import CppParser
from .utils.cache_manager import CacheManager
from .utils.state_manager import StateManager
from .utils.cross_reference import CrossReferenceManager
from .utils.llm_provider import LLMProviderFactory
from .utils.rag_uploader import RAGUploader

logger = logging.getLogger('mkdocs.plugins.llm-autodoc')


class LLMAutoDocPluginConfig(config_options.Config):
    """Configuration options for the LLM AutoDoc plugin"""

    # Required settings
    enabled = config_options.Type(bool, default=True)
    cpp_project_path = config_options.Type(str, default='.')

    # LLM Configuration
    llm_provider = config_options.Choice(['anthropic', 'openai', 'ollama', 'lmstudio'], default='anthropic')
    llm_api_key = config_options.Type(str, default=None)
    llm_model = config_options.Type(str, default='claude-3-5-sonnet-20241022')
    llm_base_url = config_options.Type(str, default=None)  # For Ollama, LM Studio, or custom endpoints
    llm_timeout = config_options.Type(float, default=600.0)  # Timeout in seconds (default: 10 minutes)

    # Documentation levels to generate
    generate_high_level = config_options.Type(bool, default=True)
    generate_mid_level = config_options.Type(bool, default=True)
    generate_detailed_level = config_options.Type(bool, default=True)
    generate_overview = config_options.Type(bool, default=True)  # NEW: High-level thematic overview

    # Output paths
    high_level_output = config_options.Type(str, default='generated')
    mid_level_output = config_options.Type(str, default='generated/modules')
    detailed_level_output = config_options.Type(str, default='generated/api')
    overview_output = config_options.Type(str, default='generated')  # NEW: Overview documentation

    # Caching
    enable_cache = config_options.Type(bool, default=True)
    cache_dir = config_options.Type(str, default='.cache/llm-autodoc')
    force_regenerate = config_options.Type(bool, default=False)

    # Quality control
    enable_quality_check = config_options.Type(bool, default=True)
    enable_cross_references = config_options.Type(bool, default=True)
    enable_code_review = config_options.Type(bool, default=True)

    # File patterns
    include_patterns = config_options.Type(list, default=['**/*'])  # Default: all files
    exclude_patterns = config_options.Type(list, default=['**/build/**', '**/third_party/**', '**/external/**', '**/.git/**', '**/__pycache__/**', '**/*.pyc', '**/.cache/**', '**/node_modules/**'])

    # Advanced
    max_concurrent_llm_calls = config_options.Type(int, default=3)
    retry_failed = config_options.Type(bool, default=True)
    verbose = config_options.Type(bool, default=False)

    # Background processing
    background_generation = config_options.Type(bool, default=True)
    show_generation_progress = config_options.Type(bool, default=True)

    # RAG Integration
    enable_rag_upload = config_options.Type(bool, default=False)
    rag_webhook_url = config_options.Type(str, default=None)
    rag_upload_source_files = config_options.Type(bool, default=True)  # Upload processed source files during generation
    rag_upload_generated_docs = config_options.Type(bool, default=True)  # Upload generated documentation
    rag_upload_all_source = config_options.Type(bool, default=True)  # Upload ALL files in project (Python, Markdown, C++, etc.)

    # Doxygen Legacy Import
    enable_doxygen_import = config_options.Type(bool, default=False)
    doxygen_xml_dir = config_options.Type(str, default=None)  # Path to Doxygen XML output directory
    doxygen_validate_freshness = config_options.Type(bool, default=True)  # Validate documentation against current code
    doxygen_merge_strategy = config_options.Type(str, default='auto')  # 'auto', 'integrate', 'new_section', 'skip'


class LLMAutoDocPlugin(BasePlugin[LLMAutoDocPluginConfig]):
    """
    MkDocs plugin that generates intelligent multi-level C++ documentation using LLMs
    and optionally uploads all project files to RAG systems.

    This plugin provides three levels of documentation:
    1. High-Level: Project overview, architecture, entry points
    2. Mid-Level: Module documentation with classes and dependencies
    3. Detailed-Level: Complete API documentation with examples

    RAG Integration:
    - Uploads ALL source files (Python, C++, Markdown, etc.) to RAG when enabled
    - Uploads generated documentation files
    - Lets the RAG service decide how to handle each file type
    """

    def __init__(self):
        super().__init__()
        self.cache_manager = None
        self.state_manager = None
        self.cpp_parser = None
        self.cross_ref_manager = None
        self.llm_provider = None
        self.rag_uploader = None
        self.doxygen_importer = None
        self.document_chunker = None
        self.auto_rag_uploader = None
        self.exclusion_checker = None

        self.high_level_agent = None
        self.mid_level_agent = None
        self.detailed_agent = None
        self.overview_agent = None

        self.generated_files = []
        self.generation_thread = None
        self.generation_complete = threading.Event()
        self.files_lock = threading.Lock()

        # RAG upload statistics
        self.rag_upload_stats = {'source_files': 0, 'doc_files': 0, 'failed': 0}

    def on_config(self, config: MkDocsConfig) -> MkDocsConfig:
        """
        Called when the config is loaded. Initialize all components.
        """
        if not self.config.enabled:
            logger.info("LLM AutoDoc plugin is disabled")
            return config

        # Validate configuration
        if not self.config.llm_api_key and self.config.llm_provider not in ['ollama', 'lmstudio']:
            logger.warning(
                "No LLM API key provided. Set llm_api_key in mkdocs.yml or "
                "use environment variable (ANTHROPIC_API_KEY or OPENAI_API_KEY)"
            )
            # Try to get from environment
            if self.config.llm_provider == 'anthropic':
                self.config.llm_api_key = os.getenv('ANTHROPIC_API_KEY')
            elif self.config.llm_provider == 'openai':
                self.config.llm_api_key = os.getenv('OPENAI_API_KEY')

        # Initialize components
        docs_dir = Path(config['docs_dir'])
        cache_dir = Path(self.config.cache_dir)
        cache_dir.mkdir(parents=True, exist_ok=True)

        self.cache_manager = CacheManager(cache_dir, enabled=self.config.enable_cache)
        self.state_manager = StateManager(cache_dir, enabled=self.config.enable_cache)
        self.cpp_parser = CppParser(
            include_patterns=self.config.include_patterns,
            exclude_patterns=self.config.exclude_patterns
        )
        self.cross_ref_manager = CrossReferenceManager()

        # Initialize LLM provider
        try:
            self.llm_provider = LLMProviderFactory.create(
                provider=self.config.llm_provider,
                api_key=self.config.llm_api_key,
                model=self.config.llm_model,
                base_url=self.config.llm_base_url,
                timeout=self.config.llm_timeout
            )
        except Exception as e:
            logger.error(f"Failed to initialize LLM provider: {e}")
            return config

        # Initialize agents
        self.high_level_agent = HighLevelAgent(
            llm_provider=self.llm_provider,
            cache_manager=self.cache_manager
        )
        self.mid_level_agent = MidLevelAgent(
            llm_provider=self.llm_provider,
            cache_manager=self.cache_manager,
            cross_ref_manager=self.cross_ref_manager
        )
        self.detailed_agent = DetailedLevelAgent(
            llm_provider=self.llm_provider,
            cache_manager=self.cache_manager,
            cross_ref_manager=self.cross_ref_manager
        )
        
        # Initialize DevX Agent
        from .agents.devx_agent import DevXAgent
        self.devx_agent = DevXAgent(
            llm_provider=self.llm_provider,
            cache_manager=self.cache_manager
        )

        # Get mkdocs.yml path (plugin has access to config file path)
        mkdocs_yml_path = config.config_file_path if hasattr(config, 'config_file_path') else 'mkdocs.yml'

        self.overview_agent = HighLevelOverviewAgent(
            llm_provider=self.llm_provider,
            cache_manager=self.cache_manager,
            state_manager=self.state_manager,
            mkdocs_yml_path=mkdocs_yml_path,
            docs_dir=config['docs_dir']
        )

        # Initialize RAG uploader
        if self.config.enable_rag_upload:
            self.rag_uploader = RAGUploader(
                webhook_url=self.config.rag_webhook_url,
                enabled=True
            )
            if self.rag_uploader.enabled:
                logger.info(f"✓ RAG upload enabled (webhook: {self.rag_uploader.webhook_url})")
            else:
                logger.warning("✗ RAG upload configured but webhook URL not available")
        else:
            logger.info("RAG upload disabled")

        # Initialize Doxygen importer
        if self.config.enable_doxygen_import:
            if not self.config.doxygen_xml_dir:
                logger.warning("✗ Doxygen import enabled but doxygen_xml_dir not specified")
            else:
                try:
                    from .utils.doxygen_importer import DoxygenImporter
                    # Parse all source files to get content
                    source_files = {}
                    project_path = Path(self.config.cpp_project_path)
                    for file_path in project_path.rglob('*.cpp'):
                        try:
                            source_files[str(file_path)] = file_path.read_text(encoding='utf-8')
                        except:
                            pass
                    for file_path in project_path.rglob('*.h'):
                        try:
                            source_files[str(file_path)] = file_path.read_text(encoding='utf-8')
                        except:
                            pass

                    self.doxygen_importer = DoxygenImporter(
                        doxygen_xml_dir=self.config.doxygen_xml_dir,
                        llm_provider=self.llm_provider,
                        source_files=source_files
                    )
                    if self.doxygen_importer.available:
                        logger.info(f"✓ Doxygen importer initialized (XML dir: {self.config.doxygen_xml_dir})")
                    else:
                        logger.warning("✗ Doxygen XML directory not found")
                except Exception as e:
                    logger.error(f"✗ Failed to initialize Doxygen importer: {e}")
        else:
            logger.info("Doxygen import disabled")

        # Initialize Exclusion Checker
        try:
            from .utils.exclusion_checker import ExclusionChecker
            self.exclusion_checker = ExclusionChecker(self.config.cpp_project_path)
        except Exception as e:
            logger.error(f"✗ Failed to initialize exclusion checker: {e}")

        # Initialize Document Chunker for RAG
        if self.config.enable_rag_upload:
            try:
                from .utils.document_chunker import DocumentChunker
                self.document_chunker = DocumentChunker(
                    max_chunk_size=1000,
                    overlap=100,
                    min_chunk_size=100
                )
                logger.info("✓ Document chunker initialized")
            except Exception as e:
                logger.error(f"✗ Failed to initialize document chunker: {e}")

        logger.info(f"LLM AutoDoc plugin initialized with {self.config.llm_provider}/{self.config.llm_model}")

        return config

    def _upload_to_rag(self, source_file: str = None, doc_files: List[str] = None):
        """
        Helper method to upload files to RAG system.

        Args:
            source_file: Source code file to upload
            doc_files: List of generated documentation files to upload
        """
        if not self.rag_uploader or not self.rag_uploader.enabled:
            return

        # Upload source file
        if source_file and self.config.rag_upload_source_files:
            if self.rag_uploader.upload_source_file(source_file):
                self.rag_upload_stats['source_files'] += 1
            else:
                self.rag_upload_stats['failed'] += 1

        # Upload documentation files
        if doc_files and self.config.rag_upload_generated_docs:
            for doc_file in doc_files:
                if self.rag_uploader.upload_documentation(doc_file, source_file=source_file):
                    self.rag_upload_stats['doc_files'] += 1
                else:
                    self.rag_upload_stats['failed'] += 1

    def _generate_documentation_sync(self, config: MkDocsConfig):
        """
        Internal method that performs the actual documentation generation.
        Can be called synchronously or in a background thread.
        """
        try:
            # Parse C++ project
            project_path = Path(self.config.cpp_project_path)
            if not project_path.exists():
                logger.error(f"C++ project path not found: {project_path}")
                return

            logger.info(f"Parsing C++ project at: {project_path}")
            project_structure = self.cpp_parser.parse_project_structure(str(project_path))

            # Detect changed files
            if self.config.force_regenerate:
                changed_files = project_structure['all_files']
                logger.info("Force regenerate enabled - processing all files")
            else:
                changed_files = self.cache_manager.detect_changed_files(
                    str(project_path),
                    project_structure['all_files']
                )
                logger.info(f"Detected {len(changed_files)} changed files")

            docs_dir = Path(config['docs_dir'])

            # Track successfully processed files for cache update
            successfully_processed_files = []

            # Log generation plan
            total_files_to_process = len(changed_files)
            logger.info("=" * 70)
            logger.info(f"📊 GENERATION PLAN:")
            logger.info(f"   Total files to process: {total_files_to_process}")
            if self.config.generate_overview:
                logger.info(f"   ✓ High-level thematic overview enabled (40+ topics)")
            if self.config.generate_high_level:
                logger.info(f"   ✓ High-level documentation enabled")
            if self.config.generate_mid_level:
                modules_count = len(project_structure.get('modules', []))
                logger.info(f"   ✓ Mid-level documentation enabled ({modules_count} modules)")
            if self.config.generate_detailed_level:
                logger.info(f"   ✓ Detailed API documentation enabled")
            logger.info("=" * 70)

            # Generate High-Level Documentation
            if self.config.generate_high_level:
                output_dir = docs_dir / self.config.high_level_output
                output_dir.mkdir(parents=True, exist_ok=True)

                # Check if high-level docs already exist and project hasn't changed
                existing_high_level_files = list(output_dir.rglob('*.md')) if output_dir.exists() else []
                mid_level_docs_dir = docs_dir / self.config.mid_level_output
                
                high_level_files = self.high_level_agent.generate(
                    project_structure=project_structure,
                    output_dir=str(output_dir),
                    module_docs_dir=str(mid_level_docs_dir)
                )

                logger.info("📤 Uploading high-level documentation to RAG...")
                self._upload_to_rag(doc_files=high_level_files)

            # Generate Mid-Level Documentation
            if self.config.generate_mid_level and project_structure['modules']:
                logger.info("Generating mid-level module documentation...")
                output_dir = docs_dir / self.config.mid_level_output
                output_dir.mkdir(parents=True, exist_ok=True)

                mid_level_files = []
                modules_to_process = [
                    module for module in project_structure['modules']
                    if any(f in changed_files for f in module['files']) or self.config.force_regenerate
                ]

                total_modules = len(modules_to_process)
                logger.info(f"📦 Processing {total_modules} modules...")

                for i, module in enumerate(modules_to_process):
                    module_name = module.get('name', 'unknown')
                    logger.info(f"   Processing module [{i+1}/{total_modules}]: {module_name}")
                    
                    try:
                        detailed_docs_dir = docs_dir / self.config.detailed_level_output
                        files = self.mid_level_agent.generate(
                            module=module,
                            output_dir=str(output_dir),
                            detailed_docs_dir=str(detailed_docs_dir)
                        )
                        mid_level_files.extend(files)

                        if self.rag_uploader and self.rag_uploader.enabled:
                            for source_file in module['files']:
                                self._upload_to_rag(source_file=source_file, doc_files=files)
                        
                        # Incremental cache update for this module
                        self.cache_manager.update_cache(
                            str(project_path),
                            module['files']
                        )
                    except Exception as e:
                        logger.error(f"   ✗ Failed to generate docs for module {module_name}: {e}")

                # Log skipped modules
                skipped = len(project_structure['modules']) - len(modules_to_process)
                if skipped > 0:
                    logger.info(f"⏭️  Skipped {skipped} unchanged modules (using cache)")

                with self.files_lock:
                    self.generated_files.extend(mid_level_files)
                logger.info(f"✅ Generated {len(mid_level_files)} module documentation files")

            # Generate Detailed API Documentation
            if self.config.generate_detailed_level:
                output_dir = docs_dir / self.config.detailed_level_output
                output_dir.mkdir(parents=True, exist_ok=True)

                files_to_document = changed_files if not self.config.force_regenerate else project_structure['all_files']
                detailed_files = []

                total_api_files = len(files_to_document)

                # Skip if no files need to be processed
                if total_api_files == 0 and not self.config.force_regenerate:
                    existing_detailed_files = list(output_dir.rglob('*.md')) if output_dir.exists() else []
                    if existing_detailed_files:
                        logger.info(f"⏭️  Detailed API documentation already exists ({len(existing_detailed_files)} files) and no files changed - skipping generation")
                        with self.files_lock:
                            self.generated_files.extend([str(f) for f in existing_detailed_files])
                else:
                    logger.info("Generating detailed API documentation...")
                    logger.info(f"📄 Processing {total_api_files} API documentation files...")

                    processed_count = 0
                    success_count = 0
                    error_count = 0

                    # Helper function for parallel processing
                    def process_file(file_path):
                        file_info = self.cpp_parser.parse_file(file_path)
                        if file_info and (file_info.get('classes') or file_info.get('functions')):
                            try:
                                files = self.detailed_agent.generate(
                                    file_info=file_info,
                                    project_structure=project_structure,
                                    output_dir=str(output_dir)
                                )
                                # Upload to RAG immediately after generation
                                if self.rag_uploader and self.rag_uploader.enabled:
                                    self._upload_to_rag(source_file=file_path, doc_files=files)
                                return files, None, file_path
                            except Exception as e:
                                if self.config.retry_failed:
                                    try:
                                        files = self.detailed_agent.generate(
                                            file_info=file_info,
                                            project_structure=project_structure,
                                            output_dir=str(output_dir)
                                        )
                                        # Upload to RAG on retry success
                                        if self.rag_uploader and self.rag_uploader.enabled:
                                            self._upload_to_rag(source_file=file_path, doc_files=files)
                                        return files, None, file_path
                                    except Exception as retry_error:
                                        return None, retry_error, file_path
                                return None, e, file_path
                        return None, None, file_path

                    # Use ThreadPoolExecutor for parallel processing with tqdm
                    max_workers = self.config.max_concurrent_llm_calls
                    logger.info(f"🔧 Using {max_workers} parallel workers for API documentation")

                    with ThreadPoolExecutor(max_workers=max_workers) as executor:
                        # Submit all tasks
                        futures = {executor.submit(process_file, fp): fp for fp in files_to_document}

                        # Process completed tasks with tqdm progress bar
                        desc = "📄 Generating API Docs" if self.config.show_generation_progress else None
                        with tqdm(total=len(files_to_document), desc=desc, unit="file", disable=not self.config.show_generation_progress) as pbar:
                            for future in as_completed(futures):
                                file_path = futures[future]
                                try:
                                    files, error, processed_path = future.result()
                                    processed_count += 1

                                    if files:
                                        detailed_files.extend(files)
                                        # Immediately add to generated_files so they can be picked up
                                        with self.files_lock:
                                            self.generated_files.extend(files)
                                        # Mark file as successfully processed for cache update
                                        successfully_processed_files.append(processed_path)
                                        success_count += 1

                                        # Log progress every 10% or every 5 files (whichever is smaller)
                                        log_interval = max(1, min(5, total_api_files // 10))
                                        if processed_count % log_interval == 0 or processed_count == total_api_files:
                                            logger.info(f"📄 Progress: {processed_count}/{total_api_files} files ({success_count} success, {error_count} errors)")
                                        
                                        # Incremental cache update (every 5 files or on completion)
                                        if processed_count % 5 == 0 or processed_count == total_api_files:
                                            # Get files processed since last update
                                            # Note: successfully_processed_files grows, so we need to be careful not to re-update everything if update_cache is slow.
                                            # However, update_cache just updates the hash map and saves to disk. 
                                            # For safety and simplicity, we can just update with the latest batch or all.
                                            # Let's update with the most recent ones to avoid massive list passing if possible, 
                                            # but successfully_processed_files is a simple list.
                                            # To be safe and ensure persistence, we'll just pass the whole list for now 
                                            # as the cache manager handles the dictionary update efficiently.
                                            # A better optimization would be to keep a "pending_cache_update" list.
                                            
                                            self.cache_manager.update_cache(
                                                str(project_path),
                                                successfully_processed_files
                                            )


                                    if error:
                                        error_count += 1
                                        logger.error(f"✗ Failed to generate documentation for {processed_path}: {error}")
                                except Exception as exc:
                                    error_count += 1
                                    logger.error(f"✗ Exception processing {file_path}: {exc}")
                                finally:
                                    pbar.update(1)

                    logger.info(f"✅ Generated {len(detailed_files)} API documentation files ({success_count} success, {error_count} errors)")

            # Update cross-references
            if self.config.enable_cross_references:
                logger.info("Updating cross-references...")
                with self.files_lock:
                    self.cross_ref_manager.update_references(str(docs_dir), self.generated_files.copy())

            # Upload ALL source files to RAG if enabled
            if self.rag_uploader and self.rag_uploader.enabled and self.config.rag_upload_all_source:
                logger.info("=" * 70)
                logger.info("📤 Uploading ALL source files to RAG...")
                all_source_files = self.cpp_parser.find_all_source_files(project_path)
                logger.info(f"   Found {len(all_source_files)} total source files")

                uploaded = 0
                failed = 0
                for source_file in all_source_files:
                    if self.rag_uploader.upload_source_file(source_file):
                        uploaded += 1
                    else:
                        failed += 1

                # Update statistics
                self.rag_upload_stats['source_files'] += uploaded
                self.rag_upload_stats['failed'] += failed
                logger.info(f"✅ Uploaded {uploaded} source files to RAG")
                if failed > 0:
                    logger.info(f"⚠️  Failed to upload {failed} files")
                logger.info("=" * 70)

            # Update cache - ONLY for successfully processed files
            # This prevents failed files from being marked as "processed" in the cache
            unique_processed_files = []
            if successfully_processed_files:
                # Remove duplicates while preserving order
                unique_processed_files = list(dict.fromkeys(successfully_processed_files))
                logger.info(f"💾 Updating cache for {len(unique_processed_files)} successfully processed files")
                self.cache_manager.update_cache(
                    str(project_path),
                    unique_processed_files
                )
            else:
                logger.warning("⚠️  No files were successfully processed - cache not updated")

            # Generate High-Level Thematic Overview (AFTER all other docs!)
            if self.config.generate_overview:
                logger.info("=" * 70)
                logger.info("Generating high-level thematic overview...")
                logger.info("This uses both source code AND the generated documentation above")
                logger.info("=" * 70)

                output_dir = docs_dir / self.config.overview_output
                output_dir.mkdir(parents=True, exist_ok=True)

                # Collect all generated docs to pass to overview agent
                with self.files_lock:
                    all_generated_docs = self.generated_files.copy()

                overview_files = self.overview_agent.generate(
                    project_structure=project_structure,
                    output_dir=str(output_dir),
                    generated_docs=all_generated_docs,
                    max_workers=self.config.max_concurrent_llm_calls,
                    force_regenerate=self.config.force_regenerate
                )
                with self.files_lock:
                    self.generated_files.extend(overview_files)
                logger.info(f"✓ Generated {len(overview_files)} thematic overview documentation files")

                # Upload to RAG
                if self.rag_uploader and self.rag_uploader.enabled:
                    logger.info("📤 Uploading overview documentation to RAG...")
                    self._upload_to_rag(doc_files=overview_files)

            with self.files_lock:
                total_files = len(self.generated_files)

            # Final summary
            logger.info("=" * 70)
            logger.info(f"✅ DOCUMENTATION GENERATION COMPLETE!")
            logger.info(f"   Total documentation files generated: {total_files}")
            logger.info(f"   Successfully processed source files: {len(unique_processed_files)}")
            logger.info(f"   Cache updated: {'Yes' if unique_processed_files else 'No'}")

            # RAG upload summary
            if self.rag_uploader and self.rag_uploader.enabled:
                logger.info(f"")
                logger.info(f"📤 RAG UPLOAD SUMMARY:")
                logger.info(f"   Source files uploaded: {self.rag_upload_stats['source_files']}")
                logger.info(f"   Documentation files uploaded: {self.rag_upload_stats['doc_files']}")
                if self.rag_upload_stats['failed'] > 0:
                    logger.info(f"   Failed uploads: {self.rag_upload_stats['failed']}")
                logger.info(f"   Total uploaded: {self.rag_upload_stats['source_files'] + self.rag_upload_stats['doc_files']}")

            logger.info("=" * 70)

        except Exception as e:
            logger.error(f"Error during documentation generation: {e}", exc_info=True)
        finally:
            self.generation_complete.set()

    def on_pre_build(self, config: MkDocsConfig) -> None:
        """
        Called before the build starts. Start documentation generation here.
        """
        if not self.config.enabled or not self.llm_provider:
            return

        logger.info("Starting LLM-powered documentation generation...")

        # Check if there are already generated files (from a previous run)
        docs_dir = Path(config['docs_dir'])
        existing_files = []
        for output_dir in [self.config.high_level_output, self.config.mid_level_output, self.config.detailed_level_output]:
            gen_dir = docs_dir / output_dir
            if gen_dir.exists():
                existing_files.extend([str(f) for f in gen_dir.rglob('*.md')])

        if existing_files:
            logger.info(f"📚 Found {len(existing_files)} existing documentation files - they will be available immediately")

        # Start generation in background or synchronously
        if self.config.background_generation:
            logger.info("🚀 Starting background documentation generation...")
            logger.info("📝 New documentation will appear automatically as it's generated")
            self.generation_thread = threading.Thread(
                target=self._generate_documentation_sync,
                args=(config,),
                daemon=True,
                name="LLMAutoDocGenerator"
            )
            self.generation_thread.start()
        else:
            logger.info("Starting synchronous documentation generation...")
            self._generate_documentation_sync(config)

    def on_files(self, files: Files, config: MkDocsConfig) -> Files:
        """
        Called after files are collected. Add generated files to the build.
        """
        if not self.config.enabled:
            return files

        # Generated files are already in the docs directory, so they will be
        # picked up automatically by MkDocs
        return files

    def on_post_build(self, config: MkDocsConfig) -> None:
        """
        Called after the build is complete.
        """
        if not self.config.enabled:
            return

        with self.files_lock:
            num_files = len(self.generated_files)

        if self.config.background_generation and self.generation_thread and self.generation_thread.is_alive():
            logger.info(f"📄 Build complete with {num_files} generated files so far")
            logger.info("⏳ Background documentation generation is still running...")
            logger.info("💡 New files will appear automatically in your browser as they're generated")
        else:
            logger.info(f"✅ Build complete with {num_files} generated files")

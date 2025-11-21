"""
State Manager for Multi-Pass Analysis

Tracks progress through multiple analysis phases and enables resumable
documentation generation.
"""

import json
import logging
from pathlib import Path
from typing import Dict, List, Any, Optional, Set
from enum import Enum
from datetime import datetime


logger = logging.getLogger('mkdocs.plugins.llm-autodoc.state')


class AnalysisPhase(Enum):
    """Phases of the high-level overview generation"""
    NOT_STARTED = "not_started"
    TOPIC_EXTRACTION = "topic_extraction"  # Pass 1: Extract info per topic per file
    TOPIC_SYNTHESIS = "topic_synthesis"    # Pass 2: Synthesize topic documents
    TOPIC_REFINEMENT = "topic_refinement"  # Pass 3: Refine and remove duplicates
    DEPENDENCY_ANALYSIS = "dependency_analysis"  # Pass 4: Analyze dependencies
    INDEX_GENERATION = "index_generation"  # Pass 5: Generate master index
    COMPLETED = "completed"


class StateManager:
    """
    Manages state for multi-pass high-level documentation generation.

    Enables resumable documentation generation by tracking:
    - Current analysis phase
    - Files processed per topic
    - Intermediate results
    - Topic completion status
    """

    def __init__(self, cache_dir: Path, enabled: bool = True):
        self.cache_dir = Path(cache_dir)
        self.enabled = enabled

        if self.enabled:
            self.cache_dir.mkdir(parents=True, exist_ok=True)

        self.state_file = self.cache_dir / 'overview_state.json'
        self.state = self._load_state()

    def _load_state(self) -> Dict[str, Any]:
        """Load state from disk"""
        if not self.enabled or not self.state_file.exists():
            return self._create_empty_state()

        try:
            with open(self.state_file, 'r', encoding='utf-8') as f:
                state = json.load(f)
                logger.info(f"Loaded state from {self.state_file}")
                logger.info(f"Current phase: {state.get('current_phase', 'unknown')}")
                return state
        except Exception as e:
            logger.warning(f"Error loading state file: {e}")
            return self._create_empty_state()

    def _create_empty_state(self) -> Dict[str, Any]:
        """Create a new empty state"""
        return {
            'version': '1.0',
            'current_phase': AnalysisPhase.NOT_STARTED.value,
            'started_at': None,
            'updated_at': None,
            'topics': {},  # topic_id -> topic state
            'global_data': {
                'total_files': 0,
                'processed_files': 0,
                'project_hash': None,
            }
        }

    def _save_state(self):
        """Save state to disk"""
        if not self.enabled:
            return

        try:
            self.state['updated_at'] = datetime.now().isoformat()
            with open(self.state_file, 'w', encoding='utf-8') as f:
                json.dump(self.state, f, indent=2)
            logger.debug(f"State saved to {self.state_file}")
        except Exception as e:
            logger.error(f"Error saving state file: {e}")

    def get_current_phase(self) -> AnalysisPhase:
        """Get the current analysis phase"""
        phase_str = self.state.get('current_phase', AnalysisPhase.NOT_STARTED.value)
        return AnalysisPhase(phase_str)

    def set_current_phase(self, phase: AnalysisPhase):
        """Set the current analysis phase"""
        old_phase = self.state.get('current_phase')
        self.state['current_phase'] = phase.value

        if old_phase != phase.value:
            logger.info(f"Phase transition: {old_phase} -> {phase.value}")

        if phase == AnalysisPhase.NOT_STARTED and not self.state['started_at']:
            self.state['started_at'] = datetime.now().isoformat()

        self._save_state()

    def start_analysis(self, total_files: int, project_hash: str):
        """Start a new analysis session"""
        # Check if we need to restart due to project changes
        if self.state['global_data']['project_hash'] != project_hash:
            logger.info("Project structure changed, restarting analysis")
            self.state = self._create_empty_state()

        self.state['global_data']['total_files'] = total_files
        self.state['global_data']['project_hash'] = project_hash
        self.state['started_at'] = datetime.now().isoformat()
        self.set_current_phase(AnalysisPhase.TOPIC_EXTRACTION)

    def init_topic(self, topic_id: str):
        """Initialize state for a topic"""
        if topic_id not in self.state['topics']:
            self.state['topics'][topic_id] = {
                'status': 'pending',  # pending, in_progress, completed
                'processed_files': [],
                'extraction_complete': False,
                'synthesis_complete': False,
                'refinement_complete': False,
                'output_file': None,
                'intermediate_results': {},
                'started_at': None,
                'completed_at': None,
            }
            self._save_state()

    def get_topic_state(self, topic_id: str) -> Dict[str, Any]:
        """Get state for a specific topic"""
        return self.state['topics'].get(topic_id, {})

    def mark_file_processed_for_topic(self, topic_id: str, file_path: str):
        """Mark a file as processed for a specific topic"""
        self.init_topic(topic_id)

        if file_path not in self.state['topics'][topic_id]['processed_files']:
            self.state['topics'][topic_id]['processed_files'].append(file_path)
            self.state['global_data']['processed_files'] = len(
                set(f for topic in self.state['topics'].values()
                    for f in topic['processed_files'])
            )
            self._save_state()

    def is_file_processed_for_topic(self, topic_id: str, file_path: str) -> bool:
        """Check if a file has been processed for a topic"""
        topic_state = self.get_topic_state(topic_id)
        return file_path in topic_state.get('processed_files', [])

    def get_unprocessed_files_for_topic(self, topic_id: str, all_files: List[str]) -> List[str]:
        """Get list of files not yet processed for a topic"""
        topic_state = self.get_topic_state(topic_id)
        processed = set(topic_state.get('processed_files', []))
        return [f for f in all_files if f not in processed]

    def mark_topic_extraction_complete(self, topic_id: str):
        """Mark extraction phase complete for a topic"""
        self.init_topic(topic_id)
        self.state['topics'][topic_id]['extraction_complete'] = True
        logger.info(f"Topic '{topic_id}': extraction complete")
        self._save_state()

    def mark_topic_synthesis_complete(self, topic_id: str, output_file: str):
        """Mark synthesis phase complete for a topic"""
        self.init_topic(topic_id)
        self.state['topics'][topic_id]['synthesis_complete'] = True
        self.state['topics'][topic_id]['output_file'] = output_file
        logger.info(f"Topic '{topic_id}': synthesis complete -> {output_file}")
        self._save_state()

    def mark_topic_refinement_complete(self, topic_id: str):
        """Mark refinement phase complete for a topic"""
        self.init_topic(topic_id)
        self.state['topics'][topic_id]['refinement_complete'] = True
        logger.info(f"Topic '{topic_id}': refinement complete")
        self._save_state()

    def mark_topic_complete(self, topic_id: str):
        """Mark a topic as fully complete"""
        self.init_topic(topic_id)
        self.state['topics'][topic_id]['status'] = 'completed'
        self.state['topics'][topic_id]['completed_at'] = datetime.now().isoformat()
        logger.info(f"Topic '{topic_id}': COMPLETE")
        self._save_state()

    def is_topic_extraction_complete(self, topic_id: str) -> bool:
        """Check if extraction is complete for a topic"""
        topic_state = self.get_topic_state(topic_id)
        return topic_state.get('extraction_complete', False)

    def is_topic_synthesis_complete(self, topic_id: str) -> bool:
        """Check if synthesis is complete for a topic"""
        topic_state = self.get_topic_state(topic_id)
        return topic_state.get('synthesis_complete', False)

    def is_topic_refinement_complete(self, topic_id: str) -> bool:
        """Check if refinement is complete for a topic"""
        topic_state = self.get_topic_state(topic_id)
        return topic_state.get('refinement_complete', False)

    def get_topic_output_file(self, topic_id: str) -> Optional[str]:
        """Get the output file path for a topic"""
        topic_state = self.get_topic_state(topic_id)
        return topic_state.get('output_file')

    def store_intermediate_result(self, topic_id: str, key: str, data: Any):
        """Store intermediate results for a topic"""
        self.init_topic(topic_id)
        self.state['topics'][topic_id]['intermediate_results'][key] = data
        self._save_state()

    def get_intermediate_result(self, topic_id: str, key: str) -> Optional[Any]:
        """Retrieve intermediate results for a topic"""
        topic_state = self.get_topic_state(topic_id)
        return topic_state.get('intermediate_results', {}).get(key)

    def get_all_topics_status(self) -> Dict[str, str]:
        """Get status of all topics"""
        return {
            topic_id: topic_data.get('status', 'pending')
            for topic_id, topic_data in self.state['topics'].items()
        }

    def get_completed_topics(self) -> List[str]:
        """Get list of completed topic IDs"""
        return [
            topic_id for topic_id, topic_data in self.state['topics'].items()
            if topic_data.get('status') == 'completed'
        ]

    def get_pending_topics(self, all_topic_ids: List[str]) -> List[str]:
        """Get list of pending topic IDs"""
        completed = set(self.get_completed_topics())
        return [tid for tid in all_topic_ids if tid not in completed]

    def is_phase_complete(self, phase: AnalysisPhase) -> bool:
        """Check if a specific phase is complete"""
        current = self.get_current_phase()
        phase_order = [
            AnalysisPhase.NOT_STARTED,
            AnalysisPhase.TOPIC_EXTRACTION,
            AnalysisPhase.TOPIC_SYNTHESIS,
            AnalysisPhase.TOPIC_REFINEMENT,
            AnalysisPhase.DEPENDENCY_ANALYSIS,
            AnalysisPhase.INDEX_GENERATION,
            AnalysisPhase.COMPLETED,
        ]

        try:
            current_idx = phase_order.index(current)
            target_idx = phase_order.index(phase)
            return current_idx > target_idx
        except ValueError:
            return False

    def get_progress_summary(self) -> Dict[str, Any]:
        """Get a summary of overall progress"""
        total_topics = len(self.state['topics'])
        completed_topics = len(self.get_completed_topics())

        extraction_complete = sum(
            1 for t in self.state['topics'].values()
            if t.get('extraction_complete', False)
        )
        synthesis_complete = sum(
            1 for t in self.state['topics'].values()
            if t.get('synthesis_complete', False)
        )
        refinement_complete = sum(
            1 for t in self.state['topics'].values()
            if t.get('refinement_complete', False)
        )

        return {
            'current_phase': self.get_current_phase().value,
            'total_topics': total_topics,
            'completed_topics': completed_topics,
            'extraction_complete': extraction_complete,
            'synthesis_complete': synthesis_complete,
            'refinement_complete': refinement_complete,
            'total_files': self.state['global_data']['total_files'],
            'processed_files': self.state['global_data']['processed_files'],
            'started_at': self.state.get('started_at'),
            'updated_at': self.state.get('updated_at'),
        }

    def reset(self):
        """Reset all state"""
        logger.warning("Resetting all state")
        self.state = self._create_empty_state()
        self._save_state()

    def reset_from_phase(self, phase: AnalysisPhase):
        """Reset state from a specific phase onwards"""
        logger.warning(f"Resetting state from phase: {phase.value}")

        if phase == AnalysisPhase.TOPIC_EXTRACTION:
            # Reset everything
            self.reset()
        elif phase == AnalysisPhase.TOPIC_SYNTHESIS:
            # Keep extraction results, reset synthesis onwards
            for topic_data in self.state['topics'].values():
                topic_data['synthesis_complete'] = False
                topic_data['refinement_complete'] = False
                topic_data['output_file'] = None
                if topic_data['status'] != 'pending':
                    topic_data['status'] = 'in_progress'
        elif phase == AnalysisPhase.TOPIC_REFINEMENT:
            # Keep extraction and synthesis, reset refinement
            for topic_data in self.state['topics'].values():
                topic_data['refinement_complete'] = False
                if topic_data['status'] != 'pending':
                    topic_data['status'] = 'in_progress'

        self.set_current_phase(phase)

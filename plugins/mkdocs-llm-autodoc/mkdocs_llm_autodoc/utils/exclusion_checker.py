"""
Exclusion Checker for Documentation

Checks for .exclude_from_docu marker files to exclude directories.
"""

import logging
from pathlib import Path
from typing import Set, List

logger = logging.getLogger('mkdocs.plugins.llm-autodoc.exclusion')


class ExclusionChecker:
    """
    Checks for exclusion markers in directories.
    """

    MARKER_FILE = '.exclude_from_docu'

    def __init__(self, project_root: str):
        """
        Initialize exclusion checker.

        Args:
            project_root: Root directory of the project
        """
        self.project_root = Path(project_root).resolve()
        self.excluded_dirs = self._scan_excluded_directories()

        if self.excluded_dirs:
            logger.info(f"Found {len(self.excluded_dirs)} excluded directories:")
            for excluded in self.excluded_dirs:
                logger.info(f"  - {excluded.relative_to(self.project_root)}")

    def _scan_excluded_directories(self) -> Set[Path]:
        """
        Scan for directories containing .exclude_from_docu marker.

        Returns:
            Set of excluded directory paths
        """
        excluded = set()

        # Search for marker files
        for marker_file in self.project_root.rglob(self.MARKER_FILE):
            # The directory containing the marker
            excluded_dir = marker_file.parent.resolve()
            excluded.add(excluded_dir)

            logger.debug(f"Excluding directory: {excluded_dir}")

        return excluded

    def is_excluded(self, file_path: str) -> bool:
        """
        Check if a file should be excluded based on directory markers.

        Args:
            file_path: Path to file to check

        Returns:
            True if file should be excluded
        """
        file_path_resolved = Path(file_path).resolve()

        # Check if file is in any excluded directory or subdirectory
        for excluded_dir in self.excluded_dirs:
            try:
                # Check if file is relative to excluded directory
                file_path_resolved.relative_to(excluded_dir)
                logger.debug(f"Excluded: {file_path} (in {excluded_dir})")
                return True
            except ValueError:
                # Not in this excluded directory
                continue

        return False

    def filter_files(self, file_paths: List[str]) -> List[str]:
        """
        Filter a list of files, removing excluded ones.

        Args:
            file_paths: List of file paths

        Returns:
            Filtered list of file paths
        """
        filtered = []

        for file_path in file_paths:
            if not self.is_excluded(file_path):
                filtered.append(file_path)
            else:
                logger.debug(f"Filtered out: {file_path}")

        excluded_count = len(file_paths) - len(filtered)
        if excluded_count > 0:
            logger.info(f"Filtered out {excluded_count} files from excluded directories")

        return filtered

    def get_excluded_directories(self) -> List[str]:
        """
        Get list of excluded directory paths.

        Returns:
            List of excluded directory paths (relative to project root)
        """
        return [str(d.relative_to(self.project_root)) for d in self.excluded_dirs]

    def create_exclusion_marker(self, directory: str, reason: str = None):
        """
        Create an exclusion marker file in a directory.

        Args:
            directory: Directory to exclude
            reason: Optional reason for exclusion
        """
        marker_path = Path(directory) / self.MARKER_FILE

        content = "# This directory is excluded from documentation generation\n"
        if reason:
            content += f"# Reason: {reason}\n"
        content += f"# Created by: mkdocs-llm-autodoc\n"

        marker_path.write_text(content, encoding='utf-8')
        logger.info(f"Created exclusion marker: {marker_path}")

        # Rescan excluded directories
        self.excluded_dirs = self._scan_excluded_directories()

    def remove_exclusion_marker(self, directory: str):
        """
        Remove an exclusion marker from a directory.

        Args:
            directory: Directory to include again
        """
        marker_path = Path(directory) / self.MARKER_FILE

        if marker_path.exists():
            marker_path.unlink()
            logger.info(f"Removed exclusion marker: {marker_path}")

            # Rescan excluded directories
            self.excluded_dirs = self._scan_excluded_directories()
        else:
            logger.warning(f"No exclusion marker found in: {directory}")

    def add_custom_exclusion_patterns(self, patterns: List[str]):
        """
        Add custom exclusion patterns (glob patterns).

        Args:
            patterns: List of glob patterns (e.g., '**/test_*.py')
        """
        # This could be extended to support pattern-based exclusions
        # For now, we only support marker files
        pass

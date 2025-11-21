"""
Dependency Analyzer

Analyzes file dependencies, includes, and component relationships
to create comprehensive dependency documentation.
"""

import re
import logging
from pathlib import Path
from typing import Dict, List, Set, Tuple, Any
from collections import defaultdict


logger = logging.getLogger('mkdocs.plugins.llm-autodoc.dependency')


class DependencyAnalyzer:
    """
    Analyzes dependencies between files and components.

    Features:
    - Include/import graph construction
    - Circular dependency detection
    - Component grouping
    - Coupling analysis
    """

    def __init__(self):
        self.include_graph = defaultdict(set)  # file -> set of included files
        self.reverse_graph = defaultdict(set)  # file -> set of files that include it
        self.file_classes = defaultdict(set)  # file -> set of classes defined
        self.file_functions = defaultdict(set)  # file -> set of functions defined
        self.external_dependencies = defaultdict(set)  # file -> external libs

    def analyze_project(self, project_structure: Dict[str, Any], all_files: List[str]) -> Dict[str, Any]:
        """
        Analyze entire project for dependencies.

        Args:
            project_structure: Parsed project structure
            all_files: List of all source files

        Returns:
            Dictionary with dependency analysis results
        """
        logger.info(f"Analyzing dependencies for {len(all_files)} files...")

        # Parse all files
        for file_path in all_files:
            self._analyze_file(file_path)

        # Build analysis results
        results = {
            'include_graph': self._serialize_graph(self.include_graph),
            'reverse_graph': self._serialize_graph(self.reverse_graph),
            'circular_dependencies': self._find_circular_dependencies(),
            'component_groups': self._identify_component_groups(),
            'coupling_metrics': self._calculate_coupling_metrics(),
            'hub_files': self._identify_hub_files(),
            'leaf_files': self._identify_leaf_files(),
            'external_dependencies': self._serialize_graph(self.external_dependencies),
            'dependency_layers': self._identify_dependency_layers(),
        }

        logger.info(f"Dependency analysis complete:")
        logger.info(f"  - Circular dependencies: {len(results['circular_dependencies'])}")
        logger.info(f"  - Component groups: {len(results['component_groups'])}")
        logger.info(f"  - Hub files: {len(results['hub_files'])}")
        logger.info(f"  - Dependency layers: {len(results['dependency_layers'])}")

        return results

    def _analyze_file(self, file_path: str):
        """Analyze a single file for dependencies"""
        try:
            with open(file_path, 'r', encoding='utf-8', errors='ignore') as f:
                content = f.read()

            # Extract includes
            includes = self._extract_includes(content)
            for include in includes:
                if self._is_external_library(include):
                    self.external_dependencies[file_path].add(include)
                else:
                    # Try to resolve to actual file
                    resolved = self._resolve_include(include, file_path)
                    if resolved:
                        self.include_graph[file_path].add(resolved)
                        self.reverse_graph[resolved].add(file_path)

            # Extract class definitions
            classes = self._extract_class_names(content)
            self.file_classes[file_path].update(classes)

            # Extract function definitions
            functions = self._extract_function_names(content)
            self.file_functions[file_path].update(functions)

        except Exception as e:
            logger.warning(f"Error analyzing file {file_path}: {e}")

    def _extract_includes(self, content: str) -> List[str]:
        """Extract #include statements from C++ code"""
        includes = []

        # Match #include "file.h" and #include <file.h>
        pattern = r'^\s*#include\s+[<"]([^>"]+)[>"]'
        for match in re.finditer(pattern, content, re.MULTILINE):
            includes.append(match.group(1))

        return includes

    def _extract_class_names(self, content: str) -> List[str]:
        """Extract class names from C++ code"""
        classes = []

        # Match class/struct definitions
        # Simple pattern - may need refinement
        patterns = [
            r'^\s*class\s+(\w+)',
            r'^\s*struct\s+(\w+)',
        ]

        for pattern in patterns:
            for match in re.finditer(pattern, content, re.MULTILINE):
                classes.append(match.group(1))

        return classes

    def _extract_function_names(self, content: str) -> List[str]:
        """Extract function names from C++ code"""
        functions = []

        # Match function definitions (simplified)
        # This is a basic pattern and may have false positives
        pattern = r'^\s*(?:static\s+)?(?:inline\s+)?[\w:]+\s+(\w+)\s*\([^)]*\)\s*(?:const)?\s*\{'
        for match in re.finditer(pattern, content, re.MULTILINE):
            func_name = match.group(1)
            # Filter out common keywords that might match
            if func_name not in ['if', 'while', 'for', 'switch', 'catch']:
                functions.append(func_name)

        return functions

    def _is_external_library(self, include: str) -> bool:
        """Check if an include is from an external library"""
        # Common external library patterns
        external_patterns = [
            'std', 'boost', 'qt', 'gtest', 'gmock',
            'iostream', 'string', 'vector', 'map',
            'memory', 'algorithm', 'functional',
        ]

        include_lower = include.lower()
        for pattern in external_patterns:
            if pattern in include_lower:
                return True

        # System includes (no extension or common system headers)
        if '/' not in include or include.startswith('sys/'):
            return True

        return False

    def _resolve_include(self, include: str, source_file: str) -> str:
        """Try to resolve an include to an actual file path"""
        # This is simplified - in reality, you'd need to check include paths
        source_dir = Path(source_file).parent

        # Try relative to source file
        possible_path = source_dir / include
        if possible_path.exists():
            return str(possible_path)

        # Try finding the file in the project
        # For now, just use the include as-is
        return include

    def _find_circular_dependencies(self) -> List[List[str]]:
        """Find circular dependencies using DFS"""
        visited = set()
        rec_stack = set()
        cycles = []

        def dfs(node: str, path: List[str]):
            visited.add(node)
            rec_stack.add(node)
            path.append(node)

            for neighbor in self.include_graph.get(node, set()):
                if neighbor not in visited:
                    dfs(neighbor, path.copy())
                elif neighbor in rec_stack:
                    # Found a cycle
                    cycle_start = path.index(neighbor)
                    cycle = path[cycle_start:] + [neighbor]
                    if cycle not in cycles:
                        cycles.append(cycle)

            rec_stack.remove(node)

        for node in self.include_graph.keys():
            if node not in visited:
                dfs(node, [])

        return cycles

    def _identify_component_groups(self) -> List[Dict[str, Any]]:
        """Identify groups of highly coupled files (components)"""
        # Use a simple connected components algorithm
        visited = set()
        components = []

        def dfs(node: str, component: Set[str]):
            visited.add(node)
            component.add(node)

            # Check both directions
            for neighbor in self.include_graph.get(node, set()):
                if neighbor not in visited:
                    dfs(neighbor, component)

            for neighbor in self.reverse_graph.get(node, set()):
                if neighbor not in visited:
                    dfs(neighbor, component)

        for node in set(self.include_graph.keys()) | set(self.reverse_graph.keys()):
            if node not in visited:
                component = set()
                dfs(node, component)
                if len(component) > 1:  # Only include multi-file components
                    components.append({
                        'files': list(component),
                        'size': len(component),
                        'internal_dependencies': self._count_internal_deps(component),
                    })

        # Sort by size (largest first)
        components.sort(key=lambda x: x['size'], reverse=True)
        return components

    def _count_internal_deps(self, component: Set[str]) -> int:
        """Count internal dependencies within a component"""
        count = 0
        for file in component:
            for dep in self.include_graph.get(file, set()):
                if dep in component:
                    count += 1
        return count

    def _calculate_coupling_metrics(self) -> Dict[str, Dict[str, int]]:
        """Calculate coupling metrics for each file"""
        metrics = {}

        for file in set(self.include_graph.keys()) | set(self.reverse_graph.keys()):
            efferent = len(self.include_graph.get(file, set()))  # Outgoing dependencies
            afferent = len(self.reverse_graph.get(file, set()))  # Incoming dependencies

            # Instability metric: I = Ce / (Ce + Ca)
            # 0 = stable, 1 = unstable
            instability = efferent / (efferent + afferent) if (efferent + afferent) > 0 else 0

            metrics[file] = {
                'efferent_coupling': efferent,  # Dependencies on others
                'afferent_coupling': afferent,  # Others depending on this
                'instability': round(instability, 2),
                'total_coupling': efferent + afferent,
            }

        return metrics

    def _identify_hub_files(self, threshold: int = 5) -> List[Dict[str, Any]]:
        """Identify hub files that many other files depend on"""
        hubs = []

        for file, dependents in self.reverse_graph.items():
            if len(dependents) >= threshold:
                hubs.append({
                    'file': file,
                    'dependent_count': len(dependents),
                    'dependents': list(dependents)[:10],  # Limit for readability
                    'classes': list(self.file_classes.get(file, set())),
                    'functions': list(self.file_functions.get(file, set()))[:10],
                })

        # Sort by dependent count
        hubs.sort(key=lambda x: x['dependent_count'], reverse=True)
        return hubs

    def _identify_leaf_files(self) -> List[str]:
        """Identify leaf files that don't depend on anything internal"""
        leaves = []

        for file in set(self.include_graph.keys()) | set(self.reverse_graph.keys()):
            if len(self.include_graph.get(file, set())) == 0:
                leaves.append(file)

        return leaves

    def _identify_dependency_layers(self) -> List[List[str]]:
        """Identify dependency layers using topological sort"""
        # Calculate in-degree for each node
        in_degree = defaultdict(int)
        all_nodes = set(self.include_graph.keys()) | set(self.reverse_graph.keys())

        for node in all_nodes:
            in_degree[node] = len(self.reverse_graph.get(node, set()))

        # Layer 0: nodes with no dependencies
        layers = []
        current_layer = [node for node in all_nodes if in_degree[node] == 0]
        processed = set(current_layer)

        while current_layer:
            layers.append(current_layer)
            next_layer = []

            for node in current_layer:
                for dependent in self.include_graph.get(node, set()):
                    if dependent not in processed:
                        in_degree[dependent] -= 1
                        if in_degree[dependent] == 0:
                            next_layer.append(dependent)
                            processed.add(dependent)

            current_layer = next_layer

        return layers

    def _serialize_graph(self, graph: Dict[str, Set[str]]) -> Dict[str, List[str]]:
        """Convert graph with sets to serializable format"""
        return {k: list(v) for k, v in graph.items()}

    def generate_mermaid_diagram(self, max_nodes: int = 20) -> str:
        """Generate a Mermaid diagram for dependencies"""
        # Get top N most coupled files
        coupling = self._calculate_coupling_metrics()
        top_files = sorted(
            coupling.items(),
            key=lambda x: x[1]['total_coupling'],
            reverse=True
        )[:max_nodes]

        top_file_set = {f[0] for f in top_files}

        lines = ["graph TD"]

        # Add nodes with styling
        for file_path in top_file_set:
            node_id = self._get_node_id(file_path)
            file_name = Path(file_path).name
            lines.append(f"    {node_id}[\"{file_name}\"]")

        # Add edges
        for file_path in top_file_set:
            node_id = self._get_node_id(file_path)
            for dep in self.include_graph.get(file_path, set()):
                if dep in top_file_set:
                    dep_id = self._get_node_id(dep)
                    lines.append(f"    {node_id} --> {dep_id}")

        return "\n".join(lines)

    def _get_node_id(self, file_path: str) -> str:
        """Generate a safe node ID for Mermaid"""
        # Create a safe identifier
        name = Path(file_path).stem
        return re.sub(r'[^a-zA-Z0-9]', '_', name)

    def get_summary_stats(self) -> Dict[str, Any]:
        """Get summary statistics"""
        all_files = set(self.include_graph.keys()) | set(self.reverse_graph.keys())

        total_deps = sum(len(deps) for deps in self.include_graph.values())
        avg_deps = total_deps / len(all_files) if all_files else 0

        return {
            'total_files_analyzed': len(all_files),
            'total_dependencies': total_deps,
            'average_dependencies_per_file': round(avg_deps, 2),
            'circular_dependency_count': len(self._find_circular_dependencies()),
            'hub_file_count': len(self._identify_hub_files()),
            'leaf_file_count': len(self._identify_leaf_files()),
        }

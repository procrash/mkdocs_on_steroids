"""
Topic Definitions for High-Level Overview Documentation

Defines comprehensive topic categories that software developers need
when exploring a new codebase.
"""

from typing import Dict, List
from dataclasses import dataclass


@dataclass
class Topic:
    """Represents a documentation topic"""
    id: str
    name: str
    description: str
    questions: List[str]
    keywords: List[str]
    priority: int  # 1=highest, 5=lowest


class TopicRegistry:
    """
    Central registry of all documentation topics.

    Each topic represents a specific area of interest for developers
    learning a new codebase.
    """

    @staticmethod
    def get_all_topics() -> List[Topic]:
        """Get all defined topics"""
        return [
            # Priority 1: Critical for understanding
            Topic(
                id="project_overview",
                name="Project Overview & Setup",
                description="High-level understanding of what the project does and why it exists",
                questions=[
                    "What is the main purpose of this project?",
                    "What problems does it solve?",
                    "Who are the target users?",
                    "What is the project's vision and goals?",
                    "What is the licensing model?"
                ],
                keywords=["README", "LICENSE", "main", "purpose", "vision", "goals"],
                priority=1
            ),

            Topic(
                id="getting_started",
                name="Getting Started",
                description="How to set up the development environment and start working",
                questions=[
                    "What are the prerequisites for development?",
                    "Which OS/compiler versions are required?",
                    "How do I set up my development environment?",
                    "What is the 'Hello World' for this project?",
                    "How do I verify my setup is correct?"
                ],
                keywords=["setup", "install", "requirements", "prerequisites", "getting started"],
                priority=1
            ),

            Topic(
                id="architecture",
                name="Architecture & Design",
                description="Overall system architecture and design patterns",
                questions=[
                    "What is the high-level architecture?",
                    "Which design patterns are used?",
                    "What architectural decisions were made and why?",
                    "How is the system modularized?",
                    "What is the layer/tier structure?",
                    "Is there a plugin architecture?"
                ],
                keywords=["architecture", "design", "pattern", "layer", "module", "component"],
                priority=1
            ),

            Topic(
                id="code_organization",
                name="Code Organization",
                description="How the code is structured and organized",
                questions=[
                    "What is the directory structure?",
                    "What naming conventions are used?",
                    "How are modules/packages organized?",
                    "Who owns which parts of the code?",
                    "Where can I find specific functionality?"
                ],
                keywords=["directory", "structure", "organization", "namespace", "package"],
                priority=1
            ),

            Topic(
                id="entry_points",
                name="Entry Points & Program Flow",
                description="Where the program starts and how it flows",
                questions=[
                    "Where is the main() function?",
                    "What is the initialization sequence?",
                    "What is the shutdown sequence?",
                    "Is there an event loop?",
                    "How is the application lifecycle managed?"
                ],
                keywords=["main", "entry", "start", "init", "shutdown", "lifecycle"],
                priority=1
            ),

            # Priority 2: Important for daily work
            Topic(
                id="build_system",
                name="Build System & Compilation",
                description="How to build and compile the project",
                questions=[
                    "What build system is used (CMake, Make, Bazel)?",
                    "What build configurations exist (Debug, Release)?",
                    "What compiler flags are used?",
                    "What preprocessor definitions are important?",
                    "How do I do cross-compilation?",
                    "What build optimizations are applied?"
                ],
                keywords=["cmake", "make", "build", "compile", "compiler", "flags"],
                priority=2
            ),

            Topic(
                id="dependencies",
                name="Dependencies & Third-Party Libraries",
                description="External dependencies and how they're managed",
                questions=[
                    "What external libraries are used?",
                    "How are dependencies managed?",
                    "How are versions pinned?",
                    "Are there license compatibility issues?",
                    "How are vendor dependencies handled?"
                ],
                keywords=["dependency", "library", "external", "vendor", "third-party", "submodule"],
                priority=2
            ),

            Topic(
                id="data_structures",
                name="Data Structures & Models",
                description="Core data structures and domain models",
                questions=[
                    "What are the central data structures?",
                    "What are the domain models?",
                    "What are the DTOs (Data Transfer Objects)?",
                    "How is serialization/deserialization handled?",
                    "What data formats are used?"
                ],
                keywords=["struct", "class", "data", "model", "dto", "serialize"],
                priority=2
            ),

            Topic(
                id="data_flow",
                name="Data Flow & Processing",
                description="How data flows through the system",
                questions=[
                    "How does data flow through the system?",
                    "Are there data pipelines?",
                    "What transformations occur?",
                    "How is input/output handled?",
                    "Where are the data processing stages?"
                ],
                keywords=["pipeline", "flow", "process", "transform", "input", "output"],
                priority=2
            ),

            Topic(
                id="apis",
                name="APIs & Interfaces",
                description="Public and internal APIs",
                questions=[
                    "What public APIs are exposed?",
                    "What are the internal APIs?",
                    "What are the interface contracts?",
                    "What is the versioning strategy?",
                    "How is backwards compatibility maintained?"
                ],
                keywords=["api", "interface", "public", "export", "contract"],
                priority=2
            ),

            Topic(
                id="error_handling",
                name="Error Handling & Recovery",
                description="How errors are handled and recovered from",
                questions=[
                    "What is the error handling strategy?",
                    "What is the exception hierarchy?",
                    "What error codes are used?",
                    "What recovery mechanisms exist?",
                    "How is graceful degradation handled?"
                ],
                keywords=["error", "exception", "throw", "catch", "recovery", "failure"],
                priority=2
            ),

            Topic(
                id="logging",
                name="Logging & Debugging",
                description="Logging infrastructure and debugging tools",
                questions=[
                    "What logging framework is used?",
                    "What log levels exist?",
                    "What debug tools are available?",
                    "How do I enable trace/profiling?",
                    "How are core dumps analyzed?"
                ],
                keywords=["log", "debug", "trace", "profile", "dump"],
                priority=2
            ),

            Topic(
                id="configuration",
                name="Configuration & Settings",
                description="How the system is configured",
                questions=[
                    "What configuration mechanisms exist?",
                    "What config file formats are used?",
                    "How are environment variables used?",
                    "What command-line arguments are available?",
                    "Can configuration be changed at runtime?"
                ],
                keywords=["config", "settings", "environment", "options", "parameters"],
                priority=2
            ),

            Topic(
                id="threading",
                name="Threading & Concurrency",
                description="Multithreading and concurrency mechanisms",
                questions=[
                    "What is the threading model?",
                    "What synchronization primitives are used?",
                    "Are there thread pools?",
                    "Are lock-free data structures used?",
                    "How are race conditions prevented?",
                    "How are deadlocks avoided?"
                ],
                keywords=["thread", "mutex", "lock", "concurrent", "parallel", "sync"],
                priority=2
            ),

            Topic(
                id="memory_management",
                name="Memory Management",
                description="Memory allocation and management strategies",
                questions=[
                    "What memory allocation strategies are used?",
                    "How are smart pointers used?",
                    "Are there memory pools?",
                    "How is RAII applied?",
                    "How are memory leaks prevented?",
                    "Are custom allocators used?"
                ],
                keywords=["memory", "allocation", "pointer", "new", "delete", "raii"],
                priority=2
            ),

            # Priority 3: Important for optimization and quality
            Topic(
                id="performance",
                name="Performance & Optimization",
                description="Performance-critical areas and optimizations",
                questions=[
                    "What are the performance-critical areas?",
                    "What are known bottlenecks?",
                    "What caching strategies are used?",
                    "Is lazy loading implemented?",
                    "What profiling results exist?",
                    "What optimization techniques are applied?"
                ],
                keywords=["performance", "optimization", "cache", "fast", "bottleneck", "profile"],
                priority=3
            ),

            Topic(
                id="security",
                name="Security & Safety",
                description="Security practices and safety measures",
                questions=[
                    "What security best practices are followed?",
                    "How is input validated?",
                    "How are buffer overflows prevented?",
                    "What secure coding standards are used?",
                    "How are vulnerabilities managed?",
                    "Have security audits been performed?"
                ],
                keywords=["security", "validate", "sanitize", "safe", "vulnerability", "audit"],
                priority=3
            ),

            Topic(
                id="testing",
                name="Testing Strategy",
                description="Testing infrastructure and practices",
                questions=[
                    "What test framework is used?",
                    "Where are the unit tests?",
                    "Where are the integration tests?",
                    "Are there end-to-end tests?",
                    "What is the test coverage?",
                    "How is mocking/stubbing done?",
                    "How is test data managed?"
                ],
                keywords=["test", "unittest", "mock", "coverage", "assert"],
                priority=3
            ),

            Topic(
                id="ci_cd",
                name="CI/CD Pipeline",
                description="Continuous Integration and Deployment",
                questions=[
                    "What CI tools are used (Jenkins, GitHub Actions, GitLab CI)?",
                    "What is the build pipeline?",
                    "How is test automation set up?",
                    "What code quality checks run in CI?",
                    "What static analysis tools are used?",
                    "What is the deployment pipeline?",
                    "What is the release process?",
                    "How are artifacts managed?"
                ],
                keywords=["ci", "cd", "pipeline", "jenkins", "github actions", "gitlab", "deploy"],
                priority=3
            ),

            Topic(
                id="code_quality",
                name="Code Quality & Standards",
                description="Coding standards and quality measures",
                questions=[
                    "What coding standards are followed?",
                    "What linting tools are used?",
                    "What code formatter is used?",
                    "Are there pre-commit hooks?",
                    "What is the code review process?",
                    "How is technical debt tracked?"
                ],
                keywords=["lint", "format", "standard", "style", "quality", "review"],
                priority=3
            ),

            Topic(
                id="documentation",
                name="Documentation",
                description="Documentation strategy and tools",
                questions=[
                    "What is the documentation strategy?",
                    "How is API documentation generated?",
                    "Are there Architecture Decision Records?",
                    "What inline comment standards exist?",
                    "How is the README structured?",
                    "Is there a wiki or knowledge base?"
                ],
                keywords=["documentation", "doxygen", "comment", "readme", "wiki", "adr"],
                priority=3
            ),

            Topic(
                id="version_control",
                name="Version Control & Branching",
                description="Git workflow and branching strategy",
                questions=[
                    "What Git workflow is used?",
                    "What branching strategy (GitFlow, Trunk-Based)?",
                    "What commit message conventions exist?",
                    "What is the PR/MR process?",
                    "What is the tagging strategy?"
                ],
                keywords=["git", "branch", "commit", "merge", "pull request"],
                priority=3
            ),

            # Priority 4: Operational and deployment
            Topic(
                id="deployment",
                name="Deployment & Distribution",
                description="How the software is deployed and distributed",
                questions=[
                    "What are the deployment targets?",
                    "What packaging formats are used (DEB, RPM, Docker)?",
                    "What is the installation process?",
                    "How do updates work?",
                    "What is the rollback strategy?"
                ],
                keywords=["deploy", "package", "install", "docker", "distribution"],
                priority=4
            ),

            Topic(
                id="monitoring",
                name="Monitoring & Observability",
                description="Monitoring and observability infrastructure",
                questions=[
                    "What monitoring tools are used?",
                    "What metrics are collected?",
                    "How are health checks implemented?",
                    "What alerting exists?",
                    "Is there APM (Application Performance Monitoring)?"
                ],
                keywords=["monitoring", "metrics", "health", "alert", "observability"],
                priority=4
            ),

            Topic(
                id="networking",
                name="Networking & Communication",
                description="Network protocols and communication",
                questions=[
                    "What network protocols are used?",
                    "Are there REST/gRPC/WebSocket APIs?",
                    "How does client-server communication work?",
                    "Are message queues used?",
                    "How does service discovery work?"
                ],
                keywords=["network", "protocol", "rest", "grpc", "socket", "http"],
                priority=4
            ),

            Topic(
                id="database",
                name="Database & Persistence",
                description="Data persistence and database access",
                questions=[
                    "What is the database schema?",
                    "Is an ORM used?",
                    "What is the migration strategy?",
                    "How are backups handled?",
                    "Is there a caching layer?"
                ],
                keywords=["database", "sql", "orm", "persistence", "schema", "migration"],
                priority=4
            ),

            Topic(
                id="file_io",
                name="File I/O & Storage",
                description="File operations and storage handling",
                questions=[
                    "What file formats are supported?",
                    "How are file system operations handled?",
                    "Is streaming supported?",
                    "How are temporary files managed?"
                ],
                keywords=["file", "io", "stream", "storage", "filesystem"],
                priority=4
            ),

            Topic(
                id="platform_specific",
                name="Platform-Specific Code",
                description="Platform-specific implementations",
                questions=[
                    "What platform abstractions exist?",
                    "Where is OS-specific code?",
                    "How is cross-platform compatibility ensured?",
                    "How is platform detection done?"
                ],
                keywords=["platform", "os", "windows", "linux", "macos", "cross-platform"],
                priority=4
            ),

            # Priority 5: Nice to have
            Topic(
                id="i18n",
                name="Internationalization & Localization",
                description="i18n/l10n support",
                questions=[
                    "Is i18n/l10n supported?",
                    "How are strings externalized?",
                    "How are locales handled?",
                    "What character encoding is used?"
                ],
                keywords=["i18n", "l10n", "locale", "translation", "encoding"],
                priority=5
            ),

            Topic(
                id="resource_management",
                name="Resource Management",
                description="Loading and managing resources",
                questions=[
                    "How are resources loaded?",
                    "How are assets managed?",
                    "How is resource cleanup done?",
                    "Is reference counting used?"
                ],
                keywords=["resource", "asset", "cleanup", "reference"],
                priority=5
            ),

            Topic(
                id="plugin_system",
                name="Plugin/Extension System",
                description="Plugin architecture if applicable",
                questions=[
                    "Is there a plugin architecture?",
                    "How is dynamic loading done?",
                    "What are the plugin APIs?",
                    "What extension points exist?"
                ],
                keywords=["plugin", "extension", "dynamic", "load"],
                priority=5
            ),

            Topic(
                id="tooling",
                name="Tooling & Scripts",
                description="Development tools and scripts",
                questions=[
                    "What build scripts exist?",
                    "What utility scripts are available?",
                    "Are there code generation tools?",
                    "What development tools are recommended?"
                ],
                keywords=["script", "tool", "utility", "automation"],
                priority=5
            ),

            Topic(
                id="patterns",
                name="Common Patterns & Idioms",
                description="Code patterns used in the project",
                questions=[
                    "What code patterns are commonly used?",
                    "What are the best practices in this project?",
                    "What anti-patterns should be avoided?"
                ],
                keywords=["pattern", "idiom", "practice", "convention"],
                priority=5
            ),

            Topic(
                id="migration",
                name="Migration & Upgrade Guides",
                description="Version migration information",
                questions=[
                    "What migration paths exist between versions?",
                    "What breaking changes occurred?",
                    "What is the deprecation strategy?",
                    "What are the upgrade procedures?"
                ],
                keywords=["migration", "upgrade", "breaking", "deprecation"],
                priority=5
            ),

            Topic(
                id="troubleshooting",
                name="Troubleshooting & FAQ",
                description="Common issues and solutions",
                questions=[
                    "What are common issues?",
                    "What debug checklists exist?",
                    "What are known limitations?",
                    "What workarounds are available?"
                ],
                keywords=["troubleshoot", "faq", "issue", "problem", "workaround"],
                priority=5
            ),

            Topic(
                id="contributing",
                name="Contributing Guidelines",
                description="How to contribute to the project",
                questions=[
                    "How can I contribute?",
                    "What is the development workflow?",
                    "What are the PR guidelines?",
                    "Is there a code of conduct?"
                ],
                keywords=["contribute", "contributing", "guideline", "workflow"],
                priority=5
            ),

            Topic(
                id="team",
                name="Team & Ownership",
                description="Team structure and code ownership",
                questions=[
                    "Who are the code owners?",
                    "What are the contact points?",
                    "What are the expertise areas?",
                    "Who is on-call/support?"
                ],
                keywords=["team", "owner", "contact", "maintainer"],
                priority=5
            ),

            Topic(
                id="dependencies_graph",
                name="Dependencies Between Components",
                description="Component interactions and dependencies",
                questions=[
                    "How do components interact?",
                    "What are the include/import graphs?",
                    "What is the coupling analysis?",
                    "What module dependencies exist?"
                ],
                keywords=["dependency", "coupling", "include", "import", "interaction"],
                priority=2
            ),

            Topic(
                id="history",
                name="Historical Context",
                description="Project evolution and history",
                questions=[
                    "How has the project evolved?",
                    "What major refactorings occurred?",
                    "What technical decisions were made historically?",
                    "What lessons were learned?"
                ],
                keywords=["history", "evolution", "refactoring", "decision"],
                priority=5
            ),

            Topic(
                id="roadmap",
                name="Future Roadmap",
                description="Future plans and roadmap",
                questions=[
                    "What features are planned?",
                    "What technical debt exists?",
                    "What refactorings are planned?",
                    "What is the deprecation timeline?"
                ],
                keywords=["roadmap", "future", "planned", "todo"],
                priority=5
            ),
        ]

    @staticmethod
    def get_topics_by_priority(priority: int) -> List[Topic]:
        """Get all topics with a specific priority"""
        return [t for t in TopicRegistry.get_all_topics() if t.priority == priority]

    @staticmethod
    def get_topic_by_id(topic_id: str) -> Topic:
        """Get a specific topic by ID"""
        for topic in TopicRegistry.get_all_topics():
            if topic.id == topic_id:
                return topic
        raise ValueError(f"Topic with id '{topic_id}' not found")

    @staticmethod
    def get_topic_ids() -> List[str]:
        """Get list of all topic IDs"""
        return [t.id for t in TopicRegistry.get_all_topics()]

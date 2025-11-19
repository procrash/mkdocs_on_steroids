"""
Test exclusion pattern matching in CppParser
"""
import unittest
from pathlib import Path
import tempfile
import shutil
from mkdocs_llm_autodoc.parsers.cpp_parser import CppParser


class TestExclusionPatterns(unittest.TestCase):
    """Test the exclusion pattern matching functionality"""

    def setUp(self):
        """Create a temporary project structure for testing"""
        self.test_dir = tempfile.mkdtemp()
        self.project_path = Path(self.test_dir)

        # Create test directory structure
        dirs = [
            'src',
            'build',
            'build/Debug',
            'third_party/lib',
            'external/vendor',
            '.git/objects',
            '__pycache__',
            '.cache',
            'node_modules/package',
            'src/module1',
            'src/module2',
        ]

        for dir_path in dirs:
            (self.project_path / dir_path).mkdir(parents=True, exist_ok=True)

        # Create test files
        test_files = {
            'src/main.cpp': '// main file',
            'src/module1/class1.h': '// header',
            'src/module1/class1.cpp': '// impl',
            'src/module2/class2.h': '// header',
            'build/main.o': '// object file',
            'build/Debug/app.exe': '// executable',
            'third_party/lib/helper.cpp': '// third party',
            'external/vendor/lib.h': '// external',
            '.git/config': '# git config',
            '__pycache__/module.pyc': '# python cache',
            '.cache/data.json': '{}',
            'node_modules/package/index.js': '// js',
            'README.md': '# Readme',
        }

        for file_path, content in test_files.items():
            full_path = self.project_path / file_path
            with open(full_path, 'w') as f:
                f.write(content)

    def tearDown(self):
        """Clean up temporary directory"""
        shutil.rmtree(self.test_dir)

    def test_exclude_build_directory(self):
        """Test that **/build/** excludes build directories recursively"""
        parser = CppParser(
            include_patterns=['**/*'],
            exclude_patterns=['**/build/**']
        )

        # These should be excluded
        self.assertTrue(parser._is_excluded(
            self.project_path / 'build/main.o',
            self.project_path
        ))
        self.assertTrue(parser._is_excluded(
            self.project_path / 'build/Debug/app.exe',
            self.project_path
        ))

        # These should NOT be excluded
        self.assertFalse(parser._is_excluded(
            self.project_path / 'src/main.cpp',
            self.project_path
        ))

    def test_exclude_third_party(self):
        """Test that **/third_party/** excludes third_party directories"""
        parser = CppParser(
            include_patterns=['**/*'],
            exclude_patterns=['**/third_party/**']
        )

        # Should be excluded
        self.assertTrue(parser._is_excluded(
            self.project_path / 'third_party/lib/helper.cpp',
            self.project_path
        ))

        # Should NOT be excluded
        self.assertFalse(parser._is_excluded(
            self.project_path / 'src/main.cpp',
            self.project_path
        ))

    def test_exclude_git_directory(self):
        """Test that **/.git/** excludes .git directories"""
        parser = CppParser(
            include_patterns=['**/*'],
            exclude_patterns=['**/.git/**']
        )

        # Should be excluded
        self.assertTrue(parser._is_excluded(
            self.project_path / '.git/config',
            self.project_path
        ))

        # Should NOT be excluded
        self.assertFalse(parser._is_excluded(
            self.project_path / 'src/main.cpp',
            self.project_path
        ))

    def test_exclude_pyc_files(self):
        """Test that **/*.pyc excludes Python cache files recursively"""
        parser = CppParser(
            include_patterns=['**/*'],
            exclude_patterns=['**/*.pyc']
        )

        # Should be excluded
        self.assertTrue(parser._is_excluded(
            self.project_path / '__pycache__/module.pyc',
            self.project_path
        ))

        # Should NOT be excluded
        self.assertFalse(parser._is_excluded(
            self.project_path / 'src/main.cpp',
            self.project_path
        ))

    def test_multiple_exclusions(self):
        """Test that multiple exclusion patterns work together"""
        parser = CppParser(
            include_patterns=['**/*'],
            exclude_patterns=[
                '**/build/**',
                '**/third_party/**',
                '**/external/**',
                '**/.git/**',
                '**/__pycache__/**',
                '**/*.pyc',
                '**/.cache/**',
                '**/node_modules/**'
            ]
        )

        # All these should be excluded
        excluded_files = [
            'build/main.o',
            'build/Debug/app.exe',
            'third_party/lib/helper.cpp',
            'external/vendor/lib.h',
            '.git/config',
            '__pycache__/module.pyc',
            '.cache/data.json',
            'node_modules/package/index.js',
        ]

        for file_path in excluded_files:
            self.assertTrue(
                parser._is_excluded(
                    self.project_path / file_path,
                    self.project_path
                ),
                f"Expected {file_path} to be excluded"
            )

        # These should NOT be excluded
        included_files = [
            'src/main.cpp',
            'src/module1/class1.h',
            'src/module1/class1.cpp',
            'src/module2/class2.h',
            'README.md',
        ]

        for file_path in included_files:
            self.assertFalse(
                parser._is_excluded(
                    self.project_path / file_path,
                    self.project_path
                ),
                f"Expected {file_path} to NOT be excluded"
            )

    def test_find_all_source_files_with_exclusions(self):
        """Test that find_all_source_files respects exclusion patterns"""
        parser = CppParser(
            include_patterns=['**/*'],
            exclude_patterns=[
                '**/build/**',
                '**/third_party/**',
                '**/external/**',
                '**/.git/**',
                '**/__pycache__/**',
                '**/*.pyc',
                '**/.cache/**',
                '**/node_modules/**'
            ]
        )

        all_files = parser.find_all_source_files(self.project_path)

        # Convert to relative paths for easier checking
        relative_files = [
            str(Path(f).relative_to(self.project_path)) for f in all_files
        ]

        # Check that excluded files are NOT present
        self.assertNotIn('build\\main.o', relative_files)
        self.assertNotIn('build\\Debug\\app.exe', relative_files)
        self.assertNotIn('third_party\\lib\\helper.cpp', relative_files)
        self.assertNotIn('.git\\config', relative_files)
        self.assertNotIn('node_modules\\package\\index.js', relative_files)

        # Check that included files ARE present
        self.assertIn('src\\main.cpp', relative_files)
        self.assertIn('src\\module1\\class1.h', relative_files)
        self.assertIn('README.md', relative_files)

    def test_custom_exclusion_patterns(self):
        """Test custom exclusion patterns"""
        parser = CppParser(
            include_patterns=['**/*.cpp', '**/*.h'],
            exclude_patterns=['**/test/**', '**/tests/**']
        )

        # Create test directory
        (self.project_path / 'test').mkdir(exist_ok=True)
        test_file = self.project_path / 'test/test_main.cpp'
        test_file.write_text('// test file')

        # Should be excluded
        self.assertTrue(parser._is_excluded(test_file, self.project_path))


if __name__ == '__main__':
    unittest.main()

#!/usr/bin/env python3
"""
Comprehensive test suite for GitHub Repository Analyzer
Tests all components and integration points
"""

import asyncio
import json
import os
import tempfile
import unittest
from pathlib import Path
from unittest.mock import Mock, patch, MagicMock
import shutil
import sqlite3

# Import modules under test
import sys
sys.path.append(str(Path(__file__).parent.parent / "brain" / "modules"))

from github_analyzer import (
    GitHubRepositoryAnalyzer, GitCloner, DockerSandbox,
    CodeStructureAnalyzer, SecurityAuditAnalyzer,
    ExtractedFeature, AnalysisReport, CompatibilityScore
)

from analyzer_agents import (
    CodeStructureAgent, SecurityAuditAgent, QualityAssessmentAgent,
    PerformanceProfilerAgent, MultiAgentOrchestrator
)

class TestGitCloner(unittest.TestCase):
    """Test the GitCloner class"""
    
    def setUp(self):
        self.temp_dir = tempfile.mkdtemp()
        self.cloner = GitCloner(self.temp_dir)
    
    def tearDown(self):
        shutil.rmtree(self.temp_dir, ignore_errors=True)
    
    def test_clone_directory_creation(self):
        """Test that clone directory is created correctly"""
        self.assertTrue(Path(self.temp_dir).exists())
    
    @patch('git.Repo.clone_from')
    def test_clone_repository_success(self, mock_clone):
        """Test successful repository cloning"""
        mock_repo = Mock()
        mock_clone.return_value = mock_repo
        
        repo_url = "https://github.com/test/repo.git"
        result = self.cloner.clone_repository(repo_url)
        
        self.assertIsInstance(result, Path)
        self.assertTrue(str(result).startswith(self.temp_dir))
        mock_clone.assert_called_once()
    
    @patch('git.Repo.clone_from')
    def test_clone_repository_failure(self, mock_clone):
        """Test repository cloning failure"""
        mock_clone.side_effect = Exception("Clone failed")
        
        repo_url = "https://github.com/invalid/repo.git"
        
        with self.assertRaises(Exception) as context:
            self.cloner.clone_repository(repo_url)
        
        self.assertIn("Failed to clone repository", str(context.exception))
    
    def test_cleanup(self):
        """Test repository cleanup"""
        test_dir = Path(self.temp_dir) / "test_cleanup"
        test_dir.mkdir()
        test_file = test_dir / "test.txt"
        test_file.write_text("test content")
        
        self.assertTrue(test_dir.exists())
        self.cloner.cleanup(test_dir)
        self.assertFalse(test_dir.exists())

class TestDockerSandbox(unittest.TestCase):
    """Test the DockerSandbox class"""
    
    def setUp(self):
        self.sandbox = DockerSandbox()
    
    @patch('docker.from_env')
    def test_docker_client_initialization(self, mock_docker):
        """Test Docker client initialization"""
        mock_client = Mock()
        mock_docker.return_value = mock_client
        
        sandbox = DockerSandbox()
        mock_docker.assert_called_once()
    
    @patch('docker.from_env')
    def test_build_analysis_image_exists(self, mock_docker):
        """Test when analysis image already exists"""
        mock_client = Mock()
        mock_docker.return_value = mock_client
        mock_client.images.get.return_value = Mock()  # Image exists
        
        sandbox = DockerSandbox()
        sandbox.build_analysis_image()
        
        mock_client.images.get.assert_called_once_with("aai-repo-analyzer:latest")
        mock_client.images.build.assert_not_called()
    
    @patch('docker.from_env')
    def test_run_analysis_success(self, mock_docker):
        """Test successful analysis run"""
        mock_client = Mock()
        mock_docker.return_value = mock_client
        
        mock_container = Mock()
        mock_container.wait.return_value = {'StatusCode': 0}
        mock_container.logs.return_value = b'Analysis complete'
        mock_client.containers.run.return_value = mock_container
        mock_client.images.get.return_value = Mock()  # Image exists
        
        sandbox = DockerSandbox()
        result = sandbox.run_analysis(Path("/test"), "print('test')")
        
        self.assertTrue(result['success'])
        self.assertEqual(result['exit_code'], 0)
        self.assertEqual(result['logs'], 'Analysis complete')

class TestCodeStructureAnalyzer(unittest.TestCase):
    """Test the CodeStructureAnalyzer class"""
    
    def setUp(self):
        self.analyzer = CodeStructureAnalyzer()
        self.temp_dir = tempfile.mkdtemp()
    
    def tearDown(self):
        shutil.rmtree(self.temp_dir, ignore_errors=True)
    
    def test_analyze_python_file(self):
        """Test Python file analysis"""
        # Create a test Python file
        test_file = Path(self.temp_dir) / "test.py"
        test_code = '''
def test_function(arg1, arg2):
    """Test function docstring"""
    if arg1 > arg2:
        return arg1
    else:
        return arg2

class TestClass:
    """Test class docstring"""
    def method1(self):
        pass
    
    def method2(self):
        for i in range(10):
            if i % 2 == 0:
                print(i)
'''
        test_file.write_text(test_code)
        
        features = self.analyzer.analyze_structure(Path(self.temp_dir))
        
        # Should find both function and class
        self.assertGreaterEqual(len(features), 2)
        
        function_features = [f for f in features if f.type == "function"]
        class_features = [f for f in features if f.type == "class"]
        
        self.assertGreaterEqual(len(function_features), 1)
        self.assertGreaterEqual(len(class_features), 1)
        
        # Check that function has docstring
        test_func = next((f for f in function_features if f.name == "test_function"), None)
        self.assertIsNotNone(test_func)
        self.assertIn("Test function", test_func.description)

class TestCodeStructureAgent(unittest.TestCase):
    """Test the CodeStructureAgent class"""
    
    def setUp(self):
        self.agent = CodeStructureAgent()
        self.temp_dir = tempfile.mkdtemp()
    
    def tearDown(self):
        shutil.rmtree(self.temp_dir, ignore_errors=True)
    
    async def test_analyze_empty_directory(self):
        """Test analysis of empty directory"""
        result = await self.agent.analyze(Path(self.temp_dir))
        
        self.assertTrue(result.success)
        self.assertEqual(result.agent_name, "CodeStructureAgent")
        self.assertIn('languages', result.data)
        self.assertIn('file_structure', result.data)
    
    async def test_analyze_python_project(self):
        """Test analysis of Python project"""
        # Create a simple Python project structure
        src_dir = Path(self.temp_dir) / "src"
        src_dir.mkdir()
        
        main_file = src_dir / "main.py"
        main_file.write_text('''
def main():
    """Main function"""
    print("Hello, World!")

if __name__ == "__main__":
    main()
''')
        
        utils_file = src_dir / "utils.py"
        utils_file.write_text('''
class Calculator:
    """Simple calculator class"""
    
    def add(self, a, b):
        return a + b
    
    def multiply(self, a, b):
        return a * b
''')
        
        result = await self.agent.analyze(Path(self.temp_dir))
        
        self.assertTrue(result.success)
        self.assertIn('py', result.data['languages'])
        self.assertGreater(result.data['languages']['py']['functions'], 0)
        self.assertGreater(result.data['languages']['py']['classes'], 0)

class TestSecurityAuditAgent(unittest.TestCase):
    """Test the SecurityAuditAgent class"""
    
    def setUp(self):
        self.agent = SecurityAuditAgent()
        self.temp_dir = tempfile.mkdtemp()
    
    def tearDown(self):
        shutil.rmtree(self.temp_dir, ignore_errors=True)
    
    async def test_analyze_clean_code(self):
        """Test analysis of clean code with no security issues"""
        # Create a clean Python file
        test_file = Path(self.temp_dir) / "clean.py"
        test_file.write_text('''
def safe_function():
    """A safe function with no security issues"""
    return "Hello, World!"
''')
        
        result = await self.agent.analyze(Path(self.temp_dir))
        
        self.assertTrue(result.success)
        self.assertIn('security_score', result.data)
        self.assertIn('vulnerabilities', result.data)
        self.assertIn('secret_leaks', result.data)
    
    async def test_secret_detection(self):
        """Test detection of potential secrets"""
        # Create a file with potential secrets
        test_file = Path(self.temp_dir) / "secrets.py"
        test_file.write_text('''
API_KEY = "sk-1234567890abcdef1234567890abcdef"
SECRET_TOKEN = "ghp_1234567890abcdef1234567890abcdef123456"
password = "super_secret_password"
''')
        
        result = await self.agent.analyze(Path(self.temp_dir))
        
        self.assertTrue(result.success)
        self.assertGreater(len(result.data['secret_leaks']), 0)
        self.assertLess(result.data['security_score'], 1.0)

class TestQualityAssessmentAgent(unittest.TestCase):
    """Test the QualityAssessmentAgent class"""
    
    def setUp(self):
        self.agent = QualityAssessmentAgent()
        self.temp_dir = tempfile.mkdtemp()
    
    def tearDown(self):
        shutil.rmtree(self.temp_dir, ignore_errors=True)
    
    async def test_analyze_high_quality_code(self):
        """Test analysis of high-quality code"""
        # Create a well-documented Python module
        src_dir = Path(self.temp_dir) / "src"
        src_dir.mkdir()
        
        main_file = src_dir / "main.py"
        main_file.write_text('''
"""
High-quality Python module with good documentation
"""

def well_documented_function(param1: int, param2: str) -> str:
    """
    A well-documented function with type hints
    
    Args:
        param1: An integer parameter
        param2: A string parameter
    
    Returns:
        A formatted string
    """
    return f"{param2}: {param1}"

class WellDocumentedClass:
    """
    A well-documented class with clear purpose
    """
    
    def __init__(self, value: int):
        """Initialize with a value"""
        self.value = value
    
    def get_value(self) -> int:
        """Get the stored value"""
        return self.value
''')
        
        # Create test file
        test_dir = Path(self.temp_dir) / "tests"
        test_dir.mkdir()
        test_file = test_dir / "test_main.py"
        test_file.write_text('''
import unittest
from src.main import well_documented_function, WellDocumentedClass

class TestMain(unittest.TestCase):
    def test_function(self):
        result = well_documented_function(42, "Answer")
        self.assertEqual(result, "Answer: 42")
    
    def test_class(self):
        obj = WellDocumentedClass(100)
        self.assertEqual(obj.get_value(), 100)
''')
        
        # Create README
        readme_file = Path(self.temp_dir) / "README.md"
        readme_file.write_text('''
# High Quality Project

This is a well-documented project with tests and clear structure.

## Usage

```python
from src.main import well_documented_function
result = well_documented_function(42, "Hello")
```
''')
        
        result = await self.agent.analyze(Path(self.temp_dir))
        
        self.assertTrue(result.success)
        self.assertGreater(result.data['overall_score'], 0.7)  # Should be high quality
        self.assertGreater(result.data['test_coverage'], 0.0)
        self.assertGreater(result.data['documentation_score'], 0.7)

class TestPerformanceProfilerAgent(unittest.TestCase):
    """Test the PerformanceProfilerAgent class"""
    
    def setUp(self):
        self.agent = PerformanceProfilerAgent()
        self.temp_dir = tempfile.mkdtemp()
    
    def tearDown(self):
        shutil.rmtree(self.temp_dir, ignore_errors=True)
    
    async def test_analyze_performance_issues(self):
        """Test detection of performance issues"""
        # Create a file with performance issues
        test_file = Path(self.temp_dir) / "slow.py"
        test_file.write_text('''
def slow_function():
    # Nested loops - performance issue
    for i in range(1000):
        for j in range(1000):
            result = i * j
    
    # Inefficient string concatenation
    text = ""
    for i in range(100):
        text += str(i)
    
    return text

def inefficient_check(items):
    # Inefficient length check
    if len(items) == 0:
        return True
    return False
''')
        
        result = await self.agent.analyze(Path(self.temp_dir))
        
        self.assertTrue(result.success)
        self.assertIn('bottlenecks', result.data)
        self.assertIn('optimization_opportunities', result.data)
        self.assertGreater(len(result.data['bottlenecks']), 0)
        self.assertGreater(len(result.data['optimization_opportunities']), 0)

class TestMultiAgentOrchestrator(unittest.TestCase):
    """Test the MultiAgentOrchestrator class"""
    
    def setUp(self):
        self.orchestrator = MultiAgentOrchestrator()
        self.temp_dir = tempfile.mkdtemp()
    
    def tearDown(self):
        shutil.rmtree(self.temp_dir, ignore_errors=True)
    
    async def test_run_all_agents(self):
        """Test running all agents"""
        # Create a simple test project
        test_file = Path(self.temp_dir) / "test.py"
        test_file.write_text('''
def simple_function():
    """A simple test function"""
    return "Hello, World!"
''')
        
        results = await self.orchestrator.run_analysis(Path(self.temp_dir))
        
        # Should have results from all agents
        expected_agents = ['structure', 'security', 'quality', 'performance']
        for agent_name in expected_agents:
            self.assertIn(agent_name, results)
            self.assertIsNotNone(results[agent_name])
    
    async def test_run_specific_agents(self):
        """Test running specific agents only"""
        test_file = Path(self.temp_dir) / "test.py"
        test_file.write_text('def test(): pass')
        
        results = await self.orchestrator.run_analysis(
            Path(self.temp_dir), 
            agent_names=['structure', 'security']
        )
        
        self.assertIn('structure', results)
        self.assertIn('security', results)
        self.assertNotIn('quality', results)
        self.assertNotIn('performance', results)

class TestGitHubRepositoryAnalyzer(unittest.TestCase):
    """Test the main GitHubRepositoryAnalyzer class"""
    
    def setUp(self):
        self.temp_dir = tempfile.mkdtemp()
        self.analyzer = GitHubRepositoryAnalyzer(self.temp_dir)
    
    def tearDown(self):
        shutil.rmtree(self.temp_dir, ignore_errors=True)
    
    def test_database_initialization(self):
        """Test that database is initialized correctly"""
        self.assertTrue(self.analyzer.db_path.exists())
        
        # Check that tables exist
        with sqlite3.connect(self.analyzer.db_path) as conn:
            cursor = conn.execute(
                "SELECT name FROM sqlite_master WHERE type='table'"
            )
            tables = [row[0] for row in cursor.fetchall()]
            
            self.assertIn('analyses', tables)
            self.assertIn('features', tables)
    
    @patch.object(GitCloner, 'clone_repository')
    @patch.object(GitCloner, 'cleanup')
    async def test_analyze_repository_success(self, mock_cleanup, mock_clone):
        """Test successful repository analysis"""
        # Create a mock repository directory
        mock_repo_dir = Path(self.temp_dir) / "test_repo"
        mock_repo_dir.mkdir()
        
        # Create a simple Python file
        test_file = mock_repo_dir / "main.py"
        test_file.write_text('''
def main():
    """Main function"""
    print("Hello, World!")
''')
        
        # Create a simple git repository structure
        git_dir = mock_repo_dir / ".git"
        git_dir.mkdir()
        
        mock_clone.return_value = mock_repo_dir
        
        # Mock git repository
        with patch('git.Repo') as mock_repo_class:
            mock_repo = Mock()
            mock_repo.head.commit.hexsha = "abcd1234567890"
            mock_repo.iter_commits.return_value = [Mock(), Mock(), Mock()]
            mock_repo_class.return_value = mock_repo
            
            result = await self.analyzer.analyze_repository("https://github.com/test/repo.git")
        
        self.assertTrue(result.success)
        self.assertEqual(result.repo_url, "https://github.com/test/repo.git")
        self.assertGreater(len(result.features), 0)
        mock_clone.assert_called_once()
        mock_cleanup.assert_called_once()
    
    @patch.object(GitCloner, 'clone_repository')
    async def test_analyze_repository_failure(self, mock_clone):
        """Test repository analysis failure"""
        mock_clone.side_effect = Exception("Clone failed")
        
        result = await self.analyzer.analyze_repository("https://github.com/invalid/repo.git")
        
        self.assertFalse(result.success)
        self.assertIsNotNone(result.error_message)
    
    def test_get_analysis_history(self):
        """Test getting analysis history"""
        # Insert test data
        with sqlite3.connect(self.analyzer.db_path) as conn:
            conn.execute("""
                INSERT INTO analyses 
                (id, repo_url, repo_name, timestamp, success, overall_score, report_json)
                VALUES (?, ?, ?, ?, ?, ?, ?)
            """, (
                "test_id",
                "https://github.com/test/repo.git",
                "test-repo",
                "2023-01-01T00:00:00",
                True,
                0.85,
                "{}"
            ))
        
        history = self.analyzer.get_analysis_history()
        
        self.assertEqual(len(history), 1)
        self.assertEqual(history[0]['repo_name'], 'test-repo')
        self.assertTrue(history[0]['success'])
    
    def test_get_recommended_features(self):
        """Test getting recommended features"""
        # Insert test data
        with sqlite3.connect(self.analyzer.db_path) as conn:
            # Insert analysis
            conn.execute("""
                INSERT INTO analyses 
                (id, repo_url, repo_name, timestamp, success, overall_score, report_json)
                VALUES (?, ?, ?, ?, ?, ?, ?)
            """, (
                "test_id",
                "https://github.com/test/repo.git",
                "test-repo",
                "2023-01-01T00:00:00",
                True,
                0.85,
                "{}"
            ))
            
            # Insert feature
            conn.execute("""
                INSERT INTO features
                (id, analysis_id, name, type, compatibility_score, integrated)
                VALUES (?, ?, ?, ?, ?, ?)
            """, (
                "feature_id",
                "test_id",
                "test_function",
                "function",
                0.9,
                False
            ))
        
        recommendations = self.analyzer.get_recommended_features()
        
        self.assertEqual(len(recommendations), 1)
        self.assertEqual(recommendations[0]['name'], 'test_function')
        self.assertEqual(recommendations[0]['score'], 0.9)

class TestIntegrationScenarios(unittest.TestCase):
    """Test integration scenarios with real-world-like data"""
    
    def setUp(self):
        self.temp_dir = tempfile.mkdtemp()
        self.test_repo_dir = Path(self.temp_dir) / "integration_test_repo"
        self.test_repo_dir.mkdir()
    
    def tearDown(self):
        shutil.rmtree(self.temp_dir, ignore_errors=True)
    
    def create_realistic_python_project(self):
        """Create a realistic Python project for testing"""
        # Create directory structure
        src_dir = self.test_repo_dir / "src"
        tests_dir = self.test_repo_dir / "tests"
        docs_dir = self.test_repo_dir / "docs"
        
        src_dir.mkdir()
        tests_dir.mkdir()
        docs_dir.mkdir()
        
        # Create main module
        main_file = src_dir / "calculator.py"
        main_file.write_text('''
"""
A simple calculator module for demonstration
"""

import logging
from typing import Union

class Calculator:
    """
    A calculator class that performs basic arithmetic operations
    """
    
    def __init__(self):
        self.logger = logging.getLogger(__name__)
        self.history = []
    
    def add(self, a: Union[int, float], b: Union[int, float]) -> Union[int, float]:
        """
        Add two numbers
        
        Args:
            a: First number
            b: Second number
            
        Returns:
            Sum of a and b
        """
        result = a + b
        self.history.append(f"{a} + {b} = {result}")
        self.logger.info(f"Added {a} + {b} = {result}")
        return result
    
    def multiply(self, a: Union[int, float], b: Union[int, float]) -> Union[int, float]:
        """
        Multiply two numbers
        
        Args:
            a: First number
            b: Second number
            
        Returns:
            Product of a and b
        """
        result = a * b
        self.history.append(f"{a} * {b} = {result}")
        return result
    
    def get_history(self) -> list:
        """Get calculation history"""
        return self.history.copy()

def main():
    """Main function for CLI usage"""
    calc = Calculator()
    print(f"2 + 3 = {calc.add(2, 3)}")
    print(f"4 * 5 = {calc.multiply(4, 5)}")

if __name__ == "__main__":
    main()
''')
        
        # Create utility module
        utils_file = src_dir / "utils.py"
        utils_file.write_text('''
"""
Utility functions for the calculator
"""

def validate_number(value):
    """
    Validate that a value is a number
    
    Args:
        value: Value to validate
        
    Returns:
        True if valid number, False otherwise
    """
    try:
        float(value)
        return True
    except (ValueError, TypeError):
        return False

def format_result(result, decimals=2):
    """
    Format calculation result
    
    Args:
        result: Calculation result
        decimals: Number of decimal places
        
    Returns:
        Formatted string
    """
    if isinstance(result, float):
        return f"{result:.{decimals}f}"
    return str(result)
''')
        
        # Create test file
        test_file = tests_dir / "test_calculator.py"
        test_file.write_text('''
"""
Tests for calculator module
"""

import unittest
import sys
from pathlib import Path

# Add src to path
sys.path.append(str(Path(__file__).parent.parent / "src"))

from calculator import Calculator
from utils import validate_number, format_result

class TestCalculator(unittest.TestCase):
    """Test calculator functionality"""
    
    def setUp(self):
        self.calc = Calculator()
    
    def test_add(self):
        """Test addition"""
        result = self.calc.add(2, 3)
        self.assertEqual(result, 5)
    
    def test_multiply(self):
        """Test multiplication"""
        result = self.calc.multiply(4, 5)
        self.assertEqual(result, 20)
    
    def test_history(self):
        """Test calculation history"""
        self.calc.add(1, 1)
        self.calc.multiply(2, 3)
        history = self.calc.get_history()
        self.assertEqual(len(history), 2)

class TestUtils(unittest.TestCase):
    """Test utility functions"""
    
    def test_validate_number(self):
        """Test number validation"""
        self.assertTrue(validate_number(42))
        self.assertTrue(validate_number("3.14"))
        self.assertFalse(validate_number("not a number"))
    
    def test_format_result(self):
        """Test result formatting"""
        self.assertEqual(format_result(3.14159, 2), "3.14")
        self.assertEqual(format_result(42), "42")

if __name__ == "__main__":
    unittest.main()
''')
        
        # Create README
        readme_file = self.test_repo_dir / "README.md"
        readme_file.write_text('''
# Calculator Project

A simple calculator implementation in Python with comprehensive testing.

## Features

- Basic arithmetic operations (add, multiply)
- Calculation history
- Input validation
- Comprehensive test suite

## Usage

```python
from src.calculator import Calculator

calc = Calculator()
result = calc.add(2, 3)
print(f"Result: {result}")
```

## Testing

Run tests with:
```bash
python -m pytest tests/
```
''')
        
        # Create requirements.txt
        requirements_file = self.test_repo_dir / "requirements.txt"
        requirements_file.write_text('''
pytest>=7.0.0
''')
        
        # Create LICENSE
        license_file = self.test_repo_dir / "LICENSE"
        license_file.write_text('''
MIT License

Copyright (c) 2023 Test Project

Permission is hereby granted, free of charge, to any person obtaining a copy...
''')
    
    async def test_full_analysis_pipeline(self):
        """Test the complete analysis pipeline"""
        self.create_realistic_python_project()
        
        # Test multi-agent orchestrator
        orchestrator = MultiAgentOrchestrator()
        results = await orchestrator.run_analysis(self.test_repo_dir)
        
        # Verify all agents ran successfully
        self.assertEqual(len(results), 4)  # 4 agents
        for agent_name, result in results.items():
            self.assertTrue(result.success, f"{agent_name} failed: {result.errors}")
        
        # Verify structure analysis found features
        structure_result = results['structure']
        self.assertGreater(len(structure_result.data['languages']), 0)
        self.assertIn('py', structure_result.data['languages'])
        
        # Verify quality analysis found good practices
        quality_result = results['quality']
        self.assertGreater(quality_result.data['overall_score'], 0.5)
        self.assertGreater(quality_result.data['test_coverage'], 0.0)
        self.assertGreater(quality_result.data['documentation_score'], 0.5)
        
        # Verify security analysis completed
        security_result = results['security']
        self.assertIn('security_score', security_result.data)
        self.assertGreater(security_result.data['security_score'], 0.8)  # Should be clean
        
        # Verify performance analysis completed
        performance_result = results['performance']
        self.assertIn('performance_score', performance_result.data)

async def run_async_tests():
    """Run async test methods"""
    test_classes = [
        TestCodeStructureAgent,
        TestSecurityAuditAgent,
        TestQualityAssessmentAgent,
        TestPerformanceProfilerAgent,
        TestMultiAgentOrchestrator,
        TestGitHubRepositoryAnalyzer,
        TestIntegrationScenarios
    ]
    
    for test_class in test_classes:
        suite = unittest.TestLoader().loadTestsFromTestCase(test_class)
        for test in suite:
            if hasattr(test, '_testMethodName'):
                method = getattr(test, test._testMethodName)
                if asyncio.iscoroutinefunction(method):
                    print(f"Running async test: {test_class.__name__}.{test._testMethodName}")
                    try:
                        await method()
                        print(f"  ✓ PASSED")
                    except Exception as e:
                        print(f"  ✗ FAILED: {e}")

def main():
    """Run all tests"""
    print("Running GitHub Repository Analyzer Test Suite")
    print("=" * 50)
    
    # Run sync tests
    print("\n1. Running synchronous tests...")
    loader = unittest.TestLoader()
    suite = unittest.TestSuite()
    
    # Add sync test classes
    sync_test_classes = [
        TestGitCloner,
        TestDockerSandbox,
        TestCodeStructureAnalyzer,
        TestGitHubRepositoryAnalyzer
    ]
    
    for test_class in sync_test_classes:
        tests = loader.loadTestsFromTestCase(test_class)
        suite.addTests(tests)
    
    runner = unittest.TextTestRunner(verbosity=2)
    sync_result = runner.run(suite)
    
    # Run async tests
    print("\n2. Running asynchronous tests...")
    asyncio.run(run_async_tests())
    
    print("\n" + "=" * 50)
    if sync_result.wasSuccessful():
        print("✓ All synchronous tests passed!")
    else:
        print(f"✗ {len(sync_result.failures)} test(s) failed, {len(sync_result.errors)} error(s)")
    
    print("Test suite completed.")

if __name__ == "__main__":
    main()
#!/usr/bin/env python3
"""
Pytest configuration and fixtures for Enhanced Repository Analyzer tests
"""

import asyncio
import pytest
import tempfile
import shutil
from pathlib import Path
from typing import AsyncGenerator, Generator
import logging

# Configure test logging
logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)

# Test configuration
pytest_plugins = ['pytest_asyncio']

@pytest.fixture(scope="session")
def event_loop():
    """Create an instance of the default event loop for the test session."""
    loop = asyncio.get_event_loop_policy().new_event_loop()
    yield loop
    loop.close()

@pytest.fixture
async def temp_cache_dir() -> AsyncGenerator[Path, None]:
    """Create temporary cache directory for testing"""
    with tempfile.TemporaryDirectory(prefix="test_cache_") as temp_dir:
        yield Path(temp_dir)

@pytest.fixture
async def sample_python_code() -> str:
    """Sample Python code for testing"""
    return '''
import asyncio
import logging
from typing import List, Dict, Optional

class DataProcessor:
    """Process data with various methods"""
    
    def __init__(self, config: Dict[str, str]):
        self.config = config
        self.logger = logging.getLogger(__name__)
    
    async def process_data(self, data: List[str]) -> Optional[Dict[str, any]]:
        """Process incoming data asynchronously"""
        try:
            results = {}
            for item in data:
                processed = await self._process_item(item)
                results[item] = processed
            return results
        except Exception as e:
            self.logger.error(f"Processing failed: {e}")
            return None
    
    async def _process_item(self, item: str) -> str:
        """Process individual item"""
        # TODO: Implement actual processing logic
        await asyncio.sleep(0.01)  # Simulate processing
        return item.upper()

# Main execution
if __name__ == "__main__":
    processor = DataProcessor({"mode": "test"})
    data = ["hello", "world", "test"]
    result = asyncio.run(processor.process_data(data))
    print(result)
'''

@pytest.fixture
async def sample_javascript_code() -> str:
    """Sample JavaScript code for testing"""
    return '''
const express = require('express');
const { promisify } = require('util');

class ApiServer {
    constructor(config) {
        this.app = express();
        this.config = config;
        this.setupMiddleware();
        this.setupRoutes();
    }
    
    setupMiddleware() {
        this.app.use(express.json());
        this.app.use((req, res, next) => {
            console.log(`${req.method} ${req.path}`);
            next();
        });
    }
    
    setupRoutes() {
        this.app.get('/health', (req, res) => {
            res.json({ status: 'healthy', timestamp: new Date().toISOString() });
        });
        
        this.app.post('/process', async (req, res) => {
            try {
                const result = await this.processData(req.body);
                res.json({ success: true, data: result });
            } catch (error) {
                res.status(500).json({ success: false, error: error.message });
            }
        });
    }
    
    async processData(data) {
        // TODO: Implement data processing
        return { processed: true, count: data.length };
    }
    
    start(port = 3000) {
        return new Promise((resolve) => {
            this.server = this.app.listen(port, () => {
                console.log(`Server running on port ${port}`);
                resolve();
            });
        });
    }
}

module.exports = ApiServer;
'''

@pytest.fixture
async def test_repository() -> AsyncGenerator[Path, None]:
    """Create a test repository with sample files"""
    with tempfile.TemporaryDirectory(prefix="test_repo_") as temp_dir:
        repo_path = Path(temp_dir)
        
        # Create directory structure
        (repo_path / "src").mkdir()
        (repo_path / "tests").mkdir()
        (repo_path / "docs").mkdir()
        (repo_path / "config").mkdir()
        
        # Create Python files
        with open(repo_path / "src" / "main.py", "w") as f:
            f.write('''
#!/usr/bin/env python3
"""Main application entry point"""

import asyncio
from .processor import DataProcessor

async def main():
    """Main function"""
    processor = DataProcessor()
    await processor.run()

if __name__ == "__main__":
    asyncio.run(main())
''')
        
        with open(repo_path / "src" / "processor.py", "w") as f:
            f.write('''
"""Data processing module"""

class DataProcessor:
    """Process data efficiently"""
    
    def __init__(self):
        self.data = []
    
    async def run(self):
        """Run the processor"""
        print("Processing data...")
        return True
''')
        
        # Create JavaScript files
        with open(repo_path / "src" / "app.js", "w") as f:
            f.write('''
const express = require('express');
const app = express();

app.get('/', (req, res) => {
    res.json({ message: 'Hello World' });
});

module.exports = app;
''')
        
        # Create configuration files
        with open(repo_path / "package.json", "w") as f:
            f.write('''{
    "name": "test-project",
    "version": "1.0.0",
    "description": "Test project for analyzer",
    "main": "src/app.js",
    "scripts": {
        "start": "node src/app.js",
        "test": "jest"
    },
    "dependencies": {
        "express": "^4.18.0"
    }
}''')
        
        with open(repo_path / "requirements.txt", "w") as f:
            f.write('''
fastapi>=0.100.0
uvicorn>=0.23.0
pytest>=7.4.0
pytest-asyncio>=0.21.0
''')
        
        with open(repo_path / "README.md", "w") as f:
            f.write('''# Test Project

This is a test project for the Enhanced Repository Analyzer.

## Features

- Python backend with async processing
- Express.js API server
- Comprehensive testing

## Installation

```bash
pip install -r requirements.txt
npm install
```

## Usage

```bash
python src/main.py
```
''')
        
        # Create test files
        with open(repo_path / "tests" / "test_processor.py", "w") as f:
            f.write('''
import pytest
from src.processor import DataProcessor

@pytest.mark.asyncio
async def test_processor_run():
    """Test processor runs successfully"""
    processor = DataProcessor()
    result = await processor.run()
    assert result is True
''')
        
        yield repo_path

@pytest.fixture
async def test_files_batch():
    """Create a batch of test files for streaming tests"""
    with tempfile.TemporaryDirectory() as temp_dir:
        base_path = Path(temp_dir)
        
        files = []
        for i in range(10):
            file_path = base_path / f"test_file_{i}.py"
            with open(file_path, "w") as f:
                f.write(f'''
def function_{i}():
    """Test function {i}"""
    return {i}

class TestClass{i}:
    """Test class {i}"""
    
    def method_{i}(self):
        return function_{i}()
''')
            files.append(file_path)
        
        yield files

@pytest.fixture
def performance_targets():
    """Default performance targets for testing"""
    return {
        'max_execution_time': 60.0,
        'min_cache_hit_rate': 0.3,
        'max_memory_mb': 500.0,
        'min_files_per_second': 10.0
    }

@pytest.fixture
async def mock_openrouter_response():
    """Mock OpenRouter API response"""
    return {
        'primary_purpose': 'Data processing and API management',
        'business_logic': 'Handles data transformation and HTTP requests',
        'complexity_assessment': 'Medium complexity with async patterns',
        'potential_issues': ['TODO comments indicate incomplete implementation'],
        'suggestions': ['Add error handling', 'Implement caching'],
        'confidence': 0.85
    }

# Performance test markers
def pytest_configure(config):
    """Configure pytest with custom markers"""
    config.addinivalue_line(
        "markers", "performance: marks tests as performance tests"
    )
    config.addinivalue_line(
        "markers", "integration: marks tests as integration tests"
    )
    config.addinivalue_line(
        "markers", "benchmark: marks tests as benchmark tests"
    )

# Test data cleanup
@pytest.fixture(autouse=True)
async def cleanup_test_data():
    """Automatically cleanup test data after each test"""
    yield
    # Cleanup logic would go here if needed
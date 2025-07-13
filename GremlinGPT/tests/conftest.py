# ─────────────────────────────────────────────────────────────
# ⚠️ GremlinGPT Fair Use Only | Commercial Use Requires License
# Built under the GremlinGPT Dual License v1.0
# © 2025 StatikFintechLLC / AscendAI Project
# Contact: ascend.gremlin@gmail.com
# ─────────────────────────────────────────────────────────────

"""
GremlinGPT Test Configuration and Fixtures

This module provides shared test configuration, fixtures, and utilities
for the entire GremlinGPT testing suite.
"""

import pytest
import asyncio
import tempfile
import shutil
from pathlib import Path
import json
import os
import sys
from typing import Dict, Any, Generator, Optional
from unittest.mock import Mock, MagicMock

# Add project root to path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))

from utils.logging_config import setup_module_logger

# Initialize test logging
logger = setup_module_logger('tests', 'INFO')

# Test configuration constants
TEST_CONFIG = {
    'timeout': 30,
    'mock_api_port': 5555,
    'test_data_dir': 'test_data',
    'temp_dir': None,  # Will be set during setup
}

@pytest.fixture(scope="session")
def event_loop():
    """Create an instance of the default event loop for the test session."""
    loop = asyncio.get_event_loop_policy().new_event_loop()
    yield loop
    loop.close()

@pytest.fixture(scope="session")
def temp_test_dir():
    """Create a temporary directory for test files."""
    temp_dir = tempfile.mkdtemp(prefix="gremlin_test_")
    TEST_CONFIG['temp_dir'] = temp_dir
    logger.info(f"Created temporary test directory: {temp_dir}")
    yield temp_dir
    shutil.rmtree(temp_dir)
    logger.info(f"Cleaned up temporary test directory: {temp_dir}")

@pytest.fixture
def mock_config():
    """Provide mock configuration for tests."""
    return {
        'system': {
            'debug': True,
            'log_level': 'DEBUG',
            'temp_dir': TEST_CONFIG['temp_dir']
        },
        'memory': {
            'vector_store_type': 'mock',
            'embedding_dim': 384,
            'max_memory_size': 1000
        },
        'nlp': {
            'model_name': 'mock_model',
            'max_tokens': 512,
            'temperature': 0.7
        },
        'trading': {
            'mode': 'paper',
            'max_position_size': 1000,
            'risk_tolerance': 0.1
        },
        'scraper': {
            'timeout': 10,
            'max_retries': 3,
            'headless': True
        }
    }

@pytest.fixture
def mock_logger():
    """Provide a mock logger for testing."""
    mock_log = MagicMock()
    mock_log.info = Mock()
    mock_log.debug = Mock()
    mock_log.warning = Mock()
    mock_log.error = Mock()
    mock_log.critical = Mock()
    return mock_log

@pytest.fixture
def sample_text_data():
    """Provide sample text data for NLP testing."""
    return {
        'simple': "GremlinGPT is an autonomous AI system.",
        'complex': "The GremlinGPT system integrates multiple AI components including natural language processing, web scraping, trading algorithms, and self-improvement mechanisms to create a comprehensive autonomous trading and learning platform.",
        'code': "def hello_world():\n    print('Hello, GremlinGPT!')\n    return True",
        'json': '{"name": "GremlinGPT", "version": "1.0.3", "active": true}',
        'empty': "",
        'whitespace': "   \n\t  ",
        'unicode': "GremlinGPT supports unicode: 🤖 🧠 💰 📈",
        'markdown': "# GremlinGPT\n\n## Features\n- AI Trading\n- Self-Learning\n- Web Scraping"
    }

@pytest.fixture
def sample_vector_data():
    """Provide sample vector data for memory testing."""
    import numpy as np
    return {
        'simple_vector': np.random.random(384).astype(np.float32),
        'large_vector': np.random.random(1024).astype(np.float32),
        'small_vector': np.random.random(128).astype(np.float32),
        'zero_vector': np.zeros(384).astype(np.float32),
        'ones_vector': np.ones(384).astype(np.float32)
    }

@pytest.fixture
def sample_web_data():
    """Provide sample web data for scraper testing."""
    return {
        'html_simple': '<html><body><h1>Test Page</h1><p>Content</p></body></html>',
        'html_complex': '''
            <html>
                <head><title>Test Financial Page</title></head>
                <body>
                    <div class="stock-data">
                        <span class="symbol">AAPL</span>
                        <span class="price">$150.25</span>
                        <span class="change">+2.5%</span>
                    </div>
                    <table class="financial-data">
                        <tr><td>Volume</td><td>1,234,567</td></tr>
                        <tr><td>Market Cap</td><td>$2.5T</td></tr>
                    </table>
                </body>
            </html>
        ''',
        'json_api': {
            'symbol': 'TSLA',
            'price': 234.56,
            'change': 5.67,
            'volume': 987654,
            'timestamp': '2025-01-13T12:00:00Z'
        },
        'csv_data': 'Symbol,Price,Change,Volume\nAAPL,150.25,2.5,1234567\nTSLA,234.56,5.67,987654',
        'urls': [
            'https://example.com',
            'https://finance.yahoo.com',
            'https://marketwatch.com',
            'https://bloomberg.com'
        ]
    }

@pytest.fixture
def sample_trading_data():
    """Provide sample trading data for trading core testing."""
    return {
        'portfolio': {
            'cash': 10000.0,
            'positions': {
                'AAPL': {'shares': 10, 'avg_price': 145.50},
                'TSLA': {'shares': 5, 'avg_price': 220.00}
            }
        },
        'market_data': {
            'AAPL': {'price': 150.25, 'volume': 1234567, 'change': 2.5},
            'TSLA': {'price': 234.56, 'volume': 987654, 'change': 5.67},
            'MSFT': {'price': 385.12, 'volume': 543210, 'change': -1.2}
        },
        'signals': [
            {'symbol': 'AAPL', 'action': 'buy', 'confidence': 0.85, 'reason': 'strong earnings'},
            {'symbol': 'TSLA', 'action': 'sell', 'confidence': 0.75, 'reason': 'overvalued'},
            {'symbol': 'MSFT', 'action': 'hold', 'confidence': 0.65, 'reason': 'stable performance'}
        ]
    }

@pytest.fixture
def mock_api_responses():
    """Provide mock API responses for testing."""
    return {
        'chat_response': {
            'response': 'GremlinGPT processed your request successfully.',
            'confidence': 0.92,
            'timestamp': '2025-01-13T12:00:00Z',
            'tokens_used': 45
        },
        'memory_query': {
            'results': [
                {'text': 'Sample memory result 1', 'score': 0.95},
                {'text': 'Sample memory result 2', 'score': 0.87}
            ],
            'total_results': 2,
            'query_time': 0.045
        },
        'scraper_result': {
            'url': 'https://example.com',
            'status': 'success',
            'content_length': 1024,
            'extracted_data': {'title': 'Test Page', 'text': 'Sample content'},
            'timestamp': '2025-01-13T12:00:00Z'
        },
        'training_status': {
            'status': 'in_progress',
            'epoch': 5,
            'loss': 0.123,
            'accuracy': 0.876,
            'eta': '2 minutes'
        }
    }

@pytest.fixture
def test_file_paths(temp_test_dir):
    """Provide test file paths."""
    base_path = Path(temp_test_dir)
    paths = {
        'config': base_path / 'test_config.toml',
        'memory': base_path / 'test_memory.json',
        'logs': base_path / 'test_logs',
        'data': base_path / 'test_data',
        'models': base_path / 'test_models',
        'cache': base_path / 'test_cache'
    }
    
    # Create directories
    for path in paths.values():
        if path.suffix == '':  # Directory
            path.mkdir(exist_ok=True)
    
    return paths

@pytest.fixture
def performance_monitor():
    """Monitor test performance metrics."""
    import time
    import psutil
    
    class PerformanceMonitor:
        def __init__(self):
            self.start_time = None
            self.start_memory = None
            self.metrics = {}
        
        def start(self):
            self.start_time = time.time()
            self.start_memory = psutil.Process().memory_info().rss
        
        def stop(self):
            if self.start_time:
                self.metrics['duration'] = time.time() - self.start_time
                current_memory = psutil.Process().memory_info().rss
                self.metrics['memory_delta'] = current_memory - self.start_memory
                self.metrics['peak_memory'] = current_memory
            return self.metrics
    
    return PerformanceMonitor()

class TestHelpers:
    """Utility class for common test operations."""
    
    @staticmethod
    def create_test_file(path: Path, content: str = "test content"):
        """Create a test file with content."""
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(content)
        return path
    
    @staticmethod
    def assert_json_structure(data: Dict[str, Any], required_keys: list):
        """Assert that JSON data has required structure."""
        for key in required_keys:
            assert key in data, f"Missing required key: {key}"
    
    @staticmethod
    def assert_vector_properties(vector, expected_dim: Optional[int] = None, expected_type: Optional[type] = None):
        """Assert vector has expected properties."""
        import numpy as np
        assert isinstance(vector, np.ndarray), "Vector must be numpy array"
        if expected_dim:
            assert vector.shape[-1] == expected_dim, f"Expected dimension {expected_dim}, got {vector.shape[-1]}"
        if expected_type:
            assert vector.dtype == expected_type, f"Expected type {expected_type}, got {vector.dtype}"
    
    @staticmethod
    def assert_api_response(response, status_code: int = 200, required_keys: Optional[list] = None):
        """Assert API response has expected structure."""
        assert response.status_code == status_code
        if required_keys:
            data = response.json()
            TestHelpers.assert_json_structure(data, required_keys)

@pytest.fixture
def test_helpers():
    """Provide test helper utilities."""
    return TestHelpers()

# Test markers for organizing test categories
pytest_markers = [
    "unit: marks tests as unit tests",
    "integration: marks tests as integration tests", 
    "e2e: marks tests as end-to-end tests",
    "slow: marks tests as slow running",
    "network: marks tests that require network access",
    "memory_intensive: marks tests that use significant memory",
    "gpu: marks tests that require GPU",
    "trading: marks tests related to trading functionality",
    "nlp: marks tests related to NLP functionality",
    "scraper: marks tests related to scraping functionality",
    "agent: marks tests related to agent functionality"
]

def pytest_configure(config):
    """Configure pytest with custom markers."""
    for marker in pytest_markers:
        config.addinivalue_line("markers", marker)

def pytest_collection_modifyitems(config, items):
    """Modify test collection to add markers based on test names and locations."""
    for item in items:
        # Add markers based on test file names
        if "test_nlp" in item.fspath.basename:
            item.add_marker(pytest.mark.nlp)
        elif "test_trading" in item.fspath.basename:
            item.add_marker(pytest.mark.trading)
        elif "test_scraper" in item.fspath.basename:
            item.add_marker(pytest.mark.scraper)
        elif "test_agent" in item.fspath.basename:
            item.add_marker(pytest.mark.agent)
        
        # Add markers based on test names
        if "integration" in item.name:
            item.add_marker(pytest.mark.integration)
        elif "e2e" in item.name:
            item.add_marker(pytest.mark.e2e)
        elif "slow" in item.name:
            item.add_marker(pytest.mark.slow)
        else:
            item.add_marker(pytest.mark.unit)

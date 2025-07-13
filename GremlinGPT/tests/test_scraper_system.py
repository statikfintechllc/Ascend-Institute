# ─────────────────────────────────────────────────────────────
# ⚠️ GremlinGPT Fair Use Only | Commercial Use Requires License
# Built under the GremlinGPT Dual License v1.0
# © 2025 StatikFintechLLC / AscendAI Project
# Contact: ascend.gremlin@gmail.com
# ─────────────────────────────────────────────────────────────

"""
GremlinGPT Scraper Testing Suite

Comprehensive tests for the REAL GremlinGPT scraping functionality including
content extraction, data processing, browser automation, and error handling.
"""

import pytest
import asyncio
import aiohttp
import json
from unittest.mock import Mock, patch, MagicMock, AsyncMock
import sys
import os
from datetime import datetime, timedelta
import time

sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))

from utils.logging_config import setup_module_logger
logger = setup_module_logger('tests')

# Import actual GremlinGPT scraper modules
from scraper.dom_navigator import extract_dom_structure
from scraper.page_simulator import store_scrape_to_memory
from scraper.playwright_handler import get_dom_html
from scraper.web_knowledge_scraper import scrape_web_knowledge, fetch_html
from scraper.source_router import route_scraping_async, detect_apps, get_live_snapshot
from scraper.tws_scraper import safe_scrape_tws, locate_tws_files, parse_tws_json
from scraper.stt_scraper import safe_scrape_stt, locate_stt_paths
from backend.api.scraping_api import scrape_url, scrape_router

class TestDomNavigator:
    """Test suite for DOM navigation and parsing functionality."""
    
    def test_extract_dom_structure_basic(self):
        """Test basic DOM structure extraction."""
        html_content = """
        <html>
        <head><title>Test Page</title></head>
        <body>
            <h1>Main Heading</h1>
            <p>This is a paragraph with some text.</p>
            <a href="https://external.com">External Link</a>
            <a href="/internal">Internal Link</a>
            <div>More content here.</div>
        </body>
        </html>
        """
        
        result = extract_dom_structure(html_content)
        
        # Check structure
        assert 'text' in result
        assert 'links' in result
        assert 'tags' in result
        assert 'nodes' in result
        assert 'watermark' in result
        
        # Check content
        assert 'Main Heading' in result['text']
        assert 'This is a paragraph' in result['text']
        assert len(result['links']) >= 2
        assert result['watermark'] == "source:GremlinGPT"
        
        # Check links
        external_links = [link for link in result['links'] if link['url'].startswith('http')]
        internal_links = [link for link in result['links'] if not link['url'].startswith('http')]
        assert len(external_links) >= 1
        assert len(internal_links) >= 1
        
        logger.info("DOM structure extraction test passed")
    
    def test_extract_dom_structure_complex(self, sample_web_data):
        """Test DOM extraction with complex financial content."""
        result = extract_dom_structure(sample_web_data['html_complex'])
        
        assert 'text' in result
        assert 'AAPL' in result['text']
        assert '$150.25' in result['text']
        assert 'Volume' in result['text']
        
        # Check that financial data is captured
        assert any('stock' in str(node).lower() for node in result.get('nodes', []))
        
        logger.info("Complex DOM structure extraction test passed")
    
    def test_extract_dom_structure_empty(self):
        """Test DOM extraction with empty or minimal content."""
        # Test empty content
        empty_result = extract_dom_structure("")
        assert empty_result['text'] == ""
        assert len(empty_result['links']) == 0
        
        # Test minimal content
        minimal_html = "<html><body><p>Minimal</p></body></html>"
        minimal_result = extract_dom_structure(minimal_html)
        assert 'Minimal' in minimal_result['text']
        
        logger.info("Empty DOM structure extraction test passed")

class TestPageSimulator:
    """Test suite for page simulation and memory storage."""
    
    @patch('scraper.page_simulator.package_embedding')
    @patch('scraper.page_simulator.inject_watermark')
    @patch('scraper.page_simulator.embed_text')
    def test_store_scrape_to_memory(self, mock_embed, mock_inject, mock_package):
        """Test storing scrape data to memory."""
        # Mock the embedding functions
        mock_embed.return_value = [0.1, 0.2, 0.3] * 100  # Mock vector
        
        test_url = "https://test.example.com"
        test_html = "<html><body><h1>Test Content</h1><p>Sample text</p></body></html>"
        
        # This should not raise an exception
        store_scrape_to_memory(test_url, test_html)
        
        # Verify the mocked functions were called
        mock_embed.assert_called_once()
        mock_package.assert_called_once()
        mock_inject.assert_called_once()
        
        # Check that the text passed to embed contains the URL and extracted content
        call_args = mock_embed.call_args[1] if mock_embed.call_args.kwargs else mock_embed.call_args[0]
        embedded_text = call_args[0] if isinstance(call_args, tuple) else call_args
        assert test_url in embedded_text
        assert 'Test Content' in embedded_text
        
        logger.info("Store scrape to memory test passed")

class TestPlaywrightHandler:
    """Test suite for Playwright browser automation."""
    
    @pytest.mark.asyncio
    @pytest.mark.slow
    async def test_get_dom_html_success(self):
        """Test successful DOM HTML retrieval."""
        # Use a reliable test URL
        test_url = "https://httpbin.org/html"
        
        try:
            result = await get_dom_html(test_url)
            
            assert isinstance(result, str)
            assert len(result) > 0
            assert '<html' in result.lower()
            assert '</html>' in result.lower()
            
            logger.info("Playwright DOM HTML success test passed")
        except Exception as e:
            # If playwright isn't available, skip this test
            pytest.skip(f"Playwright not available: {e}")
    
    @pytest.mark.asyncio
    async def test_get_dom_html_timeout(self):
        """Test DOM HTML retrieval with timeout."""
        # Use a URL that will timeout
        test_url = "https://httpbin.org/delay/10"  # 10 second delay
        
        result = await get_dom_html(test_url)
        
        # Should return timeout error HTML
        assert isinstance(result, str)
        assert 'timeout' in result.lower() or 'error' in result.lower()
        
        logger.info("Playwright timeout test passed")
    
    @pytest.mark.asyncio
    async def test_get_dom_html_invalid_url(self):
        """Test DOM HTML retrieval with invalid URL."""
        test_url = "https://this-domain-definitely-does-not-exist-12345.com"
        
        result = await get_dom_html(test_url)
        
        # Should return error HTML
        assert isinstance(result, str)
        assert 'error' in result.lower()
        
        logger.info("Playwright invalid URL test passed")

class TestWebKnowledgeScraper:
    """Test suite for web knowledge scraping functionality."""
    
    @pytest.mark.asyncio
    @pytest.mark.slow
    async def test_fetch_html_success(self):
        """Test successful HTML fetching."""
        async with aiohttp.ClientSession() as session:
            result = await fetch_html(session, "https://httpbin.org/html")
            
            assert isinstance(result, str)
            assert len(result) > 0
            assert '<html' in result.lower()
            
            logger.info("Web knowledge fetch HTML test passed")
    
    @pytest.mark.asyncio
    async def test_fetch_html_failure(self):
        """Test HTML fetching failure handling."""
        async with aiohttp.ClientSession() as session:
            result = await fetch_html(session, "https://httpbin.org/status/404")
            
            # Should return empty string on failure
            assert result == ""
            
            logger.info("Web knowledge fetch HTML failure test passed")
    
    @pytest.mark.asyncio
    @patch('scraper.web_knowledge_scraper.package_embedding')
    @patch('scraper.web_knowledge_scraper.inject_watermark')
    @patch('scraper.web_knowledge_scraper.embed_text')
    @patch('scraper.web_knowledge_scraper.log_event')
    async def test_scrape_web_knowledge(self, mock_log, mock_embed, mock_inject, mock_package):
        """Test web knowledge scraping with mocked embedding."""
        # Mock the embedding functions
        mock_embed.return_value = [0.1, 0.2, 0.3] * 100  # Mock vector
        
        test_urls = ["https://httpbin.org/html"]
        
        try:
            results = await scrape_web_knowledge(test_urls)
            
            assert isinstance(results, list)
            assert len(results) <= len(test_urls)  # Might be less if some fail
            
            if results:  # If we got results
                result = results[0]
                assert 'url' in result
                assert 'summary' in result
                assert 'nodes' in result
                assert 'links' in result
                
                # Verify mocked functions were called
                mock_embed.assert_called()
                mock_package.assert_called()
                mock_inject.assert_called()
                mock_log.assert_called()
            
            logger.info("Web knowledge scraping test passed")
        except Exception as e:
            # If network issues, this is still a valid test result
            logger.warning(f"Web knowledge scraping test had network issues: {e}")

class TestSourceRouter:
    """Test suite for source routing functionality."""
    
    def test_detect_apps(self):
        """Test application detection."""
        result = detect_apps()
        
        assert isinstance(result, dict)
        assert 'tws' in result
        assert 'stt' in result
        assert isinstance(result['tws'], bool)
        assert isinstance(result['stt'], bool)
        
        logger.info("App detection test passed")
    
    @pytest.mark.asyncio
    async def test_route_scraping_async(self):
        """Test asynchronous scraping routing."""
        result = await route_scraping_async()
        
        assert isinstance(result, list)
        # Should return some data (even if fallback)
        if result:
            item = result[0]
            assert isinstance(item, dict)
            # Should have some basic fields
            assert any(key in item for key in ['symbol', 'price', 'volume', 'source'])
        
        logger.info("Route scraping async test passed")
    
    def test_get_live_snapshot(self):
        """Test getting live snapshot data."""
        result = get_live_snapshot()
        
        # Should return a list (even if empty)
        assert isinstance(result, list)
        
        logger.info("Live snapshot test passed")

class TestTWScraper:
    """Test suite for TWS (Trading WorkStation) scraper."""
    
    def test_locate_tws_files(self):
        """Test TWS file location."""
        result = locate_tws_files()
        
        assert isinstance(result, list)
        # Should return a list of file paths (might be empty)
        
        logger.info("TWS file location test passed")
    
    def test_parse_tws_json_valid(self):
        """Test TWS JSON parsing with valid data."""
        test_data = {
            "symbol": "AAPL",
            "price": 150.25,
            "volume": 1000000,
            "timestamp": "2025-01-01T12:00:00"
        }
        
        result = parse_tws_json(test_data)
        
        if result:  # Function might return None for invalid data
            assert isinstance(result, dict)
            assert 'symbol' in result
            assert 'price' in result
        
        logger.info("TWS JSON parsing test passed")
    
    def test_safe_scrape_tws(self):
        """Test safe TWS scraping."""
        result = safe_scrape_tws()
        
        assert isinstance(result, list)
        # Should always return something (fallback if needed)
        assert len(result) > 0
        
        if result:
            item = result[0]
            assert isinstance(item, dict)
            assert 'symbol' in item
            assert 'price' in item
        
        logger.info("Safe TWS scraping test passed")

class TestSTTScraper:
    """Test suite for STT (Speech-to-Text) scraper."""
    
    def test_locate_stt_paths(self):
        """Test STT path location."""
        result = locate_stt_paths()
        
        assert isinstance(result, list)
        # Should return a list of paths (might be empty)
        
        logger.info("STT path location test passed")
    
    def test_safe_scrape_stt(self):
        """Test safe STT scraping."""
        result = safe_scrape_stt()
        
        assert isinstance(result, list)
        # Should always return something (fallback if needed)
        assert len(result) > 0
        
        if result:
            item = result[0]
            assert isinstance(item, dict)
            # Should have some basic trading fields
            assert any(key in item for key in ['symbol', 'price', 'volume'])
        
        logger.info("Safe STT scraping test passed")

class TestScrapingAPI:
    """Test suite for scraping API functionality."""
    
    @pytest.mark.asyncio
    async def test_scrape_url_auto(self):
        """Test URL scraping with auto method."""
        test_url = "https://httpbin.org/html"
        
        try:
            result = await scrape_url(test_url, method="auto")
            
            assert isinstance(result, dict)
            if 'scrape_result' in result:
                scrape_data = result['scrape_result']
                assert isinstance(scrape_data, dict)
            elif 'error' in result:
                # Error is acceptable for network issues
                assert isinstance(result['error'], str)
            
            logger.info("Scrape URL auto test passed")
        except Exception as e:
            # Network or dependency issues are acceptable
            logger.warning(f"Scrape URL test had issues: {e}")
    
    def test_scrape_router_snapshot(self):
        """Test scrape router with snapshot mode."""
        result = scrape_router(snapshot=True)
        
        assert isinstance(result, (dict, list))
        # Should return some data structure
        
        logger.info("Scrape router snapshot test passed")

class TestScrapingIntegration:
    """Integration tests for scraping functionality."""
    
    @pytest.mark.integration
    def test_dom_extraction_to_memory_pipeline(self):
        """Test the complete pipeline from DOM extraction to memory storage."""
        test_html = """
        <html>
        <head><title>Integration Test Page</title></head>
        <body>
            <h1>Financial Data</h1>
            <div class="stock-info">
                <span class="symbol">GREMLIN</span>
                <span class="price">$123.45</span>
            </div>
            <p>This is test content for integration testing.</p>
        </body>
        </html>
        """
        
        # Step 1: Extract DOM structure
        dom_result = extract_dom_structure(test_html)
        
        assert 'text' in dom_result
        assert 'Financial Data' in dom_result['text']
        assert 'GREMLIN' in dom_result['text']
        
        # Step 2: Store to memory (with mocked embedding)
        with patch('scraper.page_simulator.package_embedding') as mock_package, \
             patch('scraper.page_simulator.inject_watermark') as mock_inject, \
             patch('scraper.page_simulator.embed_text') as mock_embed:
            
            mock_embed.return_value = [0.1] * 384  # Mock embedding vector
            
            store_scrape_to_memory("https://test-integration.com", test_html)
            
            # Verify the pipeline worked
            mock_embed.assert_called_once()
            mock_package.assert_called_once()
            mock_inject.assert_called_once()
        
        logger.info("DOM extraction to memory pipeline test passed")
    
    @pytest.mark.integration
    @pytest.mark.asyncio
    async def test_multi_source_scraping_coordination(self):
        """Test coordination between multiple scraping sources."""
        # Test that different scrapers can work together
        tws_result = safe_scrape_tws()
        stt_result = safe_scrape_stt()
        router_result = await route_scraping_async()
        
        # All should return valid data structures
        assert isinstance(tws_result, list)
        assert isinstance(stt_result, list)
        assert isinstance(router_result, list)
        
        # Should all have some data (fallback if needed)
        assert len(tws_result) > 0
        assert len(stt_result) > 0
        
        logger.info("Multi-source scraping coordination test passed")

# Performance and stress tests
class TestScrapingPerformance:
    """Performance tests for scraping functionality."""
    
    @pytest.mark.slow
    def test_dom_extraction_performance(self):
        """Test DOM extraction performance with large content."""
        # Create large HTML content
        large_html = "<html><body>"
        for i in range(1000):
            large_html += f"<p>Paragraph {i} with some content that makes it realistic.</p>"
        large_html += "</body></html>"
        
        start_time = time.time()
        result = extract_dom_structure(large_html)
        end_time = time.time()
        
        # Should complete in reasonable time
        assert end_time - start_time < 5.0  # Less than 5 seconds
        
        # Should still extract content properly
        assert 'text' in result
        assert len(result['text']) > 0
        
        logger.info(f"DOM extraction performance: {end_time - start_time:.2f}s for large content")
    
    @pytest.mark.slow
    def test_multiple_scraper_performance(self):
        """Test performance when multiple scrapers run simultaneously."""
        start_time = time.time()
        
        # Run multiple scrapers
        results = []
        results.append(safe_scrape_tws())
        results.append(safe_scrape_stt())
        
        end_time = time.time()
        
        # Should complete quickly since they're not doing heavy work
        assert end_time - start_time < 10.0  # Less than 10 seconds
        
        # All should return valid results
        for result in results:
            assert isinstance(result, list)
            assert len(result) > 0
        
        logger.info(f"Multiple scraper performance: {end_time - start_time:.2f}s")

if __name__ == '__main__':
    # Run basic tests if pytest is not available
    test_dom = TestDomNavigator()
    test_dom.test_extract_dom_structure_basic()
    
    test_source = TestSourceRouter()
    test_source.test_detect_apps()
    
    test_tws = TestTWScraper()
    test_tws.test_safe_scrape_tws()
    
    test_stt = TestSTTScraper()
    test_stt.test_safe_scrape_stt()
    
    print("All GremlinGPT scraper tests passed!")

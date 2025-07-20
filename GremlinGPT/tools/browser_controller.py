#!/usr/bin/env python3

"""
GremlinGPT Playwright System Controller
Provides browser automation and system control capabilities
"""

import asyncio
import json

import logging
import os
import sys
from typing import Dict, Any, List, Optional
from playwright.async_api import async_playwright, Browser, BrowserContext, Page
from datetime import datetime
from backend.globals import CFG, logger

class GremlinPlaywrightController:
    """Browser automation controller for GremlinGPT system management"""
    
    def __init__(self):
        self.playwright = None
        self.browser: Optional[Browser] = None
        self.context: Optional[BrowserContext] = None
        self.page: Optional[Page] = None
        self.base_url = "http://localhost:7777"
        
    async def initialize(self):
        """Initialize Playwright browser"""
        try:
            self.playwright = await async_playwright().start()
            self.browser = await self.playwright.chromium.launch(
                headless=False,
                args=['--no-sandbox', '--disable-dev-shm-usage']
            )
            self.context = await self.browser.new_context(
                viewport={'width': 1920, 'height': 1080}
            )
            self.page = await self.context.new_page()
            
            # Enable console logging
            self.page.on("console", self._handle_console)
            self.page.on("pageerror", self._handle_error)
            
            logger.info("Playwright browser initialized successfully")
            return True
            
        except Exception as e:
            logger.error(f"Failed to initialize Playwright: {e}")
            return False
    
    def _handle_console(self, msg):
        """Handle browser console messages"""
        logger.info(f"Browser Console [{msg.type}]: {msg.text}")
    
    def _handle_error(self, error):
        """Handle browser errors"""
        logger.error(f"Browser Error: {error}")
    
    async def navigate_to_dashboard(self):
        """Navigate to GremlinGPT dashboard"""
        if not self.page:
            raise RuntimeError("Browser page not initialized")
            
        try:
            await self.page.goto(f"{self.base_url}/dashboard")
            await self.page.wait_for_load_state("networkidle")
            logger.info("Navigated to GremlinGPT dashboard")
            return True
        except Exception as e:
            logger.error(f"Failed to navigate to dashboard: {e}")
            return False
    
    async def take_screenshot(self, filename: Optional[str] = None) -> str:
        """Take a screenshot of current page"""
        if not filename:
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            filename = f"gremlin_screenshot_{timestamp}.png"
        
        try:
            screenshot_path = os.path.join("screenshots", filename)
            os.makedirs("screenshots", exist_ok=True)
            
            await self.page.screenshot(path=screenshot_path, full_page=True)
            logger.info(f"Screenshot saved: {screenshot_path}")
            return screenshot_path
        except Exception as e:
            logger.error(f"Failed to take screenshot: {e}")
            return ""
    
    async def check_system_status(self) -> Dict[str, Any]:
        """Check GremlinGPT system status via dashboard"""
        try:
            await self.navigate_to_dashboard()
            
            # Wait for status elements to load
            await self.page.wait_for_selector(".status-indicator", timeout=10000)
            
            # Extract system status information
            status_data = await self.page.evaluate("""
                () => {
                    const statusElements = document.querySelectorAll('.status-indicator');
                    const statusText = document.querySelector('#systemStatus');
                    
                    let status = 'unknown';
                    for (const element of statusElements) {
                        if (element.classList.contains('status-running')) {
                            status = 'running';
                            break;
                        } else if (element.classList.contains('status-stopped')) {
                            status = 'stopped';
                            break;
                        } else if (element.classList.contains('status-starting')) {
                            status = 'starting';
                            break;
                        }
                    }
                    
                    return {
                        status: status,
                        statusText: statusText ? statusText.innerText : '',
                        timestamp: new Date().toISOString()
                    };
                }
            """)
            
            logger.info(f"System status: {status_data}")
            return status_data
            
        except Exception as e:
            logger.error(f"Failed to check system status: {e}")
            return {"status": "error", "error": str(e)}
    
    async def monitor_memory_usage(self) -> Dict[str, Any]:
        """Monitor memory system usage"""
        try:
            await self.page.goto(f"{self.base_url}/dashboard#memory")
            await self.page.wait_for_load_state("networkidle")
            
            # Extract memory metrics
            memory_data = await self.page.evaluate("""
                () => {
                    const memoryGraph = document.querySelector('#memoryGraph');
                    const memoryCards = document.querySelectorAll('.card[data-memory]');
                    
                    let metrics = {
                        total_embeddings: 0,
                        vector_dimensions: 0,
                        memory_usage: 'unknown'
                    };
                    
                    // Try to extract memory information from various elements
                    if (memoryGraph) {
                        const graphText = memoryGraph.innerText;
                        // Parse JSON or extract numbers from text
                        try {
                            const data = JSON.parse(graphText);
                            metrics.total_embeddings = data.nodes ? data.nodes.length : 0;
                        } catch (e) {
                            // Extract numbers from text
                            const numbers = graphText.match(/\\d+/g);
                            if (numbers) {
                                metrics.total_embeddings = parseInt(numbers[0]) || 0;
                            }
                        }
                    }
                    
                    return metrics;
                }
            """)
            
            logger.info(f"Memory usage: {memory_data}")
            return memory_data
            
        except Exception as e:
            logger.error(f"Failed to monitor memory usage: {e}")
            return {"error": str(e)}
    
    async def monitor_trading_signals(self) -> List[Dict[str, Any]]:
        """Monitor trading signals"""
        try:
            await self.page.goto(f"{self.base_url}/dashboard#trading")
            await self.page.wait_for_load_state("networkidle")
            
            # Extract trading signals
            signals = await self.page.evaluate("""
                () => {
                    const signalsContainer = document.querySelector('#signals');
                    const tradingCards = document.querySelectorAll('.card[data-trading]');
                    
                    let signals = [];
                    
                    if (signalsContainer) {
                        const signalElements = signalsContainer.querySelectorAll('div');
                        for (const element of signalElements) {
                            const text = element.innerText;
                            // Parse signal text like "AAPL $150.00 | Signal: BUY"
                            const match = text.match(/(\\w+)\\s+\\$(\\d+\\.\\d+).*Signal:\\s*(\\w+)/);
                            if (match) {
                                signals.push({
                                    symbol: match[1],
                                    price: parseFloat(match[2]),
                                    signal: match[3],
                                    timestamp: new Date().toISOString()
                                });
                            }
                        }
                    }
                    
                    return signals;
                }
            """)
            
            logger.info(f"Trading signals found: {len(signals)}")
            return signals
            
        except Exception as e:
            logger.error(f"Failed to monitor trading signals: {e}")
            return []
    
    async def trigger_system_action(self, action: str) -> bool:
        """Trigger system actions via dashboard buttons"""
        try:
            await self.navigate_to_dashboard()
            
            # Define action button selectors
            action_selectors = {
                "start_mutation": "button[onclick='triggerMutation()']",
                "start_feedback": "button[onclick='startFeedback()']",
                "schedule_retrain": "button[onclick='scheduleRetrain()']",
                "execute_python": "button[onclick='executePython()']",
                "refresh_status": "button[onclick='refreshStatus()']"
            }
            
            if action not in action_selectors:
                logger.error(f"Unknown action: {action}")
                return False
            
            # Click the action button
            selector = action_selectors[action]
            await self.page.click(selector)
            
            # Wait for response
            await self.page.wait_for_timeout(2000)
            
            logger.info(f"Triggered action: {action}")
            return True
            
        except Exception as e:
            logger.error(f"Failed to trigger action {action}: {e}")
            return False
    
    async def automated_health_check(self) -> Dict[str, Any]:
        """Perform automated health check of the entire system"""
        health_report = {
            "timestamp": datetime.now().isoformat(),
            "overall_status": "unknown",
            "components": {}
        }
        
        try:
            # Check system status
            system_status = await self.check_system_status()
            health_report["components"]["system"] = system_status
            
            # Check memory system
            memory_status = await self.monitor_memory_usage()
            health_report["components"]["memory"] = memory_status
            
            # Check trading system
            trading_signals = await self.monitor_trading_signals()
            health_report["components"]["trading"] = {
                "active_signals": len(trading_signals),
                "signals": trading_signals[:5]  # First 5 signals
            }
            
            # Take screenshot for visual verification
            screenshot_path = await self.take_screenshot("health_check.png")
            health_report["screenshot"] = screenshot_path
            
            # Determine overall status
            if system_status.get("status") == "running":
                health_report["overall_status"] = "healthy"
            elif system_status.get("status") == "starting":
                health_report["overall_status"] = "starting"
            else:
                health_report["overall_status"] = "unhealthy"
            
            logger.info(f"Health check completed: {health_report['overall_status']}")
            return health_report
            
        except Exception as e:
            logger.error(f"Health check failed: {e}")
            health_report["overall_status"] = "error"
            health_report["error"] = str(e)
            return health_report
    
    async def cleanup(self):
        """Cleanup browser resources"""
        try:
            if self.context:
                await self.context.close()
            if self.browser:
                await self.browser.close()
            if self.playwright:
                await self.playwright.stop()
            logger.info("Browser resources cleaned up")
        except Exception as e:
            logger.error(f"Error during cleanup: {e}")

class GremlinAutomationScheduler:
    """Scheduler for automated system monitoring and control"""
    
    def __init__(self, controller: GremlinPlaywrightController):
        self.controller = controller
        self.monitoring_active = False
    
    async def start_monitoring(self, interval_minutes: int = 5):
        """Start automated monitoring"""
        self.monitoring_active = True
        logger.info(f"Starting automated monitoring (interval: {interval_minutes} minutes)")
        
        while self.monitoring_active:
            try:
                # Perform health check
                health_report = await self.controller.automated_health_check()
                
                # Save health report
                self._save_health_report(health_report)
                
                # Check for issues and take corrective actions
                await self._handle_health_issues(health_report)
                
                # Wait for next interval
                await asyncio.sleep(interval_minutes * 60)
                
            except Exception as e:
                logger.error(f"Error in monitoring cycle: {e}")
                await asyncio.sleep(60)  # Wait 1 minute before retrying
    
    def stop_monitoring(self):
        """Stop automated monitoring"""
        self.monitoring_active = False
        logger.info("Stopped automated monitoring")
    
    def _save_health_report(self, report: Dict[str, Any]):
        """Save health report to file"""
        try:
            reports_dir = "health_reports"
            os.makedirs(reports_dir, exist_ok=True)
            
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            filename = f"health_report_{timestamp}.json"
            filepath = os.path.join(reports_dir, filename)
            
            with open(filepath, 'w') as f:
                json.dump(report, f, indent=2)
            
            logger.info(f"Health report saved: {filepath}")
            
        except Exception as e:
            logger.error(f"Failed to save health report: {e}")
    
    async def _handle_health_issues(self, report: Dict[str, Any]):
        """Handle detected health issues"""
        overall_status = report.get("overall_status")
        
        if overall_status == "unhealthy":
            logger.warning("System unhealthy - attempting corrective actions")
            
            # Try to restart system components
            await self.controller.trigger_system_action("refresh_status")
            
        elif overall_status == "error":
            logger.error("System error detected - taking screenshot for debugging")
            await self.controller.take_screenshot("error_debug.png")

async def main():
    """Main function for CLI usage"""
    controller = GremlinPlaywrightController()
    
    try:
        # Initialize browser
        if not await controller.initialize():
            logger.error("Failed to initialize browser")
            return 1
        
        # Command line arguments
        if len(sys.argv) > 1:
            command = sys.argv[1]
            
            if command == "health-check":
                report = await controller.automated_health_check()
                print(json.dumps(report, indent=2))
                
            elif command == "monitor":
                interval = int(sys.argv[2]) if len(sys.argv) > 2 else 5
                scheduler = GremlinAutomationScheduler(controller)
                await scheduler.start_monitoring(interval)
                
            elif command == "screenshot":
                path = await controller.take_screenshot()
                print(f"Screenshot saved: {path}")
                
            elif command == "status":
                status = await controller.check_system_status()
                print(json.dumps(status, indent=2))
                
            else:
                print(f"Unknown command: {command}")
                print("Available commands: health-check, monitor, screenshot, status")
                return 1
        else:
            # Interactive demo
            await controller.navigate_to_dashboard()
            await controller.take_screenshot("demo.png")
            print("GremlinGPT Browser Controller Demo")
            print("Screenshot saved as demo.png")
            
            # Wait for user input
            input("Press Enter to perform health check...")
            report = await controller.automated_health_check()
            print("Health Check Report:")
            print(json.dumps(report, indent=2))
        
    except KeyboardInterrupt:
        logger.info("Interrupted by user")
    except Exception as e:
        logger.error(f"Unexpected error: {e}")
        return 1
    finally:
        await controller.cleanup()
    
    return 0

if __name__ == "__main__":
    asyncio.run(main())

#!/usr/bin/env python3

# ─────────────────────────────────────────────────────────────
# ⚠️ GremlinGPT Fair Use Only | Commercial Use Requires License
# Built under the GremlinGPT Dual License v1.0
# © 2025 StatikFintechLLC / AscendAI Project
# Contact: ascend.gremlin@gmail.com
# ─────────────────────────────────────────────────────────────

# GremlinGPT v1.0.3 :: Unified System Startup - Living AI Ecosystem

from backend.globals import CFG, logger, resolve_path, DATA_DIR, MEM
from backend.api.api_endpoints import *
from backend.router import route_task


class GremlinGPTEcosystemLauncher:
    """
    Unified GremlinGPT Ecosystem Launcher
    
    This launches the complete living, growing, self-improving AI ecosystem
    that integrates all capabilities into a unified autonomous system.
    """
    
    def __init__(self):
        self.unified_system = None
        self.shutdown_requested = False
        self.startup_time = datetime.now(timezone.utc)
        
        # Setup signal handlers for graceful shutdown
        signal.signal(signal.SIGINT, self._signal_handler)
        signal.signal(signal.SIGTERM, self._signal_handler)
        
        logger.info("[ECOSYSTEM_LAUNCHER] Launcher initialized")
    
    def _signal_handler(self, signum, frame):
        """Handle shutdown signals"""
        logger.info(f"[ECOSYSTEM_LAUNCHER] Received signal {signum}, initiating graceful shutdown...")
        self.shutdown_requested = True
    
    async def launch_ecosystem(self):
        """Launch the complete GremlinGPT ecosystem"""
        try:
            logger.info("=" * 80)
            logger.info("🧠 GREMLINGPT UNIFIED ECOSYSTEM STARTUP")
            logger.info("Living, Growing, Self-Improving AI System")
            logger.info("=" * 80)
            
            # Phase 1: Initialize unified system
            logger.info("[PHASE 1] Initializing unified intelligence system...")
            self.unified_system = await initialize_gremlin_ecosystem()
            
            if not self.unified_system:
                raise RuntimeError("Failed to initialize unified system")
            
            logger.success("[PHASE 1] ✅ Unified system initialized")
            
            # Phase 2: System health check
            logger.info("[PHASE 2] Performing system health check...")
            status = await self.unified_system.get_system_status()
            
            if self._validate_system_health(status):
                logger.success("[PHASE 2] ✅ System health check passed")
            else:
                logger.warning("[PHASE 2] ⚠️ System health check issues detected")
            
            # Phase 3: Start core loops
            logger.info("[PHASE 3] Starting core execution loops...")
            await self._start_core_loops()
            logger.success("[PHASE 3] ✅ Core loops active")
            
            # Phase 4: Launch test workflows
            if CFG.get("unified_system", {}).get("run_startup_tests", True):
                logger.info("[PHASE 4] Running startup validation workflows...")
                await self._run_startup_tests()
                logger.success("[PHASE 4] ✅ Startup tests completed")
            
            # Phase 5: System ready
            logger.info("=" * 80)
            logger.success("🚀 GREMLINGPT ECOSYSTEM FULLY OPERATIONAL")
            logger.info("System Status: AUTONOMOUS & SELF-IMPROVING")
            logger.info(f"Startup Time: {datetime.now(timezone.utc) - self.startup_time}")
            logger.info("=" * 80)
            
            log_event("ecosystem", "startup_complete", {
                "startup_time": (datetime.now(timezone.utc) - self.startup_time).total_seconds(),
                "system_components": self._get_component_summary(status),
                "ecosystem_status": "operational"
            })
            
            # Keep system running
            await self._monitor_ecosystem()
            
        except Exception as e:
            logger.error(f"[ECOSYSTEM_LAUNCHER] Startup failed: {e}")
            await self._emergency_shutdown()
            raise
    
    def _validate_system_health(self, status: dict) -> bool:
        """Validate system health from status"""
        try:
            components = status.get("components", {})
            
            # Check orchestrator
            orchestrator_active = components.get("orchestrator", {}).get("active", False)
            
            # Check coordinator
            coordinator_active = components.get("coordinator", {}).get("active", False)
            
            # Check agents
            agents = components.get("agents", {})
            agents_active = sum(1 for agent_info in agents.values() if agent_info.get("active", False))
            
            # Check integration
            integration = status.get("integration", {})
            fsm_integration = integration.get("fsm_integration_active", False)
            
            health_score = 0
            if orchestrator_active:
                health_score += 25
            if coordinator_active:
                health_score += 25
            if agents_active >= 3:  # All 3 specialized agents
                health_score += 25
            if fsm_integration:
                health_score += 25
            
            logger.info(f"[HEALTH_CHECK] System health score: {health_score}/100")
            
            return health_score >= 75
            
        except Exception as e:
            logger.error(f"[HEALTH_CHECK] Health validation failed: {e}")
            return False
    
    def _get_component_summary(self, status: dict) -> dict:
        """Get summary of system components"""
        try:
            components = status.get("components", {})
            
            return {
                "orchestrator": components.get("orchestrator", {}).get("active", False),
                "coordinator": components.get("coordinator", {}).get("active", False),
                "agents_count": len(components.get("agents", {})),
                "fsm_active": components.get("fsm", {}).get("state", "unknown") != "ERROR",
                "integration_active": status.get("integration", {}).get("fsm_integration_active", False)
            }
            
        except Exception as e:
            logger.error(f"[COMPONENT_SUMMARY] Failed to generate summary: {e}")
            return {}
    
    async def _start_core_loops(self):
        """Start core execution loops"""
        try:
            # The FSM loop is already integrated via the unified system
            # Additional loops can be started here if needed
            
            # Start monitoring loop
            asyncio.create_task(self._monitoring_loop())
            
            logger.info("[CORE_LOOPS] Monitoring loop started")
            
        except Exception as e:
            logger.error(f"[CORE_LOOPS] Failed to start core loops: {e}")
            raise
    
    async def _monitoring_loop(self):
        """Background monitoring loop"""
        try:
            while not self.shutdown_requested:
                await asyncio.sleep(60)  # Monitor every minute
                
                if self.unified_system:
                    status = await self.unified_system.get_system_status()
                    
                    # Log system metrics
                    log_event("ecosystem", "health_monitor", {
                        "timestamp": datetime.now(timezone.utc).isoformat(),
                        "system_health": self._calculate_health_score(status),
                        "active_workflows": status.get("components", {}).get("coordinator", {}).get("status", {}).get("active_workflows", 0)
                    })
        
        except Exception as e:
            logger.error(f"[MONITORING_LOOP] Monitoring error: {e}")
    
    def _calculate_health_score(self, status: dict) -> float:
        """Calculate overall system health score"""
        try:
            components = status.get("components", {})
            integration = status.get("integration", {})
            
            score = 0.0
            max_score = 0.0
            
            # Orchestrator health
            if components.get("orchestrator", {}).get("active", False):
                score += 20
            max_score += 20
            
            # Coordinator health
            if components.get("coordinator", {}).get("active", False):
                score += 20
            max_score += 20
            
            # Agent health
            agents = components.get("agents", {})
            active_agents = sum(1 for agent_info in agents.values() if agent_info.get("active", False))
            agent_score = (active_agents / max(1, len(agents))) * 20
            score += agent_score
            max_score += 20
            
            # FSM health
            fsm_state = components.get("fsm", {}).get("state", "ERROR")
            if fsm_state in ["IDLE", "RUNNING"]:
                score += 20
            max_score += 20
            
            # Integration health
            if integration.get("fsm_integration_active", False):
                score += 20
            max_score += 20
            
            return score / max_score if max_score > 0 else 0.0
            
        except Exception as e:
            logger.error(f"[HEALTH_SCORE] Calculation failed: {e}")
            return 0.0
    
    async def _run_startup_tests(self):
        """Run startup validation tests"""
        try:
            test_results = {}
            
            # Test 1: Simple workflow execution
            logger.info("[STARTUP_TEST] Testing workflow execution...")
            
            if self.unified_system:
                test_workflow_result = await self.unified_system.execute_unified_workflow(
                    "comprehensive_market_analysis",
                    {
                        "symbols": ["TEST"],
                        "analysis_depth": "basic"
                    }
                )
            else:
                test_workflow_result = {"status": "FAILED", "error": "Unified system not available"}
            
            test_results["workflow_execution"] = {
                "status": test_workflow_result.get("status", "unknown"),
                "success": test_workflow_result.get("status") == "COMPLETED"
            }
            
            # Test 2: Agent coordination
            logger.info("[STARTUP_TEST] Testing agent coordination...")
            
            if self.unified_system and self.unified_system.coordinator:
                coordinator_status = await self.unified_system.coordinator.get_coordination_status()
            else:
                coordinator_status = {"registered_agents": []}
                
            test_results["agent_coordination"] = {
                "agents_registered": len(coordinator_status.get("registered_agents", [])),
                "success": len(coordinator_status.get("registered_agents", [])) >= 3
            }
            
            # Test 3: System integration
            logger.info("[STARTUP_TEST] Testing system integration...")
            
            if self.unified_system:
                fsm_integration = getattr(self.unified_system, 'fsm_integration_active', False)
                async_thread = getattr(self.unified_system, 'async_thread', None)
                async_active = bool(async_thread and async_thread.is_alive())
            else:
                fsm_integration = False
                async_active = False
            
            test_results["system_integration"] = {
                "fsm_integration": fsm_integration,
                "async_thread": async_active,
                "success": fsm_integration
            }
            
            # Log test results
            log_event("ecosystem", "startup_tests", test_results)
            
            # Summary
            all_tests_passed = all(test.get("success", False) for test in test_results.values())
            
            if all_tests_passed:
                logger.success("[STARTUP_TEST] ✅ All tests passed")
            else:
                logger.warning("[STARTUP_TEST] ⚠️ Some tests failed")
                for test_name, result in test_results.items():
                    if not result.get("success", False):
                        logger.warning(f"[STARTUP_TEST] Failed: {test_name}")
            
        except Exception as e:
            logger.error(f"[STARTUP_TEST] Test execution failed: {e}")
    
    async def _monitor_ecosystem(self):
        """Monitor the ecosystem and keep it running"""
        try:
            logger.info("[ECOSYSTEM_MONITOR] Monitoring started - system will run until interrupted")
            
            while not self.shutdown_requested:
                await asyncio.sleep(5)  # Check every 5 seconds
                
                # Perform basic health checks
                if self.unified_system:
                    # Check if system is still healthy
                    status = await self.unified_system.get_system_status()
                    health_score = self._calculate_health_score(status)
                    
                    if health_score < 0.5:
                        logger.warning(f"[ECOSYSTEM_MONITOR] Low health score: {health_score:.2f}")
                        
                        # Log degraded performance
                        log_event("ecosystem", "health_degraded", {
                            "health_score": health_score,
                            "timestamp": datetime.now(timezone.utc).isoformat()
                        }, status="warning")
                        
                        # Could trigger recovery workflows here
            
            logger.info("[ECOSYSTEM_MONITOR] Shutdown requested, stopping monitoring")
            
        except Exception as e:
            logger.error(f"[ECOSYSTEM_MONITOR] Monitoring error: {e}")
    
    async def _emergency_shutdown(self):
        """Perform emergency shutdown"""
        try:
            logger.warning("[EMERGENCY_SHUTDOWN] Initiating emergency shutdown...")
            
            if self.unified_system:
                await self.unified_system.shutdown_unified_system()
            
            logger.warning("[EMERGENCY_SHUTDOWN] Emergency shutdown completed")
            
        except Exception as e:
            logger.error(f"[EMERGENCY_SHUTDOWN] Shutdown error: {e}")
    
    async def graceful_shutdown(self):
        """Perform graceful shutdown"""
        try:
            logger.info("[GRACEFUL_SHUTDOWN] Initiating graceful shutdown...")
            
            # Log shutdown event
            uptime = datetime.now(timezone.utc) - self.startup_time
            log_event("ecosystem", "graceful_shutdown", {
                "uptime_seconds": uptime.total_seconds(),
                "shutdown_time": datetime.now(timezone.utc).isoformat()
            })
            
            # Shutdown unified system
            if self.unified_system:
                await self.unified_system.shutdown_unified_system()
            
            logger.info("[GRACEFUL_SHUTDOWN] ✅ Graceful shutdown completed")
            
        except Exception as e:
            logger.error(f"[GRACEFUL_SHUTDOWN] Shutdown error: {e}")


async def main():
    """Main entry point for the unified ecosystem"""
    launcher = GremlinGPTEcosystemLauncher()
    
    try:
        await launcher.launch_ecosystem()
    except KeyboardInterrupt:
        logger.info("Received keyboard interrupt")
    except Exception as e:
        logger.error(f"Ecosystem launch failed: {e}")
    finally:
        await launcher.graceful_shutdown()


if __name__ == "__main__":
    print("🧠 GremlinGPT Unified Ecosystem")
    print("Living, Growing, Self-Improving AI System")
    print("=" * 50)
    
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print("\nShutdown completed.")
    except Exception as e:
        print(f"Fatal error: {e}")
        sys.exit(1)

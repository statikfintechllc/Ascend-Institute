#!/usr/bin/env python3

# ─────────────────────────────────────────────────────────────
# ⚠️ GremlinGPT Fair Use Only | Commercial Use Requires License
# Built under the GremlinGPT Dual License v1.0
# © 2025 StatikFintechLLC / AscendAI Project
# Contact: ascend.gremlin@gmail.com
# ─────────────────────────────────────────────────────────────

# GremlinGPT v1.0.3 :: System Integration Module - Unified Architecture Bridge

import asyncio
import threading
from datetime import datetime, timezone
from pathlib import Path
import sys
import json
from typing import Dict, List, Any, Optional
import logging

# Add project root to path for imports
project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root))

from backend.globals import CFG, LOOP
from utils.logging_config import setup_module_logger
from memory.log_history import log_event
from agent_core.task_queue import enqueue_task, TaskQueue

# Import new unified system components
from core.orchestrator import get_global_orchestrator
from agents.agent_coordinator import get_agent_coordinator
from agents.data_analyst_agent import get_data_analyst_agent
from agents.trading_strategist_agent import get_trading_strategist_agent
from agents.learning_agent import get_learning_agent

logger = setup_module_logger("core", "integration")


class GremlinGPTUnifiedSystem:
    """
    Unified GremlinGPT System Integration
    
    This class bridges the new autonomous agent system with the existing
    FSM/loop architecture, creating a seamless unified ecosystem where
    traditional task execution and advanced agent collaboration coexist.
    """
    
    def __init__(self):
        self.system_id = f"gremlin_unified_{datetime.now().strftime('%Y%m%d_%H%M%S')}"
        self.orchestrator = None
        self.coordinator = None
        self.agents = {}
        self.fsm_integration_active = False
        self.async_loop = None
        self.async_thread = None
        
        # Integration configuration
        self.config = CFG.get("unified_system", {
            "enable_agent_workflows": True,
            "auto_workflow_triggers": True,
            "fsm_agent_coordination": True,
            "intelligent_task_routing": True,
            "learning_integration": True,
            "performance_monitoring": True
        })
        
        self.integration_lock = threading.Lock()
        self.workflow_triggers = []
        self.task_router_active = False
        
        logger.info(f"[UNIFIED_SYSTEM] Initialized system: {self.system_id}")
    
    async def initialize_unified_system(self):
        """Initialize the complete unified system"""
        try:
            logger.info("[UNIFIED_SYSTEM] Starting system initialization...")
            
            # Step 1: Initialize global orchestrator
            self.orchestrator = get_global_orchestrator()
            # Orchestrator initializes automatically
            
            # Step 2: Initialize agent coordinator and specialized agents
            self.coordinator = get_agent_coordinator()
            await self.coordinator.initialize_agents()
            
            # Step 3: Store agent references
            self.agents = {
                "data_analyst": get_data_analyst_agent(),
                "trading_strategist": get_trading_strategist_agent(),
                "learning_agent": get_learning_agent()
            }
            
            # Step 4: Register existing modules with orchestrator
            await self._register_existing_modules()
            
            # Step 5: Set up FSM integration
            await self._setup_fsm_integration()
            
            # Step 6: Configure workflow triggers
            await self._setup_workflow_triggers()
            
            # Step 7: Start intelligent task routing
            if self.config["intelligent_task_routing"]:
                await self._start_intelligent_task_routing()
            
            logger.success("[UNIFIED_SYSTEM] System initialization completed successfully")
            log_event("unified_system", "initialization_complete", {
                "system_id": self.system_id,
                "agents_active": len(self.agents),
                "orchestrator_active": bool(self.orchestrator),
                "coordinator_active": bool(self.coordinator)
            })
            
        except Exception as e:
            logger.error(f"[UNIFIED_SYSTEM] Initialization failed: {e}")
            raise
    
    async def _register_existing_modules(self):
        """Register existing GremlinGPT modules with the orchestrator"""
        try:
            # Register core modules
            existing_modules = [
                {
                    "name": "fsm_core",
                    "module": None,  # FSM is function-based, not class-based
                    "capabilities": ["task_execution", "loop_control", "state_management"]
                },
                {
                    "name": "task_queue",
                    "module": None,  # Task queue is global instance
                    "capabilities": ["task_queuing", "priority_management", "scheduling"]
                },
                {
                    "name": "scraper",
                    "module": None,
                    "capabilities": ["data_collection", "web_scraping", "content_extraction"]
                },
                {
                    "name": "nlp_engine",
                    "module": None,
                    "capabilities": ["text_processing", "semantic_analysis", "language_understanding"]
                },
                {
                    "name": "trading_core",
                    "module": None,
                    "capabilities": ["signal_generation", "market_analysis", "trading_execution"]
                },
                {
                    "name": "memory_system",
                    "module": None,
                    "capabilities": ["data_storage", "vector_embeddings", "knowledge_retention"]
                }
            ]
            
            for module_info in existing_modules:
                if self.orchestrator:
                    self.orchestrator.register_module(
                        module_info["name"],
                        module_info["module"],
                        module_info["capabilities"]
                    )
            
            logger.info(f"[UNIFIED_SYSTEM] Registered {len(existing_modules)} existing modules")
            
        except Exception as e:
            logger.error(f"[UNIFIED_SYSTEM] Module registration failed: {e}")
            raise
    
    async def _setup_fsm_integration(self):
        """Set up integration with existing FSM system"""
        try:
            # Import FSM functions
            from agent_core import fsm
            
            # Create FSM integration hooks
            self.original_fsm_loop = fsm.fsm_loop
            self.original_execute_tool = None
            
            # Try to import execute_tool
            try:
                from executors.tool_executor import execute_tool
                self.original_execute_tool = execute_tool
            except ImportError:
                logger.warning("[UNIFIED_SYSTEM] Could not import execute_tool for integration")
            
            # Override FSM loop with integrated version
            fsm.fsm_loop = self._integrated_fsm_loop
            
            self.fsm_integration_active = True
            logger.info("[UNIFIED_SYSTEM] FSM integration configured")
            
        except Exception as e:
            logger.error(f"[UNIFIED_SYSTEM] FSM integration setup failed: {e}")
            raise
    
    def _integrated_fsm_loop(self):
        """Integrated FSM loop that includes agent coordination"""
        try:
            # Check for agent workflow triggers
            if self.config["auto_workflow_triggers"]:
                self._check_and_execute_workflows()
            
            # Execute original FSM loop
            result = self.original_fsm_loop()
            
            # Post-processing with learning integration
            if self.config["learning_integration"]:
                self._update_learning_from_fsm_cycle()
            
            return result
            
        except Exception as e:
            logger.error(f"[UNIFIED_SYSTEM] Integrated FSM loop error: {e}")
            # Fallback to original FSM loop
            return self.original_fsm_loop()
    
    def _check_and_execute_workflows(self):
        """Check for conditions that should trigger agent workflows"""
        try:
            current_time = datetime.now(timezone.utc)
            
            # Check for workflow triggers
            for trigger in self.workflow_triggers:
                if self._should_trigger_workflow(trigger, current_time):
                    # Execute workflow asynchronously
                    if self.async_loop and not self.async_loop.is_closed():
                        asyncio.run_coroutine_threadsafe(
                            self._execute_triggered_workflow(trigger),
                            self.async_loop
                        )
                    else:
                        logger.warning("[UNIFIED_SYSTEM] Async loop not available for workflow execution")
            
        except Exception as e:
            logger.error(f"[UNIFIED_SYSTEM] Workflow trigger check failed: {e}")
    
    def _should_trigger_workflow(self, trigger: Dict[str, Any], current_time: datetime) -> bool:
        """Determine if a workflow should be triggered"""
        trigger_type = trigger.get("type", "")
        last_triggered = trigger.get("last_triggered")
        interval_minutes = trigger.get("interval_minutes", 60)
        
        # Time-based trigger
        if trigger_type == "periodic":
            if not last_triggered:
                return True
            
            time_diff = (current_time - datetime.fromisoformat(last_triggered)).total_seconds() / 60
            return time_diff >= interval_minutes
        
        # Task queue based trigger
        elif trigger_type == "queue_based":
            from agent_core.fsm import task_queue
            queue_length = sum(len(task_queue.task_queue[level]) for level in ["high", "normal", "low"])
            threshold = trigger.get("queue_threshold", 10)
            return queue_length >= threshold
        
        # Performance based trigger
        elif trigger_type == "performance":
            # This would check performance metrics and trigger optimization workflows
            return self._check_performance_trigger(trigger)
        
        return False
    
    def _check_performance_trigger(self, trigger: Dict[str, Any]) -> bool:
        """Check if performance metrics warrant triggering a workflow"""
        try:
            # Simulate performance check (in real implementation, would check actual metrics)
            performance_threshold = trigger.get("performance_threshold", 0.7)
            
            # Get current system performance (simplified)
            system_health = 0.85  # This would be calculated from actual metrics
            
            return system_health < performance_threshold
            
        except Exception as e:
            logger.error(f"[UNIFIED_SYSTEM] Performance trigger check failed: {e}")
            return False
    
    async def _execute_triggered_workflow(self, trigger: Dict[str, Any]):
        """Execute a workflow triggered by system conditions"""
        try:
            workflow_type = trigger.get("workflow_type", "general")
            workflow_data = trigger.get("data", {})
            
            workflow_definition = {
                "type": workflow_type,
                "data": workflow_data,
                "trigger_source": "auto_trigger",
                "trigger_config": trigger
            }
            
            logger.info(f"[UNIFIED_SYSTEM] Executing triggered workflow: {workflow_type}")
            
            if self.coordinator:
                result = await self.coordinator.execute_collaborative_workflow(workflow_definition)
            else:
                result = {"error": "Coordinator not available"}
            
            # Update trigger timestamp
            trigger["last_triggered"] = datetime.now(timezone.utc).isoformat()
            
            logger.info(f"[UNIFIED_SYSTEM] Triggered workflow completed: {result.get('status', 'unknown')}")
            
        except Exception as e:
            logger.error(f"[UNIFIED_SYSTEM] Triggered workflow execution failed: {e}")
    
    def _update_learning_from_fsm_cycle(self):
        """Update learning system with FSM cycle information"""
        try:
            if not self.async_loop or self.async_loop.is_closed():
                return
            
            # Create learning update task
            learning_task = {
                "type": "monitor_performance",
                "module_name": "fsm_core",
                "metrics": {
                    "cycle_completed": 1,
                    "timestamp": datetime.now(timezone.utc).isoformat()
                }
            }
            
            # Execute asynchronously
            asyncio.run_coroutine_threadsafe(
                self.agents["learning_agent"].handle_task(learning_task),
                self.async_loop
            )
            
        except Exception as e:
            logger.error(f"[UNIFIED_SYSTEM] Learning update from FSM failed: {e}")
    
    async def _setup_workflow_triggers(self):
        """Set up automatic workflow triggers"""
        try:
            self.workflow_triggers = [
                {
                    "type": "periodic",
                    "workflow_type": "comprehensive_market_analysis",
                    "interval_minutes": 30,
                    "data": {
                        "symbols": ["AAPL", "GOOGL", "MSFT"],
                        "analysis_depth": "standard"
                    },
                    "last_triggered": None
                },
                {
                    "type": "periodic",
                    "workflow_type": "adaptive_learning_cycle",
                    "interval_minutes": 60,
                    "data": {
                        "focus": "performance_improvement",
                        "data_sources": ["trading_core", "scraper", "nlp_engine"]
                    },
                    "last_triggered": None
                },
                {
                    "type": "performance",
                    "workflow_type": "performance_optimization",
                    "performance_threshold": 0.7,
                    "data": {
                        "modules": ["trading_core", "scraper"],
                        "goals": ["improve_accuracy", "reduce_latency"]
                    },
                    "last_triggered": None
                }
            ]
            
            logger.info(f"[UNIFIED_SYSTEM] Configured {len(self.workflow_triggers)} workflow triggers")
            
        except Exception as e:
            logger.error(f"[UNIFIED_SYSTEM] Workflow trigger setup failed: {e}")
    
    async def _start_intelligent_task_routing(self):
        """Start intelligent task routing system"""
        try:
            # This would monitor the task queue and route appropriate tasks to agents
            self.task_router_active = True
            
            # In a full implementation, this would start a background task
            # that monitors the task queue and routes certain tasks to specialized agents
            
            logger.info("[UNIFIED_SYSTEM] Intelligent task routing activated")
            
        except Exception as e:
            logger.error(f"[UNIFIED_SYSTEM] Task routing startup failed: {e}")
    
    def start_async_integration(self):
        """Start async integration thread for agent coordination"""
        try:
            def run_async_loop():
                self.async_loop = asyncio.new_event_loop()
                asyncio.set_event_loop(self.async_loop)
                
                try:
                    # Keep the loop running
                    self.async_loop.run_forever()
                except Exception as e:
                    logger.error(f"[UNIFIED_SYSTEM] Async loop error: {e}")
                finally:
                    self.async_loop.close()
            
            self.async_thread = threading.Thread(target=run_async_loop, daemon=True)
            self.async_thread.start()
            
            logger.info("[UNIFIED_SYSTEM] Async integration thread started")
            
        except Exception as e:
            logger.error(f"[UNIFIED_SYSTEM] Async integration startup failed: {e}")
    
    async def execute_unified_workflow(self, workflow_type: str, data: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
        """Execute a unified workflow combining FSM tasks and agent collaboration"""
        workflow_definition = {
            "type": workflow_type,
            "data": data or {},
            "source": "unified_system"
        }
        
        if self.coordinator:
            return await self.coordinator.execute_collaborative_workflow(workflow_definition)
        else:
            return {"error": "Coordinator not available"}
    
    def inject_agent_task_to_fsm(self, agent_task: Dict[str, Any]) -> bool:
        """Inject an agent-generated task into the FSM task queue"""
        try:
            # Convert agent task to FSM-compatible format
            fsm_task = self._convert_agent_task_to_fsm(agent_task)
            
            # Inject into task queue
            enqueue_task(fsm_task)
            
            logger.debug(f"[UNIFIED_SYSTEM] Injected agent task to FSM: {fsm_task.get('type', 'unknown')}")
            return True
            
        except Exception as e:
            logger.error(f"[UNIFIED_SYSTEM] Agent task injection failed: {e}")
            return False
    
    def _convert_agent_task_to_fsm(self, agent_task: Dict[str, Any]) -> Dict[str, Any]:
        """Convert agent task format to FSM-compatible format"""
        task_type = agent_task.get("type", "general")
        
        # Map agent task types to FSM task types
        task_mapping = {
            "analyze_data": "nlp",
            "generate_signals": "signal_scan",
            "scrape_data": "scrape",
            "optimize_portfolio": "trading_analysis"
        }
        
        fsm_task_type = task_mapping.get(task_type, task_type)
        
        fsm_task = {
            "type": fsm_task_type,
            "source": "agent_system",
            "agent_data": agent_task,
            "priority": "normal"
        }
        
        # Add specific fields based on task type
        if fsm_task_type == "nlp":
            fsm_task["text"] = agent_task.get("content", "")
        elif fsm_task_type == "scrape":
            fsm_task["url"] = agent_task.get("url", "")
        
        return fsm_task
    
    async def get_system_status(self) -> Dict[str, Any]:
        """Get comprehensive system status"""
        try:
            # Get orchestrator status
            if self.orchestrator:
                orchestrator_status = self.orchestrator.get_module_status()
            else:
                orchestrator_status = {}
            
            # Get coordinator status
            coordinator_status = await self.coordinator.get_coordination_status() if self.coordinator else {}
            
            # Get FSM status
            try:
                from agent_core.fsm import get_fsm_status
                fsm_status = get_fsm_status()
            except Exception:
                fsm_status = {"error": "FSM status unavailable"}
            
            # Compile comprehensive status
            system_status = {
                "system_id": self.system_id,
                "unified_system_active": True,
                "components": {
                    "orchestrator": {
                        "active": bool(self.orchestrator),
                        "status": orchestrator_status
                    },
                    "coordinator": {
                        "active": bool(self.coordinator),
                        "status": coordinator_status
                    },
                    "fsm": fsm_status,
                    "agents": {
                        agent_name: {"active": bool(agent), "type": type(agent).__name__}
                        for agent_name, agent in self.agents.items()
                    }
                },
                "integration": {
                    "fsm_integration_active": self.fsm_integration_active,
                    "task_router_active": self.task_router_active,
                    "async_thread_active": bool(self.async_thread and self.async_thread.is_alive()),
                    "workflow_triggers": len(self.workflow_triggers)
                },
                "config": self.config
            }
            
            return system_status
            
        except Exception as e:
            logger.error(f"[UNIFIED_SYSTEM] Status collection failed: {e}")
            return {"error": str(e)}
    
    async def shutdown_unified_system(self):
        """Gracefully shutdown the unified system"""
        try:
            logger.info("[UNIFIED_SYSTEM] Starting graceful shutdown...")
            
            # Stop workflow triggers
            self.workflow_triggers.clear()
            
            # Stop async loop
            if self.async_loop and not self.async_loop.is_closed():
                self.async_loop.call_soon_threadsafe(self.async_loop.stop)
            
            # Wait for async thread to finish
            if self.async_thread and self.async_thread.is_alive():
                self.async_thread.join(timeout=5)
            
            # Restore original FSM loop if modified
            if self.fsm_integration_active and hasattr(self, 'original_fsm_loop'):
                try:
                    from agent_core import fsm
                    fsm.fsm_loop = self.original_fsm_loop
                except Exception as e:
                    logger.error(f"[UNIFIED_SYSTEM] Failed to restore original FSM loop: {e}")
            
            logger.info("[UNIFIED_SYSTEM] Shutdown completed")
            
        except Exception as e:
            logger.error(f"[UNIFIED_SYSTEM] Shutdown error: {e}")


# Global instance
_unified_system = None


def get_unified_system() -> GremlinGPTUnifiedSystem:
    """Get the global unified system instance"""
    global _unified_system
    if _unified_system is None:
        _unified_system = GremlinGPTUnifiedSystem()
    return _unified_system


async def initialize_gremlin_ecosystem():
    """Initialize the complete GremlinGPT ecosystem"""
    unified_system = get_unified_system()
    
    # Start async integration
    unified_system.start_async_integration()
    
    # Give async thread time to start
    import time
    time.sleep(1)
    
    # Initialize unified system
    await unified_system.initialize_unified_system()
    
    return unified_system


def create_ecosystem_integration_task():
    """Create a task to integrate the new ecosystem with existing FSM"""
    return {
        "type": "ecosystem_integration",
        "action": "initialize",
        "priority": "high",
        "meta": {
            "reason": "unified_system_integration",
            "timestamp": datetime.now(timezone.utc).isoformat()
        }
    }


if __name__ == "__main__":
    async def test_unified_system():
        unified_system = await initialize_gremlin_ecosystem()
        
        # Test system status
        status = await unified_system.get_system_status()
        print("Unified System Status:")
        print(json.dumps(status, indent=2, default=str))
        
        # Test workflow execution
        print("\nExecuting test workflow...")
        result = await unified_system.execute_unified_workflow(
            "comprehensive_market_analysis",
            {
                "symbols": ["AAPL", "GOOGL"],
                "analysis_depth": "standard"
            }
        )
        print("Workflow Result:")
        print(json.dumps(result, indent=2, default=str))
        
        # Shutdown
        await unified_system.shutdown_unified_system()
    
    asyncio.run(test_unified_system())

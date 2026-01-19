#!/usr/bin/env python3

# ─────────────────────────────────────────────────────────────
# ⚠️ GremlinGPT Fair Use Only | Commercial Use Requires License
# Built under the GremlinGPT Dual License v1.0
# © 2025 StatikFintechLLC / AscendAI Project
# Contact: ascend.gremlin@gmail.com
# ─────────────────────────────────────────────────────────────

# GremlinGPT v1.0.3 :: Core Orchestrator - Global Intelligence Coordinator

import asyncio
import threading
import time
from datetime import datetime, timezone
from pathlib import Path
import sys
import json
from typing import Dict, List, Any, Optional
from concurrent.futures import ThreadPoolExecutor
import logging

# Add project root to path for imports
project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root))

from backend.globals import CFG, LOOP
from utils.logging_config import setup_module_logger
from memory.log_history import log_event
from backend.state_manager import save_state, load_state

logger = setup_module_logger("core", "orchestrator")


class GlobalOrchestrator:
    """
    GremlinGPT Global Intelligence Orchestrator
    
    This is the master coordinator that unifies all GremlinGPT capabilities:
    - Scrapers, Mutators, Memory, Training, Trading, Dashboard, Servers
    - Global State Management and Cross-Module Communication
    - Autonomous Learning and Self-Improvement
    - Real-time Decision Making and Execution
    """
    
    def __init__(self):
        self.state = {
            "status": "INITIALIZING",
            "active_modules": set(),
            "global_memory": {},
            "performance_metrics": {},
            "learning_state": {},
            "last_heartbeat": None,
            "orchestrator_id": f"orchestrator_{datetime.now().strftime('%Y%m%d_%H%M%S')}"
        }
        
        self.module_registry = {}
        self.communication_channels = {}
        self.thread_pool = ThreadPoolExecutor(max_workers=CFG.get("orchestrator", {}).get("max_workers", 8))
        self.running = False
        self.modules_lock = threading.Lock()
        
        # Global state persistence
        self.state_file = Path("run/checkpoints/orchestrator_state.json")
        self.state_file.parent.mkdir(parents=True, exist_ok=True)
        
        logger.info(f"[ORCHESTRATOR] Initializing Global Intelligence Coordinator: {self.state['orchestrator_id']}")
    
    def register_module(self, module_name: str, module_instance: Any, capabilities: Optional[List[str]] = None):
        """Register a module with the global orchestrator"""
        with self.modules_lock:
            self.module_registry[module_name] = {
                "instance": module_instance,
                "capabilities": capabilities or [],
                "status": "REGISTERED",
                "last_activity": datetime.now(timezone.utc),
                "performance_score": 1.0,
                "error_count": 0
            }
            self.state["active_modules"].add(module_name)
            
        logger.info(f"[ORCHESTRATOR] Registered module: {module_name} with capabilities: {capabilities}")
        log_event("orchestrator", "module_registered", {
            "module": module_name,
            "capabilities": capabilities,
            "timestamp": datetime.now(timezone.utc).isoformat()
        })
    
    def get_module_status(self, module_name: Optional[str] = None) -> Dict[str, Any]:
        """Get status of specific module or all modules"""
        with self.modules_lock:
            if module_name:
                return self.module_registry.get(module_name, {})
            return dict(self.module_registry)
    
    def update_module_performance(self, module_name: str, success: bool, execution_time: Optional[float] = None):
        """Update performance metrics for a module"""
        with self.modules_lock:
            if module_name in self.module_registry:
                module = self.module_registry[module_name]
                module["last_activity"] = datetime.now(timezone.utc)
                
                if success:
                    module["performance_score"] = min(1.0, module["performance_score"] + 0.01)
                else:
                    module["error_count"] += 1
                    module["performance_score"] = max(0.1, module["performance_score"] - 0.05)
                
                if execution_time:
                    if "avg_execution_time" not in module:
                        module["avg_execution_time"] = execution_time
                    else:
                        module["avg_execution_time"] = (module["avg_execution_time"] + execution_time) / 2
    
    def create_communication_channel(self, channel_name: str, channel_type: str = "queue"):
        """Create a communication channel between modules"""
        if channel_type == "queue":
            self.communication_channels[channel_name] = asyncio.Queue()
        elif channel_type == "event":
            self.communication_channels[channel_name] = asyncio.Event()
        else:
            self.communication_channels[channel_name] = {}
        
        logger.info(f"[ORCHESTRATOR] Created communication channel: {channel_name} [{channel_type}]")
    
    async def send_message(self, channel_name: str, message: Dict[str, Any], sender: Optional[str] = None):
        """Send a message through a communication channel"""
        if channel_name in self.communication_channels:
            channel = self.communication_channels[channel_name]
            
            message_envelope = {
                "sender": sender,
                "timestamp": datetime.now(timezone.utc).isoformat(),
                "message": message,
                "channel": channel_name
            }
            
            if isinstance(channel, asyncio.Queue):
                await channel.put(message_envelope)
            else:
                # Store in dict-based channel
                msg_id = f"{sender}_{datetime.now().timestamp()}"
                channel[msg_id] = message_envelope
            
            logger.debug(f"[ORCHESTRATOR] Message sent to {channel_name} from {sender}")
    
    async def receive_message(self, channel_name: str, timeout: float = 1.0) -> Optional[Dict[str, Any]]:
        """Receive a message from a communication channel"""
        if channel_name in self.communication_channels:
            channel = self.communication_channels[channel_name]
            
            if isinstance(channel, asyncio.Queue):
                try:
                    message = await asyncio.wait_for(channel.get(), timeout=timeout)
                    return message
                except asyncio.TimeoutError:
                    return None
            else:
                # Get latest message from dict-based channel
                if channel:
                    latest_key = max(channel.keys())
                    return channel.pop(latest_key)
        return None
    
    def save_global_state(self):
        """Save the current global state to disk"""
        try:
            state_data = {
                "orchestrator_state": self.state,
                "module_registry": {
                    name: {
                        "capabilities": info["capabilities"],
                        "status": info["status"],
                        "last_activity": info["last_activity"].isoformat(),
                        "performance_score": info["performance_score"],
                        "error_count": info["error_count"]
                    }
                    for name, info in self.module_registry.items()
                },
                "timestamp": datetime.now(timezone.utc).isoformat()
            }
            
            with open(self.state_file, 'w') as f:
                json.dump(state_data, f, indent=2)
            
            logger.debug(f"[ORCHESTRATOR] Global state saved to {self.state_file}")
            return True
        except Exception as e:
            logger.error(f"[ORCHESTRATOR] Failed to save global state: {e}")
            return False
    
    def load_global_state(self):
        """Load the global state from disk"""
        try:
            if self.state_file.exists():
                with open(self.state_file, 'r') as f:
                    state_data = json.load(f)
                
                self.state.update(state_data.get("orchestrator_state", {}))
                
                # Restore module registry (without instances)
                for name, info in state_data.get("module_registry", {}).items():
                    self.module_registry[name] = {
                        "instance": None,  # Will be re-registered
                        "capabilities": info["capabilities"],
                        "status": "RESTORED",
                        "last_activity": datetime.fromisoformat(info["last_activity"]),
                        "performance_score": info["performance_score"],
                        "error_count": info["error_count"]
                    }
                
                logger.info(f"[ORCHESTRATOR] Global state loaded from {self.state_file}")
                return True
        except Exception as e:
            logger.error(f"[ORCHESTRATOR] Failed to load global state: {e}")
        return False
    
    def get_global_intelligence(self) -> Dict[str, Any]:
        """Get comprehensive system intelligence snapshot"""
        intelligence = {
            "orchestrator_status": self.state,
            "module_status": self.get_module_status(),
            "communication_channels": list(self.communication_channels.keys()),
            "system_health": self.calculate_system_health(),
            "performance_summary": self.get_performance_summary(),
            "timestamp": datetime.now(timezone.utc).isoformat()
        }
        
        return intelligence
    
    def calculate_system_health(self) -> Dict[str, Any]:
        """Calculate overall system health metrics"""
        with self.modules_lock:
            if not self.module_registry:
                return {"overall_health": 0.0, "status": "NO_MODULES"}
            
            total_performance = sum(
                module["performance_score"] for module in self.module_registry.values()
            )
            avg_performance = total_performance / len(self.module_registry)
            
            total_errors = sum(
                module["error_count"] for module in self.module_registry.values()
            )
            
            active_modules = sum(
                1 for module in self.module_registry.values() 
                if module["status"] in ["ACTIVE", "REGISTERED"]
            )
            
            health_score = (avg_performance * 0.7) + (active_modules / len(self.module_registry) * 0.3)
            
            if total_errors > 10:
                health_score *= 0.8  # Penalize high error count
            
            return {
                "overall_health": round(health_score, 3),
                "avg_performance": round(avg_performance, 3),
                "active_modules": active_modules,
                "total_modules": len(self.module_registry),
                "total_errors": total_errors,
                "status": "HEALTHY" if health_score > 0.8 else "DEGRADED" if health_score > 0.5 else "CRITICAL"
            }
    
    def get_performance_summary(self) -> Dict[str, Any]:
        """Get performance summary for all modules"""
        with self.modules_lock:
            summary = {}
            for name, module in self.module_registry.items():
                summary[name] = {
                    "performance_score": module["performance_score"],
                    "error_count": module["error_count"],
                    "status": module["status"],
                    "avg_execution_time": module.get("avg_execution_time", 0)
                }
            return summary
    
    async def heartbeat(self):
        """Send system heartbeat and update global state"""
        self.state["last_heartbeat"] = datetime.now(timezone.utc).isoformat()
        self.state["status"] = "RUNNING" if self.running else "STOPPED"
        
        # Save state periodically
        if datetime.now().minute % 5 == 0:  # Every 5 minutes
            self.save_global_state()
        
        # Log system intelligence
        intelligence = self.get_global_intelligence()
        log_event("orchestrator", "heartbeat", intelligence)
        
        logger.debug(f"[ORCHESTRATOR] Heartbeat - Health: {intelligence['system_health']['overall_health']}")
    
    async def start(self):
        """Start the global orchestrator"""
        logger.info("[ORCHESTRATOR] Starting Global Intelligence Coordinator...")
        
        # Load previous state
        self.load_global_state()
        
        # Create essential communication channels
        essential_channels = [
            ("module_commands", "queue"),
            ("system_events", "queue"),
            ("emergency_signals", "queue"),
            ("learning_updates", "queue"),
            ("trading_signals", "queue"),
            ("memory_updates", "queue")
        ]
        
        for channel_name, channel_type in essential_channels:
            self.create_communication_channel(channel_name, channel_type)
        
        self.running = True
        self.state["status"] = "RUNNING"
        
        # Start heartbeat loop
        asyncio.create_task(self.heartbeat_loop())
        
        logger.success("[ORCHESTRATOR] Global Intelligence Coordinator started successfully")
        log_event("orchestrator", "started", {"orchestrator_id": self.state["orchestrator_id"]})
    
    async def heartbeat_loop(self):
        """Continuous heartbeat loop"""
        while self.running:
            try:
                await self.heartbeat()
                await asyncio.sleep(LOOP.get("orchestrator_heartbeat_interval", 30))
            except Exception as e:
                logger.error(f"[ORCHESTRATOR] Heartbeat error: {e}")
                await asyncio.sleep(5)
    
    async def stop(self):
        """Stop the global orchestrator"""
        logger.info("[ORCHESTRATOR] Stopping Global Intelligence Coordinator...")
        
        self.running = False
        self.state["status"] = "STOPPING"
        
        # Save final state
        self.save_global_state()
        
        # Shutdown thread pool
        self.thread_pool.shutdown(wait=True)
        
        self.state["status"] = "STOPPED"
        logger.success("[ORCHESTRATOR] Global Intelligence Coordinator stopped")
        log_event("orchestrator", "stopped", {"orchestrator_id": self.state["orchestrator_id"]})


# Global orchestrator instance
_global_orchestrator = None


def get_global_orchestrator() -> GlobalOrchestrator:
    """Get the global orchestrator instance"""
    global _global_orchestrator
    if _global_orchestrator is None:
        _global_orchestrator = GlobalOrchestrator()
    return _global_orchestrator


def initialize_orchestrator():
    """Initialize the global orchestrator"""
    orchestrator = get_global_orchestrator()
    return orchestrator


async def start_orchestrator():
    """Start the global orchestrator"""
    orchestrator = get_global_orchestrator()
    await orchestrator.start()
    return orchestrator


async def stop_orchestrator():
    """Stop the global orchestrator"""
    orchestrator = get_global_orchestrator()
    await orchestrator.stop()


if __name__ == "__main__":
    async def main():
        orchestrator = await start_orchestrator()
        try:
            # Keep running
            while orchestrator.running:
                await asyncio.sleep(1)
        except KeyboardInterrupt:
            logger.info("[ORCHESTRATOR] Received shutdown signal")
        finally:
            await stop_orchestrator()
    
    asyncio.run(main())

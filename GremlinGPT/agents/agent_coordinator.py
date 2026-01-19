#!/usr/bin/env python3

# ─────────────────────────────────────────────────────────────
# ⚠️ GremlinGPT Fair Use Only | Commercial Use Requires License
# Built under the GremlinGPT Dual License v1.0
# © 2025 StatikFintechLLC / AscendAI Project
# Contact: ascend.gremlin@gmail.com
# ─────────────────────────────────────────────────────────────

# GremlinGPT v1.0.3 :: Unified Agent Coordinator - Multi-Agent Orchestration

import asyncio
import threading
from datetime import datetime, timezone, timedelta
from pathlib import Path
import sys
import json
from typing import Dict, List, Any, Optional, Callable
from concurrent.futures import ThreadPoolExecutor, as_completed
import logging

# Add project root to path for imports
project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root))

from backend.globals import CFG, LOOP
from utils.logging_config import setup_module_logger
from memory.log_history import log_event
from memory.vector_store import embedder
from agent_core.task_queue import enqueue_task
from core.orchestrator import get_global_orchestrator

# Import specialized agents
from agents.data_analyst_agent import get_data_analyst_agent
from agents.trading_strategist_agent import get_trading_strategist_agent
from agents.learning_agent import get_learning_agent

logger = setup_module_logger("agents", "coordinator")


class AgentCoordinator:
    """
    Unified Agent Coordinator for Multi-Agent Orchestration
    
    This coordinator manages all specialized agents and orchestrates their
    collaboration to achieve complex, multi-faceted goals that require
    the combined capabilities of multiple agents working in harmony.
    """
    
    def __init__(self):
        self.coordinator_id = f"agent_coordinator_{datetime.now().strftime('%Y%m%d_%H%M%S')}"
        self.agents = {}
        self.active_workflows = {}
        self.collaboration_history = []
        self.performance_metrics = {}
        
        # Coordination configuration
        self.config = CFG.get("agent_coordinator", {
            "max_concurrent_workflows": 5,
            "agent_timeout": 300,  # 5 minutes
            "collaboration_memory_days": 30,
            "auto_learning_enabled": True,
            "cross_agent_validation": True
        })
        
        self.thread_pool = ThreadPoolExecutor(max_workers=CFG.get("agent_coordinator", {}).get("max_workers", 4))
        self.coordination_lock = threading.Lock()
        
        logger.info(f"[AGENT_COORDINATOR] Initialized coordinator: {self.coordinator_id}")
    
    async def initialize_agents(self):
        """Initialize and register all specialized agents"""
        try:
            # Initialize specialized agents
            self.agents = {
                "data_analyst": get_data_analyst_agent(),
                "trading_strategist": get_trading_strategist_agent(),
                "learning_agent": get_learning_agent()
            }
            
            # Register agents with global orchestrator
            orchestrator = get_global_orchestrator()
            
            for agent_name, agent_instance in self.agents.items():
                capabilities = getattr(agent_instance, 'capabilities', [])
                orchestrator.register_module(f"agent_{agent_name}", agent_instance, capabilities)
            
            # Register coordinator itself
            orchestrator.register_module("agent_coordinator", self, [
                "multi_agent_orchestration",
                "workflow_management",
                "agent_collaboration",
                "performance_optimization"
            ])
            
            logger.success(f"[AGENT_COORDINATOR] Initialized {len(self.agents)} specialized agents")
            log_event("agent_coordinator", "agents_initialized", {
                "agent_count": len(self.agents),
                "agent_types": list(self.agents.keys())
            })
            
        except Exception as e:
            logger.error(f"[AGENT_COORDINATOR] Agent initialization failed: {e}")
            raise
    
    async def execute_collaborative_workflow(self, workflow_definition: Dict[str, Any]) -> Dict[str, Any]:
        """Execute a complex workflow requiring multiple agents"""
        workflow_id = f"workflow_{datetime.now().strftime('%Y%m%d_%H%M%S')}_{len(self.active_workflows)}"
        
        workflow_result = {
            "workflow_id": workflow_id,
            "start_time": datetime.now(timezone.utc).isoformat(),
            "end_time": None,
            "status": "RUNNING",
            "agents_involved": [],
            "task_results": {},
            "collaboration_insights": {},
            "final_outcome": {}
        }
        
        try:
            with self.coordination_lock:
                if len(self.active_workflows) >= self.config["max_concurrent_workflows"]:
                    workflow_result["status"] = "REJECTED"
                    workflow_result["error"] = "Maximum concurrent workflows exceeded"
                    return workflow_result
                
                self.active_workflows[workflow_id] = workflow_result
            
            workflow_type = workflow_definition.get("type", "general")
            workflow_data = workflow_definition.get("data", {})
            workflow_goals = workflow_definition.get("goals", [])
            
            logger.info(f"[AGENT_COORDINATOR] Starting workflow: {workflow_id} [{workflow_type}]")
            
            # Execute workflow based on type
            if workflow_type == "comprehensive_market_analysis":
                final_outcome = await self._execute_market_analysis_workflow(workflow_id, workflow_data)
            
            elif workflow_type == "adaptive_learning_cycle":
                final_outcome = await self._execute_learning_cycle_workflow(workflow_id, workflow_data)
            
            elif workflow_type == "performance_optimization":
                final_outcome = await self._execute_optimization_workflow(workflow_id, workflow_data)
            
            elif workflow_type == "anomaly_investigation":
                final_outcome = await self._execute_anomaly_investigation_workflow(workflow_id, workflow_data)
            
            elif workflow_type == "strategic_planning":
                final_outcome = await self._execute_strategic_planning_workflow(workflow_id, workflow_data)
            
            else:
                final_outcome = await self._execute_custom_workflow(workflow_id, workflow_definition)
            
            workflow_result["final_outcome"] = final_outcome
            workflow_result["status"] = "COMPLETED"
            
            # Analyze collaboration effectiveness
            collaboration_insights = await self._analyze_collaboration_effectiveness(workflow_id)
            workflow_result["collaboration_insights"] = collaboration_insights
            
            # Update learning agent with workflow results
            if self.config["auto_learning_enabled"]:
                await self._update_learning_from_workflow(workflow_id, workflow_result)
            
            logger.success(f"[AGENT_COORDINATOR] Completed workflow: {workflow_id}")
            
        except Exception as e:
            logger.error(f"[AGENT_COORDINATOR] Workflow {workflow_id} failed: {e}")
            workflow_result["status"] = "FAILED"
            workflow_result["error"] = str(e)
        
        finally:
            workflow_result["end_time"] = datetime.now(timezone.utc).isoformat()
            
            with self.coordination_lock:
                if workflow_id in self.active_workflows:
                    del self.active_workflows[workflow_id]
            
            # Store in collaboration history
            self.collaboration_history.append(workflow_result)
            
            # Trim history if too large
            if len(self.collaboration_history) > 100:
                self.collaboration_history.pop(0)
        
        return workflow_result
    
    async def _execute_market_analysis_workflow(self, workflow_id: str, data: Dict[str, Any]) -> Dict[str, Any]:
        """Execute comprehensive market analysis using multiple agents"""
        market_data = data.get("market_data", {})
        symbols = data.get("symbols", [])
        analysis_depth = data.get("analysis_depth", "standard")
        
        workflow_result = await self._get_workflow_result(workflow_id)
        
        # Step 1: Data Analysis - Analyze market data for patterns and anomalies
        logger.info(f"[WORKFLOW:{workflow_id}] Step 1: Data analysis")
        
        data_analysis_task = {
            "type": "analyze_data",
            "data": [{"symbol": symbol, **market_data.get(symbol, {})} for symbol in symbols],
            "stream_name": "market_analysis"
        }
        
        data_analysis_result = await self.agents["data_analyst"].handle_task(data_analysis_task)
        workflow_result["task_results"]["data_analysis"] = data_analysis_result
        workflow_result["agents_involved"].append("data_analyst")
        
        # Step 2: Trading Analysis - Generate trading signals and risk assessment
        logger.info(f"[WORKFLOW:{workflow_id}] Step 2: Trading strategy analysis")
        
        trading_analysis_task = {
            "type": "generate_signals",
            "market_data": market_data,
            "symbols": symbols
        }
        
        trading_analysis_result = await self.agents["trading_strategist"].handle_task(trading_analysis_task)
        workflow_result["task_results"]["trading_analysis"] = trading_analysis_result
        workflow_result["agents_involved"].append("trading_strategist")
        
        # Step 3: Cross-validation and synthesis
        logger.info(f"[WORKFLOW:{workflow_id}] Step 3: Cross-validation and synthesis")
        
        synthesis_result = await self._synthesize_market_analysis(
            data_analysis_result, 
            trading_analysis_result, 
            analysis_depth
        )
        
        # Step 4: Learning integration
        if self.config["auto_learning_enabled"]:
            logger.info(f"[WORKFLOW:{workflow_id}] Step 4: Learning integration")
            
            learning_task = {
                "type": "monitor_performance",
                "module_name": "market_analysis_workflow",
                "metrics": {
                    "data_quality": data_analysis_result.get("quality_score", 0),
                    "signals_generated": len(trading_analysis_result.get("signals", [])),
                    "anomalies_detected": len(data_analysis_result.get("anomalies", [])),
                    "synthesis_confidence": synthesis_result.get("confidence", 0)
                }
            }
            
            learning_result = await self.agents["learning_agent"].handle_task(learning_task)
            workflow_result["task_results"]["learning_integration"] = learning_result
            workflow_result["agents_involved"].append("learning_agent")
        
        return synthesis_result
    
    async def _execute_learning_cycle_workflow(self, workflow_id: str, data: Dict[str, Any]) -> Dict[str, Any]:
        """Execute adaptive learning cycle across all agents"""
        learning_focus = data.get("focus", "performance_improvement")
        data_sources = data.get("data_sources", ["trading_core", "scraper", "nlp_engine"])
        
        workflow_result = await self._get_workflow_result(workflow_id)
        
        # Step 1: Performance monitoring across all modules
        logger.info(f"[WORKFLOW:{workflow_id}] Step 1: Performance monitoring")
        
        performance_data = {}
        for source in data_sources:
            # Simulate performance metrics (in real implementation, these would come from actual modules)
            metrics = self._get_module_performance_metrics(source)
            
            monitoring_task = {
                "type": "monitor_performance",
                "module_name": source,
                "metrics": metrics
            }
            
            monitoring_result = await self.agents["learning_agent"].handle_task(monitoring_task)
            performance_data[source] = monitoring_result
        
        workflow_result["task_results"]["performance_monitoring"] = performance_data
        workflow_result["agents_involved"].append("learning_agent")
        
        # Step 2: Pattern discovery across data sources
        logger.info(f"[WORKFLOW:{workflow_id}] Step 2: Pattern discovery")
        
        pattern_discovery_task = {
            "type": "discover_patterns",
            "data_sources": data_sources,
            "analysis_type": "correlation"
        }
        
        pattern_result = await self.agents["learning_agent"].handle_task(pattern_discovery_task)
        workflow_result["task_results"]["pattern_discovery"] = pattern_result
        
        # Step 3: Data-driven insights for strategy improvement
        logger.info(f"[WORKFLOW:{workflow_id}] Step 3: Strategy optimization insights")
        
        # Use data analyst to find optimization opportunities
        optimization_data = []
        for source, perf_data in performance_data.items():
            opportunities = perf_data.get("learning_opportunities", [])
            for opp in opportunities:
                optimization_data.append({
                    "source": source,
                    "metric": opp.get("metric", ""),
                    "change": opp.get("change", 0),
                    "type": opp.get("type", "")
                })
        
        data_analysis_task = {
            "type": "analyze_data",
            "data": optimization_data,
            "stream_name": "performance_optimization"
        }
        
        optimization_analysis = await self.agents["data_analyst"].handle_task(data_analysis_task)
        workflow_result["task_results"]["optimization_analysis"] = optimization_analysis
        workflow_result["agents_involved"].append("data_analyst")
        
        # Step 4: Parameter optimization
        logger.info(f"[WORKFLOW:{workflow_id}] Step 4: Parameter optimization")
        
        parameter_optimization_task = {"type": "optimize_parameters"}
        parameter_result = await self.agents["learning_agent"].handle_task(parameter_optimization_task)
        workflow_result["task_results"]["parameter_optimization"] = parameter_result
        
        # Step 5: Synthesis and recommendations
        learning_synthesis = await self._synthesize_learning_cycle(
            performance_data, pattern_result, optimization_analysis, parameter_result
        )
        
        return learning_synthesis
    
    async def _execute_optimization_workflow(self, workflow_id: str, data: Dict[str, Any]) -> Dict[str, Any]:
        """Execute performance optimization workflow"""
        target_modules = data.get("modules", ["trading_core", "scraper"])
        optimization_goals = data.get("goals", ["improve_accuracy", "reduce_latency"])
        
        workflow_result = await self._get_workflow_result(workflow_id)
        
        # Step 1: Current performance assessment
        logger.info(f"[WORKFLOW:{workflow_id}] Step 1: Performance assessment")
        
        current_performance = {}
        for module in target_modules:
            metrics = self._get_module_performance_metrics(module)
            
            # Analyze current performance with data analyst
            analysis_task = {
                "type": "analyze_data",
                "data": [{"module": module, **metrics}],
                "stream_name": f"{module}_performance"
            }
            
            analysis_result = await self.agents["data_analyst"].handle_task(analysis_task)
            current_performance[module] = analysis_result
        
        workflow_result["task_results"]["performance_assessment"] = current_performance
        workflow_result["agents_involved"].append("data_analyst")
        
        # Step 2: Optimization opportunity identification
        logger.info(f"[WORKFLOW:{workflow_id}] Step 2: Opportunity identification")
        
        optimization_opportunities = []
        for module, analysis in current_performance.items():
            for insight in analysis.get("insights", []):
                if any(goal in insight.lower() for goal in optimization_goals):
                    optimization_opportunities.append({
                        "module": module,
                        "opportunity": insight,
                        "priority": "high" if "critical" in insight.lower() else "medium"
                    })
        
        # Step 3: Strategy recommendation
        if "trading_core" in target_modules:
            logger.info(f"[WORKFLOW:{workflow_id}] Step 3: Trading strategy optimization")
            
            # Get current trading performance
            trading_performance = current_performance.get("trading_core", {})
            
            # Use trading strategist to optimize
            portfolio_optimization_task = {
                "type": "optimize_portfolio",
                "positions": data.get("current_positions", {}),
                "signals": []  # Would be populated with current signals
            }
            
            trading_optimization = await self.agents["trading_strategist"].handle_task(portfolio_optimization_task)
            workflow_result["task_results"]["trading_optimization"] = trading_optimization
            workflow_result["agents_involved"].append("trading_strategist")
        
        # Step 4: Learning-based recommendations
        logger.info(f"[WORKFLOW:{workflow_id}] Step 4: Learning-based recommendations")
        
        learning_summary_task = {"type": "get_learning_summary"}
        learning_summary = await self.agents["learning_agent"].handle_task(learning_summary_task)
        workflow_result["task_results"]["learning_summary"] = learning_summary
        workflow_result["agents_involved"].append("learning_agent")
        
        # Step 5: Synthesis and action plan
        optimization_synthesis = await self._synthesize_optimization_workflow(
            current_performance, optimization_opportunities, learning_summary
        )
        
        return optimization_synthesis
    
    async def _execute_anomaly_investigation_workflow(self, workflow_id: str, data: Dict[str, Any]) -> Dict[str, Any]:
        """Execute anomaly investigation workflow"""
        anomaly_data = data.get("anomaly_data", {})
        investigation_scope = data.get("scope", "comprehensive")
        
        workflow_result = await self._get_workflow_result(workflow_id)
        
        # Step 1: Detailed anomaly analysis
        logger.info(f"[WORKFLOW:{workflow_id}] Step 1: Anomaly analysis")
        
        anomaly_analysis_task = {
            "type": "detect_anomalies",
            "data": anomaly_data.get("data_points", []),
            "stream_name": "anomaly_investigation"
        }
        
        anomaly_analysis = await self.agents["data_analyst"].handle_task(anomaly_analysis_task)
        workflow_result["task_results"]["anomaly_analysis"] = anomaly_analysis
        workflow_result["agents_involved"].append("data_analyst")
        
        # Step 2: Impact assessment
        if "trading" in investigation_scope.lower():
            logger.info(f"[WORKFLOW:{workflow_id}] Step 2: Trading impact assessment")
            
            risk_assessment_task = {
                "type": "assess_risk",
                "symbol": anomaly_data.get("symbol", "UNKNOWN"),
                "data": anomaly_data
            }
            
            risk_assessment = await self.agents["trading_strategist"].handle_task(risk_assessment_task)
            workflow_result["task_results"]["risk_assessment"] = risk_assessment
            workflow_result["agents_involved"].append("trading_strategist")
        
        # Step 3: Historical pattern analysis
        logger.info(f"[WORKFLOW:{workflow_id}] Step 3: Historical pattern analysis")
        
        pattern_analysis_task = {
            "type": "discover_patterns",
            "data_sources": [anomaly_data.get("source", "unknown")],
            "analysis_type": "anomaly"
        }
        
        pattern_analysis = await self.agents["learning_agent"].handle_task(pattern_analysis_task)
        workflow_result["task_results"]["pattern_analysis"] = pattern_analysis
        workflow_result["agents_involved"].append("learning_agent")
        
        # Step 4: Investigation synthesis
        investigation_synthesis = await self._synthesize_anomaly_investigation(
            anomaly_analysis, workflow_result["task_results"], investigation_scope
        )
        
        return investigation_synthesis
    
    async def _execute_strategic_planning_workflow(self, workflow_id: str, data: Dict[str, Any]) -> Dict[str, Any]:
        """Execute strategic planning workflow"""
        planning_horizon = data.get("horizon", "medium_term")  # short_term, medium_term, long_term
        focus_areas = data.get("focus_areas", ["trading", "learning", "optimization"])
        
        workflow_result = await self._get_workflow_result(workflow_id)
        
        # Step 1: Current state analysis
        logger.info(f"[WORKFLOW:{workflow_id}] Step 1: Current state analysis")
        
        current_state = {}
        
        # Get learning agent summary
        learning_summary_task = {"type": "get_learning_summary"}
        learning_state = await self.agents["learning_agent"].handle_task(learning_summary_task)
        current_state["learning"] = learning_state
        
        # Analyze system performance data
        system_performance_data = self._get_system_wide_metrics()
        performance_analysis_task = {
            "type": "analyze_data",
            "data": system_performance_data,
            "stream_name": "system_performance"
        }
        
        performance_analysis = await self.agents["data_analyst"].handle_task(performance_analysis_task)
        current_state["performance"] = performance_analysis
        
        workflow_result["task_results"]["current_state"] = current_state
        workflow_result["agents_involved"].extend(["learning_agent", "data_analyst"])
        
        # Step 2: Opportunity identification
        logger.info(f"[WORKFLOW:{workflow_id}] Step 2: Opportunity identification")
        
        opportunities = []
        
        # Learning opportunities
        learning_effectiveness = learning_state.get("learning_effectiveness", 0.5)
        if learning_effectiveness < 0.7:
            opportunities.append({
                "area": "learning",
                "opportunity": "Improve learning effectiveness",
                "priority": "high",
                "potential_impact": "system_wide"
            })
        
        # Performance opportunities
        for insight in performance_analysis.get("insights", []):
            opportunities.append({
                "area": "performance",
                "opportunity": insight,
                "priority": "medium",
                "potential_impact": "module_specific"
            })
        
        # Step 3: Strategic recommendations
        logger.info(f"[WORKFLOW:{workflow_id}] Step 3: Strategic recommendations")
        
        strategic_recommendations = await self._generate_strategic_recommendations(
            current_state, opportunities, planning_horizon, focus_areas
        )
        
        workflow_result["task_results"]["strategic_recommendations"] = strategic_recommendations
        
        # Step 4: Implementation planning
        implementation_plan = await self._create_implementation_plan(
            strategic_recommendations, planning_horizon
        )
        
        workflow_result["task_results"]["implementation_plan"] = implementation_plan
        
        # Step 5: Strategy synthesis
        strategy_synthesis = await self._synthesize_strategic_planning(
            current_state, opportunities, strategic_recommendations, implementation_plan
        )
        
        return strategy_synthesis
    
    async def _execute_custom_workflow(self, workflow_id: str, workflow_definition: Dict[str, Any]) -> Dict[str, Any]:
        """Execute custom workflow based on definition"""
        steps = workflow_definition.get("steps", [])
        workflow_data = workflow_definition.get("data", {})
        
        workflow_result = await self._get_workflow_result(workflow_id)
        custom_results = {}
        
        for i, step in enumerate(steps):
            step_name = step.get("name", f"step_{i+1}")
            agent_name = step.get("agent")
            task = step.get("task", {})
            
            logger.info(f"[WORKFLOW:{workflow_id}] Custom step {i+1}: {step_name}")
            
            if agent_name in self.agents:
                # Add workflow data to task
                task.update(workflow_data.get(step_name, {}))
                
                step_result = await self.agents[agent_name].handle_task(task)
                custom_results[step_name] = step_result
                
                if agent_name not in workflow_result["agents_involved"]:
                    workflow_result["agents_involved"].append(agent_name)
            else:
                logger.warning(f"[WORKFLOW:{workflow_id}] Unknown agent: {agent_name}")
                custom_results[step_name] = {"error": f"Unknown agent: {agent_name}"}
        
        workflow_result["task_results"]["custom_steps"] = custom_results
        
        return {"custom_workflow_results": custom_results, "steps_completed": len(steps)}
    
    async def _get_workflow_result(self, workflow_id: str) -> Dict[str, Any]:
        """Get workflow result object"""
        with self.coordination_lock:
            return self.active_workflows.get(workflow_id, {})
    
    def _get_module_performance_metrics(self, module_name: str) -> Dict[str, float]:
        """Get performance metrics for a module (simulated for now)"""
        # In a real implementation, this would fetch actual metrics from modules
        base_metrics = {
            "accuracy": 0.85,
            "response_time": 1.2,
            "success_rate": 0.92,
            "error_rate": 0.08,
            "throughput": 50.0
        }
        
        # Add module-specific metrics
        if module_name == "trading_core":
            base_metrics.update({
                "profit_factor": 1.25,
                "win_rate": 0.68,
                "sharpe_ratio": 1.15,
                "max_drawdown": 0.12
            })
        elif module_name == "scraper":
            base_metrics.update({
                "scrape_success_rate": 0.95,
                "data_quality": 0.88,
                "coverage": 0.92
            })
        elif module_name == "nlp_engine":
            base_metrics.update({
                "semantic_accuracy": 0.91,
                "processing_speed": 45.0,
                "model_confidence": 0.87
            })
        
        return base_metrics
    
    def _get_system_wide_metrics(self) -> List[Dict[str, Any]]:
        """Get system-wide performance metrics"""
        return [
            {"metric": "overall_system_health", "value": 0.89, "timestamp": datetime.now().isoformat()},
            {"metric": "agent_coordination_efficiency", "value": 0.92, "timestamp": datetime.now().isoformat()},
            {"metric": "learning_rate", "value": 0.75, "timestamp": datetime.now().isoformat()},
            {"metric": "adaptive_capability", "value": 0.83, "timestamp": datetime.now().isoformat()}
        ]
    
    async def _synthesize_market_analysis(self, data_analysis: Dict[str, Any], 
                                         trading_analysis: Dict[str, Any], 
                                         analysis_depth: str) -> Dict[str, Any]:
        """Synthesize market analysis results from multiple agents"""
        synthesis = {
            "analysis_confidence": 0.0,
            "key_insights": [],
            "trading_recommendations": [],
            "risk_assessment": {},
            "data_quality_score": data_analysis.get("quality_score", 0),
            "signals_confidence": 0.0
        }
        
        # Calculate overall confidence
        data_confidence = data_analysis.get("quality_score", 0)
        signals = trading_analysis.get("signals", [])
        
        if signals:
            signal_confidences = [signal.get("confidence", 0) for signal in signals]
            signals_confidence = sum(signal_confidences) / len(signal_confidences)
        else:
            signals_confidence = 0.0
        
        synthesis["signals_confidence"] = signals_confidence
        synthesis["analysis_confidence"] = (data_confidence + signals_confidence) / 2
        
        # Extract key insights
        synthesis["key_insights"].extend(data_analysis.get("insights", []))
        
        # Process trading signals
        high_confidence_signals = [s for s in signals if s.get("confidence", 0) > 0.7]
        synthesis["trading_recommendations"] = [
            {
                "symbol": signal.get("symbol"),
                "action": signal.get("signal_type"),
                "confidence": signal.get("confidence"),
                "reasoning": signal.get("reasoning")
            }
            for signal in high_confidence_signals
        ]
        
        # Aggregate risk assessment
        if high_confidence_signals:
            risk_levels = [signal.get("risk_level", "medium") for signal in high_confidence_signals]
            synthesis["risk_assessment"] = {
                "overall_risk": max(risk_levels) if risk_levels else "medium",
                "signal_count": len(high_confidence_signals),
                "risk_distribution": {level: risk_levels.count(level) for level in set(risk_levels)}
            }
        
        return synthesis
    
    async def _synthesize_learning_cycle(self, performance_data: Dict[str, Any], 
                                        pattern_result: Dict[str, Any], 
                                        optimization_analysis: Dict[str, Any], 
                                        parameter_result: Dict[str, Any]) -> Dict[str, Any]:
        """Synthesize learning cycle results"""
        synthesis = {
            "learning_effectiveness": 0.0,
            "improvement_opportunities": [],
            "optimization_recommendations": [],
            "parameter_adjustments": parameter_result.get("improvements_made", []),
            "patterns_discovered": len(pattern_result.get("patterns_found", [])),
            "modules_analyzed": len(performance_data)
        }
        
        # Calculate learning effectiveness
        total_opportunities = sum(
            len(module_data.get("learning_opportunities", [])) 
            for module_data in performance_data.values()
        )
        
        if total_opportunities > 0:
            improvement_opportunities = [
                {
                    "module": module,
                    "opportunities": module_data.get("learning_opportunities", [])
                }
                for module, module_data in performance_data.items()
                if module_data.get("learning_opportunities")
            ]
            synthesis["improvement_opportunities"] = improvement_opportunities
        
        # Extract optimization insights
        optimization_insights = optimization_analysis.get("insights", [])
        synthesis["optimization_recommendations"] = optimization_insights
        
        # Calculate overall effectiveness score
        pattern_score = min(1.0, len(pattern_result.get("patterns_found", [])) / 5)
        opportunity_score = min(1.0, total_opportunities / 10)
        parameter_score = parameter_result.get("optimization_score", 0.5)
        
        synthesis["learning_effectiveness"] = (pattern_score + opportunity_score + parameter_score) / 3
        
        return synthesis
    
    async def _synthesize_optimization_workflow(self, current_performance: Dict[str, Any], 
                                              opportunities: List[Dict[str, Any]], 
                                              learning_summary: Dict[str, Any]) -> Dict[str, Any]:
        """Synthesize optimization workflow results"""
        synthesis = {
            "optimization_potential": 0.0,
            "priority_actions": [],
            "performance_baseline": {},
            "improvement_targets": {},
            "learning_integration": learning_summary.get("learning_effectiveness", 0)
        }
        
        # Calculate baseline performance
        for module, analysis in current_performance.items():
            quality_score = analysis.get("quality_score", 0)
            synthesis["performance_baseline"][module] = quality_score
        
        # Prioritize opportunities
        high_priority = [opp for opp in opportunities if opp.get("priority") == "high"]
        medium_priority = [opp for opp in opportunities if opp.get("priority") == "medium"]
        
        synthesis["priority_actions"] = high_priority + medium_priority[:3]  # Top 3 medium priority
        
        # Set improvement targets
        for module, baseline in synthesis["performance_baseline"].items():
            if baseline < 0.8:
                synthesis["improvement_targets"][module] = min(1.0, baseline + 0.2)
            else:
                synthesis["improvement_targets"][module] = min(1.0, baseline + 0.1)
        
        # Calculate optimization potential
        if synthesis["performance_baseline"]:
            avg_baseline = sum(synthesis["performance_baseline"].values()) / len(synthesis["performance_baseline"])
            avg_target = sum(synthesis["improvement_targets"].values()) / len(synthesis["improvement_targets"])
            synthesis["optimization_potential"] = avg_target - avg_baseline
        
        return synthesis
    
    async def _synthesize_anomaly_investigation(self, anomaly_analysis: Dict[str, Any], 
                                              all_results: Dict[str, Any], 
                                              investigation_scope: str) -> Dict[str, Any]:
        """Synthesize anomaly investigation results"""
        synthesis = {
            "anomaly_severity": "unknown",
            "root_cause_analysis": [],
            "impact_assessment": {},
            "mitigation_strategies": [],
            "monitoring_recommendations": []
        }
        
        # Determine severity
        anomalies = anomaly_analysis.get("anomalies", [])
        if anomalies:
            max_severity = max(anomaly.get("severity", 0) for anomaly in anomalies)
            if max_severity > 0.8:
                synthesis["anomaly_severity"] = "critical"
            elif max_severity > 0.6:
                synthesis["anomaly_severity"] = "high"
            elif max_severity > 0.4:
                synthesis["anomaly_severity"] = "medium"
            else:
                synthesis["anomaly_severity"] = "low"
        
        # Extract root cause insights
        for anomaly in anomalies:
            synthesis["root_cause_analysis"].append({
                "type": anomaly.get("type", "unknown"),
                "description": anomaly.get("description", ""),
                "confidence": anomaly.get("confidence", 0)
            })
        
        # Impact assessment
        if "risk_assessment" in all_results:
            risk_data = all_results["risk_assessment"]
            synthesis["impact_assessment"] = {
                "risk_level": risk_data.get("risk_level", "unknown"),
                "risk_factors": risk_data.get("risk_factors", [])
            }
        
        # Mitigation strategies
        for anomaly in anomalies:
            synthesis["mitigation_strategies"].extend(anomaly.get("recommended_actions", []))
        
        # Remove duplicates
        synthesis["mitigation_strategies"] = list(set(synthesis["mitigation_strategies"]))
        
        return synthesis
    
    async def _generate_strategic_recommendations(self, current_state: Dict[str, Any], 
                                                opportunities: List[Dict[str, Any]], 
                                                planning_horizon: str, 
                                                focus_areas: List[str]) -> List[Dict[str, Any]]:
        """Generate strategic recommendations"""
        recommendations = []
        
        # Learning-focused recommendations
        if "learning" in focus_areas:
            learning_effectiveness = current_state.get("learning", {}).get("learning_effectiveness", 0.5)
            
            if learning_effectiveness < 0.7:
                recommendations.append({
                    "area": "learning",
                    "recommendation": "Enhance learning agent capabilities and feedback mechanisms",
                    "priority": "high",
                    "horizon": planning_horizon,
                    "expected_impact": "improved_system_adaptability"
                })
        
        # Trading-focused recommendations
        if "trading" in focus_areas:
            recommendations.append({
                "area": "trading",
                "recommendation": "Implement advanced risk management strategies",
                "priority": "medium",
                "horizon": planning_horizon,
                "expected_impact": "reduced_portfolio_risk"
            })
        
        # Optimization-focused recommendations
        if "optimization" in focus_areas:
            performance_analysis = current_state.get("performance", {})
            quality_score = performance_analysis.get("quality_score", 0.5)
            
            if quality_score < 0.8:
                recommendations.append({
                    "area": "optimization",
                    "recommendation": "Implement systematic performance monitoring and optimization",
                    "priority": "high",
                    "horizon": planning_horizon,
                    "expected_impact": "improved_system_efficiency"
                })
        
        # Opportunity-based recommendations
        for opportunity in opportunities[:3]:  # Top 3 opportunities
            recommendations.append({
                "area": opportunity.get("area", "general"),
                "recommendation": opportunity.get("opportunity", ""),
                "priority": opportunity.get("priority", "medium"),
                "horizon": planning_horizon,
                "expected_impact": opportunity.get("potential_impact", "unknown")
            })
        
        return recommendations
    
    async def _create_implementation_plan(self, recommendations: List[Dict[str, Any]], 
                                        planning_horizon: str) -> Dict[str, Any]:
        """Create implementation plan for strategic recommendations"""
        implementation_plan = {
            "timeline": {},
            "resource_requirements": {},
            "success_metrics": {},
            "dependencies": []
        }
        
        # Timeline based on horizon
        if planning_horizon == "short_term":
            phases = ["immediate", "1_month", "3_months"]
        elif planning_horizon == "medium_term":
            phases = ["3_months", "6_months", "12_months"]
        else:  # long_term
            phases = ["6_months", "12_months", "24_months"]
        
        # Distribute recommendations across phases
        high_priority = [r for r in recommendations if r.get("priority") == "high"]
        medium_priority = [r for r in recommendations if r.get("priority") == "medium"]
        low_priority = [r for r in recommendations if r.get("priority") == "low"]
        
        implementation_plan["timeline"][phases[0]] = high_priority[:2]  # Immediate high priority
        implementation_plan["timeline"][phases[1]] = high_priority[2:] + medium_priority[:2]
        implementation_plan["timeline"][phases[2]] = medium_priority[2:] + low_priority
        
        # Resource requirements (simplified)
        implementation_plan["resource_requirements"] = {
            "computational": "medium",
            "development_effort": "high" if len(high_priority) > 2 else "medium",
            "learning_data": "continuous"
        }
        
        # Success metrics
        implementation_plan["success_metrics"] = {
            "learning_effectiveness_improvement": 0.2,
            "system_performance_improvement": 0.15,
            "anomaly_detection_accuracy": 0.9,
            "user_satisfaction": 0.85
        }
        
        return implementation_plan
    
    async def _synthesize_strategic_planning(self, current_state: Dict[str, Any], 
                                           opportunities: List[Dict[str, Any]], 
                                           recommendations: List[Dict[str, Any]], 
                                           implementation_plan: Dict[str, Any]) -> Dict[str, Any]:
        """Synthesize strategic planning results"""
        synthesis = {
            "strategic_overview": {},
            "key_priorities": [],
            "success_probability": 0.0,
            "resource_efficiency": 0.0,
            "expected_outcomes": []
        }
        
        # Strategic overview
        synthesis["strategic_overview"] = {
            "current_maturity": current_state.get("learning", {}).get("learning_effectiveness", 0.5),
            "improvement_opportunities": len(opportunities),
            "strategic_initiatives": len(recommendations),
            "implementation_complexity": "high" if len(recommendations) > 5 else "medium"
        }
        
        # Key priorities
        high_priority_recs = [r for r in recommendations if r.get("priority") == "high"]
        synthesis["key_priorities"] = [
            {
                "area": rec.get("area"),
                "action": rec.get("recommendation"),
                "impact": rec.get("expected_impact")
            }
            for rec in high_priority_recs[:3]
        ]
        
        # Success probability (simplified calculation)
        learning_effectiveness = current_state.get("learning", {}).get("learning_effectiveness", 0.5)
        performance_quality = current_state.get("performance", {}).get("quality_score", 0.5)
        
        base_probability = (learning_effectiveness + performance_quality) / 2
        complexity_penalty = 0.1 if len(recommendations) > 5 else 0.05
        
        synthesis["success_probability"] = max(0.3, base_probability - complexity_penalty)
        
        # Resource efficiency
        high_impact_recs = [r for r in recommendations if "system" in r.get("expected_impact", "")]
        synthesis["resource_efficiency"] = min(1.0, len(high_impact_recs) / max(1, len(recommendations)))
        
        # Expected outcomes
        synthesis["expected_outcomes"] = [
            "Improved learning and adaptation capabilities",
            "Enhanced system performance and reliability",
            "Better anomaly detection and response",
            "Increased overall system intelligence"
        ]
        
        return synthesis
    
    async def _analyze_collaboration_effectiveness(self, workflow_id: str) -> Dict[str, Any]:
        """Analyze effectiveness of agent collaboration in workflow"""
        workflow_result = await self._get_workflow_result(workflow_id)
        
        analysis = {
            "collaboration_score": 0.0,
            "agent_synergy": {},
            "bottlenecks_identified": [],
            "optimization_suggestions": []
        }
        
        agents_involved = workflow_result.get("agents_involved", [])
        task_results = workflow_result.get("task_results", {})
        
        if len(agents_involved) < 2:
            analysis["collaboration_score"] = 0.5  # Single agent workflow
            return analysis
        
        # Calculate collaboration score based on task success and integration
        successful_tasks = sum(1 for result in task_results.values() if not result.get("error"))
        total_tasks = len(task_results)
        
        if total_tasks > 0:
            success_rate = successful_tasks / total_tasks
            agent_diversity = len(set(agents_involved)) / len(agents_involved)
            
            analysis["collaboration_score"] = (success_rate + agent_diversity) / 2
        
        # Analyze agent synergy
        for agent in set(agents_involved):
            agent_task_count = agents_involved.count(agent)
            analysis["agent_synergy"][agent] = {
                "utilization": agent_task_count / len(agents_involved),
                "contribution": "high" if agent_task_count > 1 else "medium"
            }
        
        # Identify potential bottlenecks
        if analysis["collaboration_score"] < 0.7:
            analysis["bottlenecks_identified"].append("Low task success rate")
        
        if len(set(agents_involved)) < 3:
            analysis["optimization_suggestions"].append("Consider involving more specialized agents")
        
        return analysis
    
    async def _update_learning_from_workflow(self, workflow_id: str, workflow_result: Dict[str, Any]):
        """Update learning agent with workflow results"""
        try:
            feedback_data = {
                "type": "workflow_feedback",
                "content": f"Workflow {workflow_id} completed with status {workflow_result.get('status')}",
                "context": {
                    "workflow_id": workflow_id,
                    "agents_involved": workflow_result.get("agents_involved", []),
                    "collaboration_score": workflow_result.get("collaboration_insights", {}).get("collaboration_score", 0.5)
                },
                "rating": 1.0 if workflow_result.get("status") == "COMPLETED" else 0.3
            }
            
            learning_task = {
                "type": "learn_from_feedback",
                "feedback_data": feedback_data
            }
            
            await self.agents["learning_agent"].handle_task(learning_task)
            
            logger.debug(f"[AGENT_COORDINATOR] Updated learning from workflow {workflow_id}")
            
        except Exception as e:
            logger.error(f"[AGENT_COORDINATOR] Failed to update learning from workflow {workflow_id}: {e}")
    
    async def get_coordination_status(self) -> Dict[str, Any]:
        """Get current coordination status and metrics"""
        with self.coordination_lock:
            active_workflows_info = {
                wf_id: {
                    "status": wf_data.get("status"),
                    "agents_involved": wf_data.get("agents_involved", []),
                    "start_time": wf_data.get("start_time")
                }
                for wf_id, wf_data in self.active_workflows.items()
            }
        
        # Calculate performance metrics
        recent_workflows = self.collaboration_history[-10:] if self.collaboration_history else []
        
        if recent_workflows:
            success_rate = sum(1 for wf in recent_workflows if wf.get("status") == "COMPLETED") / len(recent_workflows)
            avg_collaboration_score = sum(
                wf.get("collaboration_insights", {}).get("collaboration_score", 0.5) 
                for wf in recent_workflows
            ) / len(recent_workflows)
        else:
            success_rate = 0.0
            avg_collaboration_score = 0.5
        
        return {
            "coordinator_id": self.coordinator_id,
            "registered_agents": list(self.agents.keys()),
            "active_workflows": len(self.active_workflows),
            "workflow_details": active_workflows_info,
            "collaboration_history_size": len(self.collaboration_history),
            "performance_metrics": {
                "workflow_success_rate": success_rate,
                "avg_collaboration_score": avg_collaboration_score,
                "total_workflows_completed": len(self.collaboration_history)
            },
            "config": self.config
        }
    
    async def handle_task(self, task: Dict[str, Any]) -> Dict[str, Any]:
        """Handle tasks assigned to the coordinator"""
        task_type = task.get("type")
        
        if task_type == "execute_workflow":
            workflow_definition = task.get("workflow_definition", {})
            return await self.execute_collaborative_workflow(workflow_definition)
        
        elif task_type == "get_coordination_status":
            return await self.get_coordination_status()
        
        elif task_type == "analyze_collaboration":
            workflow_id = task.get("workflow_id")
            if workflow_id:
                return await self._analyze_collaboration_effectiveness(workflow_id)
            else:
                return {"error": "workflow_id required"}
        
        else:
            return {"error": f"Unknown task type: {task_type}"}


# Global instance
_agent_coordinator = None


def get_agent_coordinator() -> AgentCoordinator:
    """Get the global agent coordinator instance"""
    global _agent_coordinator
    if _agent_coordinator is None:
        _agent_coordinator = AgentCoordinator()
    return _agent_coordinator


async def initialize_multi_agent_system():
    """Initialize the complete multi-agent system"""
    coordinator = get_agent_coordinator()
    await coordinator.initialize_agents()
    return coordinator


if __name__ == "__main__":
    async def test_coordinator():
        coordinator = await initialize_multi_agent_system()
        
        # Test comprehensive market analysis workflow
        market_workflow = {
            "type": "comprehensive_market_analysis",
            "data": {
                "market_data": {
                    "AAPL": {"close": 150, "volume": 1000000},
                    "GOOGL": {"close": 2800, "volume": 500000}
                },
                "symbols": ["AAPL", "GOOGL"],
                "analysis_depth": "comprehensive"
            },
            "goals": ["identify_opportunities", "assess_risk", "generate_signals"]
        }
        
        result = await coordinator.execute_collaborative_workflow(market_workflow)
        print("Market Analysis Workflow Result:")
        print(json.dumps(result, indent=2, default=str))
        
        # Get coordination status
        status = await coordinator.get_coordination_status()
        print("\nCoordination Status:")
        print(json.dumps(status, indent=2, default=str))
    
    asyncio.run(test_coordinator())

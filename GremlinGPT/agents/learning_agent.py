#!/usr/bin/env python3

# ─────────────────────────────────────────────────────────────
# ⚠️ GremlinGPT Fair Use Only | Commercial Use Requires License
# Built under the GremlinGPT Dual License v1.0
# © 2025 StatikFintechLLC / AscendAI Project
# Contact: ascend.gremlin@gmail.com
# ─────────────────────────────────────────────────────────────

# GremlinGPT v1.0.3 :: Specialized Agent - Learning & Self-Improvement

import asyncio
import numpy as np
import json
from datetime import datetime, timezone, timedelta
from pathlib import Path
import sys
import pickle
from typing import Dict, List, Any, Optional, Tuple
import statistics
from dataclasses import dataclass
from collections import defaultdict
import re

# Add project root to path for imports
project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root))

from backend.globals import CFG
from utils.logging_config import setup_module_logger
from memory.log_history import log_event
from memory.vector_store import embedder
from agent_core.task_queue import enqueue_task

logger = setup_module_logger("agents", "learning_agent")


@dataclass
class LearningGoal:
    """Learning objective with metrics"""
    goal_id: str
    description: str
    target_metric: str
    current_value: float
    target_value: float
    improvement_strategies: List[str]
    priority: float
    deadline: Optional[datetime]


@dataclass
class PerformanceMetric:
    """Performance tracking metric"""
    metric_name: str
    current_value: float
    historical_values: List[Tuple[datetime, float]]
    trend: str  # "improving", "declining", "stable"
    confidence: float


class LearningAgent:
    """
    Specialized Agent for Learning and Self-Improvement
    
    Capabilities:
    - Continuous performance monitoring
    - Adaptive learning from failures and successes
    - Strategy optimization and refinement
    - Knowledge base expansion
    - Self-modification and improvement
    - Cross-module learning integration
    """
    
    def __init__(self):
        self.agent_id = f"learning_agent_{datetime.now().strftime('%Y%m%d_%H%M%S')}"
        self.capabilities = [
            "performance_monitoring",
            "adaptive_learning",
            "strategy_optimization",
            "knowledge_expansion",
            "self_modification",
            "pattern_discovery",
            "meta_learning"
        ]
        
        self.learning_goals = {}
        self.performance_metrics = {}
        self.learning_history = []
        self.knowledge_base = {}
        self.improvement_strategies = {}
        
        # Learning configuration
        self.config = CFG.get("learning_agent", {
            "learning_rate": 0.01,
            "exploration_rate": 0.1,
            "memory_retention_days": 90,
            "performance_window": 50,
            "improvement_threshold": 0.05,
            "max_learning_history": 1000
        })
        
        # Learning models directory
        self.models_dir = Path("memory/learning_models")
        self.models_dir.mkdir(parents=True, exist_ok=True)
        
        logger.info(f"[LEARNING_AGENT] Initialized agent: {self.agent_id}")
    
    async def monitor_performance(self, module_name: str, metrics: Dict[str, float]) -> Dict[str, Any]:
        """Monitor and analyze performance metrics for a module"""
        timestamp = datetime.now(timezone.utc)
        
        analysis_result = {
            "module": module_name,
            "timestamp": timestamp.isoformat(),
            "metrics_analyzed": len(metrics),
            "performance_changes": {},
            "recommendations": [],
            "learning_opportunities": []
        }
        
        try:
            for metric_name, value in metrics.items():
                metric_key = f"{module_name}.{metric_name}"
                
                # Update or create performance metric
                if metric_key not in self.performance_metrics:
                    self.performance_metrics[metric_key] = PerformanceMetric(
                        metric_name=metric_key,
                        current_value=value,
                        historical_values=[(timestamp, value)],
                        trend="stable",
                        confidence=0.5
                    )
                else:
                    perf_metric = self.performance_metrics[metric_key]
                    perf_metric.historical_values.append((timestamp, value))
                    
                    # Keep only recent history
                    cutoff_date = timestamp - timedelta(days=self.config["memory_retention_days"])
                    perf_metric.historical_values = [
                        (ts, val) for ts, val in perf_metric.historical_values 
                        if ts > cutoff_date
                    ]
                    
                    # Analyze trend
                    old_value = perf_metric.current_value
                    perf_metric.current_value = value
                    
                    trend_analysis = self._analyze_trend(perf_metric.historical_values)
                    perf_metric.trend = trend_analysis["trend"]
                    perf_metric.confidence = trend_analysis["confidence"]
                    
                    # Track performance change
                    if old_value != 0:
                        change_percent = ((value - old_value) / old_value) * 100
                        analysis_result["performance_changes"][metric_name] = {
                            "old_value": old_value,
                            "new_value": value,
                            "change_percent": change_percent,
                            "trend": perf_metric.trend
                        }
                        
                        # Identify learning opportunities
                        if abs(change_percent) > self.config["improvement_threshold"] * 100:
                            opportunity = {
                                "metric": metric_name,
                                "change": change_percent,
                                "type": "improvement" if change_percent > 0 else "degradation",
                                "recommended_action": self._suggest_improvement_action(metric_name, change_percent, perf_metric)
                            }
                            analysis_result["learning_opportunities"].append(opportunity)
            
            # Generate recommendations
            recommendations = self._generate_performance_recommendations(module_name, analysis_result)
            analysis_result["recommendations"] = recommendations
            
            # Update learning goals if needed
            await self._update_learning_goals(module_name, analysis_result)
            
            # Log performance monitoring
            log_event("learning_agent", "performance_monitored", {
                "module": module_name,
                "metrics_count": len(metrics),
                "opportunities_found": len(analysis_result["learning_opportunities"]),
                "recommendations_generated": len(recommendations)
            })
            
            logger.info(f"[LEARNING_AGENT] Monitored {module_name}: {len(analysis_result['learning_opportunities'])} opportunities identified")
            
        except Exception as e:
            logger.error(f"[LEARNING_AGENT] Performance monitoring failed for {module_name}: {e}")
            analysis_result["error"] = str(e)
        
        return analysis_result
    
    def _analyze_trend(self, historical_values: List[Tuple[datetime, float]]) -> Dict[str, Any]:
        """Analyze trend in historical performance data"""
        if len(historical_values) < 3:
            return {"trend": "stable", "confidence": 0.3}
        
        # Extract values and calculate trend
        values = [val for _, val in historical_values[-self.config["performance_window"]:]]
        
        if len(values) < 3:
            return {"trend": "stable", "confidence": 0.3}
        
        # Simple linear regression for trend
        n = len(values)
        x = list(range(n))
        y = values
        
        x_mean = sum(x) / n
        y_mean = sum(y) / n
        
        numerator = sum((x[i] - x_mean) * (y[i] - y_mean) for i in range(n))
        denominator = sum((x[i] - x_mean) ** 2 for i in range(n))
        
        if denominator == 0:
            return {"trend": "stable", "confidence": 0.5}
        
        slope = numerator / denominator
        
        # Calculate correlation coefficient for confidence
        y_variance = sum((y[i] - y_mean) ** 2 for i in range(n))
        if y_variance == 0:
            confidence = 0.5
        else:
            r_squared = (numerator ** 2) / (denominator * y_variance)
            confidence = min(1.0, r_squared)
        
        # Determine trend direction
        slope_threshold = statistics.stdev(values) * 0.1 if len(values) > 1 else 0.01
        
        if slope > slope_threshold:
            trend = "improving"
        elif slope < -slope_threshold:
            trend = "declining"
        else:
            trend = "stable"
        
        return {"trend": trend, "confidence": confidence, "slope": slope}
    
    def _suggest_improvement_action(self, metric_name: str, change_percent: float, 
                                  perf_metric: PerformanceMetric) -> str:
        """Suggest improvement actions based on metric changes"""
        if change_percent > 0:
            # Positive change - reinforce
            if "accuracy" in metric_name.lower() or "success" in metric_name.lower():
                return "Analyze successful patterns and apply to similar scenarios"
            elif "speed" in metric_name.lower() or "time" in metric_name.lower():
                return "Document optimization techniques for replication"
            else:
                return "Investigate and document improvement factors"
        else:
            # Negative change - correct
            if "error" in metric_name.lower() or "failure" in metric_name.lower():
                return "Implement error prevention and recovery mechanisms"
            elif "accuracy" in metric_name.lower():
                return "Review and retrain models with recent data"
            elif "speed" in metric_name.lower():
                return "Profile and optimize performance bottlenecks"
            else:
                return "Investigate root cause and implement corrective measures"
    
    def _generate_performance_recommendations(self, module_name: str, 
                                           analysis_result: Dict[str, Any]) -> List[str]:
        """Generate actionable recommendations based on performance analysis"""
        recommendations = []
        
        opportunities = analysis_result.get("learning_opportunities", [])
        
        # Group opportunities by type
        improvements = [opp for opp in opportunities if opp["type"] == "improvement"]
        degradations = [opp for opp in opportunities if opp["type"] == "degradation"]
        
        if improvements:
            recommendations.append(f"Leverage {len(improvements)} positive performance changes for knowledge transfer")
            
            # Specific recommendations for improvements
            for improvement in improvements[:3]:  # Top 3
                recommendations.append(f"Study improvement in {improvement['metric']} (+{improvement['change']:.1f}%)")
        
        if degradations:
            recommendations.append(f"Address {len(degradations)} performance degradations immediately")
            
            # Specific recommendations for degradations
            for degradation in degradations[:3]:  # Top 3
                recommendations.append(f"Fix degradation in {degradation['metric']} ({degradation['change']:.1f}%)")
        
        # Module-specific recommendations
        if module_name == "trading_core":
            if any("accuracy" in opp["metric"] for opp in degradations):
                recommendations.append("Review and update trading algorithms with recent market data")
            if any("profit" in opp["metric"] for opp in improvements):
                recommendations.append("Scale successful trading strategies across portfolio")
        
        elif module_name == "scraper":
            if any("success_rate" in opp["metric"] for opp in degradations):
                recommendations.append("Update scraping patterns and error handling")
            if any("speed" in opp["metric"] for opp in improvements):
                recommendations.append("Apply performance optimizations to other scrapers")
        
        elif module_name == "nlp_engine":
            if any("accuracy" in opp["metric"] for opp in degradations):
                recommendations.append("Retrain NLP models with recent data and feedback")
        
        return recommendations
    
    async def _update_learning_goals(self, module_name: str, analysis_result: Dict[str, Any]):
        """Update learning goals based on performance analysis"""
        opportunities = analysis_result.get("learning_opportunities", [])
        
        for opportunity in opportunities:
            if opportunity["type"] == "degradation":
                # Create learning goal to address degradation
                goal_id = f"fix_{module_name}_{opportunity['metric']}_{datetime.now().strftime('%Y%m%d')}"
                
                if goal_id not in self.learning_goals:
                    self.learning_goals[goal_id] = LearningGoal(
                        goal_id=goal_id,
                        description=f"Improve {opportunity['metric']} in {module_name}",
                        target_metric=opportunity['metric'],
                        current_value=opportunity.get('new_value', 0),
                        target_value=opportunity.get('old_value', 0),
                        improvement_strategies=[opportunity['recommended_action']],
                        priority=min(1.0, abs(opportunity['change']) / 100),
                        deadline=datetime.now(timezone.utc) + timedelta(days=7)
                    )
    
    async def learn_from_feedback(self, feedback_data: Dict[str, Any]) -> Dict[str, Any]:
        """Learn from user feedback and system outcomes"""
        learning_result = {
            "timestamp": datetime.now(timezone.utc).isoformat(),
            "feedback_processed": True,
            "patterns_discovered": [],
            "knowledge_updates": [],
            "strategy_adjustments": []
        }
        
        try:
            feedback_type = feedback_data.get("type", "general")
            feedback_content = feedback_data.get("content", "")
            context = feedback_data.get("context", {})
            rating = feedback_data.get("rating", 0)  # Numerical rating if available
            
            # Analyze feedback content
            patterns = await self._analyze_feedback_patterns(feedback_content, context)
            learning_result["patterns_discovered"] = patterns
            
            # Update knowledge base
            knowledge_updates = self._update_knowledge_base(feedback_type, feedback_content, patterns, rating)
            learning_result["knowledge_updates"] = knowledge_updates
            
            # Adjust strategies based on feedback
            strategy_adjustments = await self._adjust_strategies_from_feedback(feedback_data, patterns)
            learning_result["strategy_adjustments"] = strategy_adjustments
            
            # Store in learning history
            self.learning_history.append({
                "timestamp": datetime.now(timezone.utc),
                "type": "feedback_learning",
                "data": feedback_data,
                "result": learning_result
            })
            
            # Trim history if too large
            if len(self.learning_history) > self.config["max_learning_history"]:
                self.learning_history.pop(0)
            
            # Embed learning for future reference
            learning_text = f"Learned from {feedback_type} feedback: {len(patterns)} patterns discovered"
            vector = embedder.embed_text(learning_text)
            embedder.package_embedding(
                text=learning_text,
                vector=vector,
                meta={
                    "agent": "learning_agent",
                    "feedback_type": feedback_type,
                    "patterns_count": len(patterns),
                    "rating": rating,
                    "timestamp": datetime.now(timezone.utc).isoformat(),
                    "watermark": "source:GremlinGPT_LearningAgent"
                }
            )
            
            log_event("learning_agent", "feedback_processed", {
                "feedback_type": feedback_type,
                "patterns_discovered": len(patterns),
                "knowledge_updates": len(knowledge_updates),
                "rating": rating
            })
            
            logger.info(f"[LEARNING_AGENT] Processed {feedback_type} feedback: {len(patterns)} patterns, {len(knowledge_updates)} updates")
            
        except Exception as e:
            logger.error(f"[LEARNING_AGENT] Feedback learning failed: {e}")
            learning_result["error"] = str(e)
            learning_result["feedback_processed"] = False
        
        return learning_result
    
    async def _analyze_feedback_patterns(self, content: str, context: Dict[str, Any]) -> List[Dict[str, Any]]:
        """Analyze patterns in feedback content"""
        patterns = []
        
        # Text pattern analysis
        if content:
            # Sentiment patterns
            positive_words = ["good", "great", "excellent", "perfect", "amazing", "helpful", "useful", "accurate"]
            negative_words = ["bad", "poor", "terrible", "wrong", "inaccurate", "slow", "confusing", "useless"]
            
            content_lower = content.lower()
            positive_count = sum(1 for word in positive_words if word in content_lower)
            negative_count = sum(1 for word in negative_words if word in content_lower)
            
            if positive_count > negative_count:
                patterns.append({
                    "type": "sentiment",
                    "pattern": "positive_feedback",
                    "confidence": min(1.0, positive_count / (positive_count + negative_count + 1)),
                    "details": {"positive_words": positive_count, "negative_words": negative_count}
                })
            elif negative_count > positive_count:
                patterns.append({
                    "type": "sentiment",
                    "pattern": "negative_feedback",
                    "confidence": min(1.0, negative_count / (positive_count + negative_count + 1)),
                    "details": {"positive_words": positive_count, "negative_words": negative_count}
                })
            
            # Feature-specific feedback patterns
            feature_keywords = {
                "speed": ["fast", "slow", "quick", "time", "speed", "performance"],
                "accuracy": ["accurate", "wrong", "correct", "precise", "error", "mistake"],
                "usability": ["easy", "difficult", "confusing", "intuitive", "user-friendly"],
                "reliability": ["reliable", "stable", "crash", "bug", "fail", "consistent"]
            }
            
            for feature, keywords in feature_keywords.items():
                feature_mentions = sum(1 for keyword in keywords if keyword in content_lower)
                if feature_mentions > 0:
                    patterns.append({
                        "type": "feature_feedback",
                        "pattern": f"{feature}_mentioned",
                        "confidence": min(1.0, feature_mentions / len(keywords)),
                        "details": {"mentions": feature_mentions, "feature": feature}
                    })
        
        # Context patterns
        if context:
            # Module-specific patterns
            if "module" in context:
                patterns.append({
                    "type": "module_specific",
                    "pattern": f"feedback_for_{context['module']}",
                    "confidence": 1.0,
                    "details": {"module": context["module"]}
                })
            
            # Task-specific patterns
            if "task_type" in context:
                patterns.append({
                    "type": "task_specific",
                    "pattern": f"feedback_for_{context['task_type']}",
                    "confidence": 1.0,
                    "details": {"task_type": context["task_type"]}
                })
        
        return patterns
    
    def _update_knowledge_base(self, feedback_type: str, content: str, 
                              patterns: List[Dict[str, Any]], rating: float) -> List[str]:
        """Update knowledge base with new insights"""
        updates = []
        
        # Create knowledge key
        knowledge_key = f"{feedback_type}_knowledge"
        
        if knowledge_key not in self.knowledge_base:
            self.knowledge_base[knowledge_key] = {
                "feedback_count": 0,
                "average_rating": 0.0,
                "common_patterns": {},
                "improvement_areas": [],
                "success_factors": []
            }
        
        kb_section = self.knowledge_base[knowledge_key]
        
        # Update statistics
        old_count = kb_section["feedback_count"]
        old_avg = kb_section["average_rating"]
        
        kb_section["feedback_count"] += 1
        kb_section["average_rating"] = (old_avg * old_count + rating) / kb_section["feedback_count"]
        
        updates.append(f"Updated {feedback_type} feedback statistics")
        
        # Update pattern frequency
        for pattern in patterns:
            pattern_key = f"{pattern['type']}:{pattern['pattern']}"
            if pattern_key not in kb_section["common_patterns"]:
                kb_section["common_patterns"][pattern_key] = {"count": 0, "avg_confidence": 0.0}
            
            pattern_info = kb_section["common_patterns"][pattern_key]
            old_pattern_count = pattern_info["count"]
            old_pattern_conf = pattern_info["avg_confidence"]
            
            pattern_info["count"] += 1
            pattern_info["avg_confidence"] = (old_pattern_conf * old_pattern_count + pattern["confidence"]) / pattern_info["count"]
            
            updates.append(f"Updated pattern frequency: {pattern_key}")
        
        # Identify improvement areas from negative feedback
        if rating < 0.5:  # Negative feedback
            negative_patterns = [p for p in patterns if p.get("pattern") == "negative_feedback"]
            for pattern in negative_patterns:
                feature = pattern.get("details", {}).get("feature", "general")
                if feature not in kb_section["improvement_areas"]:
                    kb_section["improvement_areas"].append(feature)
                    updates.append(f"Identified improvement area: {feature}")
        
        # Identify success factors from positive feedback
        elif rating > 0.7:  # Positive feedback
            positive_patterns = [p for p in patterns if p.get("pattern") == "positive_feedback"]
            for pattern in positive_patterns:
                feature = pattern.get("details", {}).get("feature", "general")
                if feature not in kb_section["success_factors"]:
                    kb_section["success_factors"].append(feature)
                    updates.append(f"Identified success factor: {feature}")
        
        return updates
    
    async def _adjust_strategies_from_feedback(self, feedback_data: Dict[str, Any], 
                                             patterns: List[Dict[str, Any]]) -> List[str]:
        """Adjust improvement strategies based on feedback"""
        adjustments = []
        
        rating = feedback_data.get("rating", 0)
        context = feedback_data.get("context", {})
        
        # Adjust exploration vs exploitation based on feedback
        if rating > 0.7:  # Good feedback - exploit current strategies
            old_exploration = self.config["exploration_rate"]
            self.config["exploration_rate"] = max(0.05, old_exploration * 0.9)
            adjustments.append(f"Reduced exploration rate from {old_exploration:.3f} to {self.config['exploration_rate']:.3f}")
        
        elif rating < 0.3:  # Poor feedback - explore more
            old_exploration = self.config["exploration_rate"]
            self.config["exploration_rate"] = min(0.3, old_exploration * 1.1)
            adjustments.append(f"Increased exploration rate from {old_exploration:.3f} to {self.config['exploration_rate']:.3f}")
        
        # Module-specific strategy adjustments
        if "module" in context:
            module = context["module"]
            strategy_key = f"{module}_strategy"
            
            if strategy_key not in self.improvement_strategies:
                self.improvement_strategies[strategy_key] = {
                    "focus_areas": [],
                    "success_patterns": [],
                    "avoid_patterns": []
                }
            
            strategy = self.improvement_strategies[strategy_key]
            
            # Update based on patterns
            for pattern in patterns:
                if pattern["type"] == "feature_feedback":
                    feature = pattern["details"]["feature"]
                    
                    if rating > 0.7 and feature not in strategy["success_patterns"]:
                        strategy["success_patterns"].append(feature)
                        adjustments.append(f"Added {feature} to success patterns for {module}")
                    
                    elif rating < 0.3 and feature not in strategy["avoid_patterns"]:
                        strategy["avoid_patterns"].append(feature)
                        adjustments.append(f"Added {feature} to avoid patterns for {module}")
        
        return adjustments
    
    async def discover_patterns(self, data_sources: List[str], 
                              analysis_type: str = "correlation") -> Dict[str, Any]:
        """Discover patterns across multiple data sources"""
        discovery_result = {
            "timestamp": datetime.now(timezone.utc).isoformat(),
            "analysis_type": analysis_type,
            "data_sources": data_sources,
            "patterns_found": [],
            "correlations": {},
            "recommendations": []
        }
        
        try:
            if analysis_type == "correlation":
                correlations = await self._discover_correlations(data_sources)
                discovery_result["correlations"] = correlations
                discovery_result["patterns_found"] = self._extract_patterns_from_correlations(correlations)
            
            elif analysis_type == "temporal":
                temporal_patterns = await self._discover_temporal_patterns(data_sources)
                discovery_result["patterns_found"] = temporal_patterns
            
            elif analysis_type == "anomaly":
                anomaly_patterns = await self._discover_anomaly_patterns(data_sources)
                discovery_result["patterns_found"] = anomaly_patterns
            
            # Generate recommendations based on patterns
            recommendations = self._generate_pattern_recommendations(discovery_result["patterns_found"])
            discovery_result["recommendations"] = recommendations
            
            # Save discovered patterns
            await self._save_discovered_patterns(discovery_result)
            
            logger.info(f"[LEARNING_AGENT] Pattern discovery complete: {len(discovery_result['patterns_found'])} patterns found")
            
        except Exception as e:
            logger.error(f"[LEARNING_AGENT] Pattern discovery failed: {e}")
            discovery_result["error"] = str(e)
        
        return discovery_result
    
    async def _discover_correlations(self, data_sources: List[str]) -> Dict[str, Any]:
        """Discover correlations between different metrics"""
        correlations = {}
        
        # Collect metric data from different sources
        metric_data = {}
        
        for source in data_sources:
            if source in self.performance_metrics:
                for metric_name, metric in self.performance_metrics.items():
                    if metric_name.startswith(source):
                        values = [val for _, val in metric.historical_values[-20:]]  # Last 20 values
                        if len(values) >= 5:  # Minimum data points
                            metric_data[metric_name] = values
        
        # Calculate correlations between metrics
        metric_names = list(metric_data.keys())
        
        for i, metric1 in enumerate(metric_names):
            for j, metric2 in enumerate(metric_names[i+1:], i+1):
                if len(metric_data[metric1]) == len(metric_data[metric2]) and len(metric_data[metric1]) >= 5:
                    try:
                        correlation = np.corrcoef(metric_data[metric1], metric_data[metric2])[0, 1]
                        if not np.isnan(correlation) and abs(correlation) > 0.5:
                            correlations[f"{metric1} vs {metric2}"] = {
                                "correlation": correlation,
                                "strength": "strong" if abs(correlation) > 0.8 else "moderate",
                                "direction": "positive" if correlation > 0 else "negative"
                            }
                    except:
                        continue
        
        return correlations
    
    def _extract_patterns_from_correlations(self, correlations: Dict[str, Any]) -> List[Dict[str, Any]]:
        """Extract actionable patterns from correlation analysis"""
        patterns = []
        
        for corr_name, corr_data in correlations.items():
            if corr_data["strength"] == "strong":
                pattern = {
                    "type": "correlation",
                    "description": f"Strong {corr_data['direction']} correlation between {corr_name}",
                    "confidence": abs(corr_data["correlation"]),
                    "actionability": "high" if abs(corr_data["correlation"]) > 0.8 else "medium",
                    "recommendation": self._generate_correlation_recommendation(corr_name, corr_data)
                }
                patterns.append(pattern)
        
        return patterns
    
    def _generate_correlation_recommendation(self, corr_name: str, corr_data: Dict[str, Any]) -> str:
        """Generate recommendation based on correlation"""
        direction = corr_data["direction"]
        metrics = corr_name.split(" vs ")
        
        if direction == "positive":
            return f"Improving {metrics[0]} should also improve {metrics[1]}"
        else:
            return f"Improving {metrics[0]} may negatively impact {metrics[1]} - balance optimization"
    
    async def _discover_temporal_patterns(self, data_sources: List[str]) -> List[Dict[str, Any]]:
        """Discover temporal patterns in data"""
        patterns = []
        
        for source in data_sources:
            source_metrics = {name: metric for name, metric in self.performance_metrics.items() 
                            if name.startswith(source)}
            
            for metric_name, metric in source_metrics.items():
                if len(metric.historical_values) >= 10:
                    # Analyze for cyclical patterns
                    timestamps = [ts for ts, _ in metric.historical_values]
                    values = [val for _, val in metric.historical_values]
                    
                    # Check for daily patterns (if timestamps span multiple days)
                    daily_pattern = self._check_daily_pattern(timestamps, values)
                    if daily_pattern["detected"]:
                        patterns.append({
                            "type": "temporal_daily",
                            "metric": metric_name,
                            "description": f"Daily pattern detected in {metric_name}",
                            "confidence": daily_pattern["confidence"],
                            "pattern_details": daily_pattern
                        })
                    
                    # Check for weekly patterns
                    if len(timestamps) >= 14:  # At least 2 weeks of data
                        weekly_pattern = self._check_weekly_pattern(timestamps, values)
                        if weekly_pattern["detected"]:
                            patterns.append({
                                "type": "temporal_weekly",
                                "metric": metric_name,
                                "description": f"Weekly pattern detected in {metric_name}",
                                "confidence": weekly_pattern["confidence"],
                                "pattern_details": weekly_pattern
                            })
        
        return patterns
    
    def _check_daily_pattern(self, timestamps: List[datetime], values: List[float]) -> Dict[str, Any]:
        """Check for daily patterns in temporal data"""
        # Group data by hour of day
        hourly_data = defaultdict(list)
        
        for ts, val in zip(timestamps, values):
            hour = ts.hour
            hourly_data[hour].append(val)
        
        # Calculate average for each hour
        hourly_averages = {}
        for hour, vals in hourly_data.items():
            if len(vals) >= 2:  # Need at least 2 data points
                hourly_averages[hour] = statistics.mean(vals)
        
        if len(hourly_averages) < 6:  # Need data from at least 6 different hours
            return {"detected": False, "confidence": 0.0}
        
        # Check for significant variation across hours
        avg_values = list(hourly_averages.values())
        if len(avg_values) < 2:
            return {"detected": False, "confidence": 0.0}
        
        variation = statistics.stdev(avg_values) / statistics.mean(avg_values) if statistics.mean(avg_values) != 0 else 0
        
        detected = variation > 0.1  # 10% variation threshold
        confidence = min(1.0, variation) if detected else 0.0
        
        return {
            "detected": detected,
            "confidence": confidence,
            "hourly_averages": hourly_averages,
            "variation": variation
        }
    
    def _check_weekly_pattern(self, timestamps: List[datetime], values: List[float]) -> Dict[str, Any]:
        """Check for weekly patterns in temporal data"""
        # Group data by day of week (0=Monday, 6=Sunday)
        daily_data = defaultdict(list)
        
        for ts, val in zip(timestamps, values):
            day_of_week = ts.weekday()
            daily_data[day_of_week].append(val)
        
        # Calculate average for each day
        daily_averages = {}
        for day, vals in daily_data.items():
            if len(vals) >= 2:  # Need at least 2 data points
                daily_averages[day] = statistics.mean(vals)
        
        if len(daily_averages) < 5:  # Need data from at least 5 different days
            return {"detected": False, "confidence": 0.0}
        
        # Check for significant variation across days
        avg_values = list(daily_averages.values())
        if len(avg_values) < 2:
            return {"detected": False, "confidence": 0.0}
        
        variation = statistics.stdev(avg_values) / statistics.mean(avg_values) if statistics.mean(avg_values) != 0 else 0
        
        detected = variation > 0.15  # 15% variation threshold for weekly patterns
        confidence = min(1.0, variation) if detected else 0.0
        
        return {
            "detected": detected,
            "confidence": confidence,
            "daily_averages": daily_averages,
            "variation": variation
        }
    
    async def _discover_anomaly_patterns(self, data_sources: List[str]) -> List[Dict[str, Any]]:
        """Discover patterns in anomalies and outliers"""
        patterns = []
        
        for source in data_sources:
            source_metrics = {name: metric for name, metric in self.performance_metrics.items() 
                            if name.startswith(source)}
            
            for metric_name, metric in source_metrics.items():
                if len(metric.historical_values) >= 20:
                    values = [val for _, val in metric.historical_values]
                    
                    # Statistical outlier detection
                    mean_val = statistics.mean(values)
                    std_val = statistics.stdev(values) if len(values) > 1 else 0
                    
                    if std_val > 0:
                        outliers = []
                        for i, val in enumerate(values):
                            z_score = abs((val - mean_val) / std_val)
                            if z_score > 2.5:  # More than 2.5 standard deviations
                                outliers.append({"index": i, "value": val, "z_score": z_score})
                        
                        if len(outliers) > 0:
                            outlier_rate = len(outliers) / len(values)
                            
                            pattern = {
                                "type": "anomaly_statistical",
                                "metric": metric_name,
                                "description": f"Statistical outliers detected in {metric_name}",
                                "confidence": min(1.0, outlier_rate * 10),  # Scale outlier rate
                                "outlier_count": len(outliers),
                                "outlier_rate": outlier_rate,
                                "outliers": outliers[:5]  # First 5 outliers
                            }
                            patterns.append(pattern)
        
        return patterns
    
    def _generate_pattern_recommendations(self, patterns: List[Dict[str, Any]]) -> List[str]:
        """Generate recommendations based on discovered patterns"""
        recommendations = []
        
        for pattern in patterns:
            pattern_type = pattern.get("type", "")
            
            if pattern_type == "correlation":
                recommendations.append(pattern.get("recommendation", ""))
            
            elif pattern_type.startswith("temporal"):
                metric = pattern.get("metric", "unknown")
                recommendations.append(f"Leverage {pattern_type.split('_')[1]} patterns in {metric} for predictive optimization")
            
            elif pattern_type.startswith("anomaly"):
                metric = pattern.get("metric", "unknown")
                outlier_rate = pattern.get("outlier_rate", 0)
                if outlier_rate > 0.1:  # More than 10% outliers
                    recommendations.append(f"Investigate and address high anomaly rate ({outlier_rate:.1%}) in {metric}")
                else:
                    recommendations.append(f"Monitor outlier patterns in {metric} for early warning system")
        
        # Remove duplicates and empty recommendations
        recommendations = list(set([rec for rec in recommendations if rec.strip()]))
        
        return recommendations
    
    async def _save_discovered_patterns(self, discovery_result: Dict[str, Any]):
        """Save discovered patterns for future reference"""
        try:
            patterns_file = self.models_dir / f"patterns_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
            
            with open(patterns_file, 'w') as f:
                json.dump(discovery_result, f, indent=2, default=str)
            
            logger.debug(f"[LEARNING_AGENT] Saved patterns to {patterns_file}")
            
        except Exception as e:
            logger.error(f"[LEARNING_AGENT] Failed to save patterns: {e}")
    
    async def optimize_learning_parameters(self) -> Dict[str, Any]:
        """Optimize learning parameters based on performance history"""
        optimization_result = {
            "timestamp": datetime.now(timezone.utc).isoformat(),
            "old_parameters": self.config.copy(),
            "new_parameters": {},
            "optimization_score": 0.0,
            "improvements_made": []
        }
        
        try:
            # Analyze recent learning effectiveness
            recent_history = self.learning_history[-50:] if self.learning_history else []
            
            if len(recent_history) >= 10:
                # Calculate learning effectiveness metrics
                effectiveness_score = self._calculate_learning_effectiveness(recent_history)
                
                # Optimize exploration rate
                if effectiveness_score < 0.6:
                    # Increase exploration for better learning
                    new_exploration = min(0.3, self.config["exploration_rate"] * 1.2)
                    optimization_result["improvements_made"].append("Increased exploration rate for better learning")
                elif effectiveness_score > 0.8:
                    # Decrease exploration to exploit current knowledge
                    new_exploration = max(0.05, self.config["exploration_rate"] * 0.9)
                    optimization_result["improvements_made"].append("Decreased exploration rate to exploit knowledge")
                else:
                    new_exploration = self.config["exploration_rate"]
                
                self.config["exploration_rate"] = new_exploration
                
                # Optimize learning rate
                if effectiveness_score < 0.5:
                    # Increase learning rate for faster adaptation
                    new_learning_rate = min(0.05, self.config["learning_rate"] * 1.1)
                    optimization_result["improvements_made"].append("Increased learning rate for faster adaptation")
                else:
                    new_learning_rate = self.config["learning_rate"]
                
                self.config["learning_rate"] = new_learning_rate
                
                # Optimize performance window
                avg_data_points = sum(len(h.get("data", {}).get("patterns", [])) for h in recent_history) / len(recent_history)
                
                if avg_data_points > 30:
                    # Increase window for more stable analysis
                    new_window = min(100, self.config["performance_window"] + 10)
                    optimization_result["improvements_made"].append("Increased performance window for stability")
                elif avg_data_points < 10:
                    # Decrease window for faster response
                    new_window = max(20, self.config["performance_window"] - 10)
                    optimization_result["improvements_made"].append("Decreased performance window for responsiveness")
                else:
                    new_window = self.config["performance_window"]
                
                self.config["performance_window"] = new_window
                
                optimization_result["optimization_score"] = effectiveness_score
            
            optimization_result["new_parameters"] = self.config.copy()
            
            logger.info(f"[LEARNING_AGENT] Parameter optimization complete. Score: {optimization_result['optimization_score']:.2f}")
            
        except Exception as e:
            logger.error(f"[LEARNING_AGENT] Parameter optimization failed: {e}")
            optimization_result["error"] = str(e)
        
        return optimization_result
    
    def _calculate_learning_effectiveness(self, history: List[Dict[str, Any]]) -> float:
        """Calculate effectiveness of recent learning activities"""
        if not history:
            return 0.5  # Neutral score
        
        effectiveness_factors = []
        
        # Factor 1: Pattern discovery success rate
        pattern_discoveries = [h for h in history if h.get("type") == "pattern_discovery"]
        if pattern_discoveries:
            avg_patterns = sum(len(pd.get("result", {}).get("patterns_found", [])) for pd in pattern_discoveries) / len(pattern_discoveries)
            pattern_score = min(1.0, avg_patterns / 5)  # Normalize to 5 patterns as max
            effectiveness_factors.append(pattern_score)
        
        # Factor 2: Feedback processing quality
        feedback_processing = [h for h in history if h.get("type") == "feedback_learning"]
        if feedback_processing:
            avg_updates = sum(len(fp.get("result", {}).get("knowledge_updates", [])) for fp in feedback_processing) / len(feedback_processing)
            feedback_score = min(1.0, avg_updates / 3)  # Normalize to 3 updates as max
            effectiveness_factors.append(feedback_score)
        
        # Factor 3: Strategy adjustment impact
        performance_monitoring = [h for h in history if h.get("type") == "performance_monitoring"]
        if performance_monitoring:
            avg_opportunities = sum(len(pm.get("result", {}).get("learning_opportunities", [])) for pm in performance_monitoring) / len(performance_monitoring)
            performance_score = min(1.0, avg_opportunities / 2)  # Normalize to 2 opportunities as max
            effectiveness_factors.append(performance_score)
        
        # Calculate weighted average
        if effectiveness_factors:
            return sum(effectiveness_factors) / len(effectiveness_factors)
        else:
            return 0.5  # Neutral score if no data
    
    async def get_learning_summary(self) -> Dict[str, Any]:
        """Get comprehensive summary of learning activities"""
        summary = {
            "agent_id": self.agent_id,
            "capabilities": self.capabilities,
            "learning_goals": len(self.learning_goals),
            "performance_metrics_tracked": len(self.performance_metrics),
            "learning_history_entries": len(self.learning_history),
            "knowledge_base_sections": len(self.knowledge_base),
            "improvement_strategies": len(self.improvement_strategies),
            "current_config": self.config.copy(),
            "recent_activities": [],
            "learning_effectiveness": 0.0
        }
        
        # Recent activities
        recent_history = self.learning_history[-10:] if self.learning_history else []
        for activity in recent_history:
            summary["recent_activities"].append({
                "timestamp": activity["timestamp"].isoformat(),
                "type": activity["type"],
                "summary": self._summarize_activity(activity)
            })
        
        # Learning effectiveness
        if recent_history:
            summary["learning_effectiveness"] = self._calculate_learning_effectiveness(recent_history)
        
        return summary
    
    def _summarize_activity(self, activity: Dict[str, Any]) -> str:
        """Create a summary of a learning activity"""
        activity_type = activity.get("type", "unknown")
        result = activity.get("result", {})
        
        if activity_type == "feedback_learning":
            patterns_count = len(result.get("patterns_discovered", []))
            updates_count = len(result.get("knowledge_updates", []))
            return f"Processed feedback: {patterns_count} patterns, {updates_count} updates"
        
        elif activity_type == "performance_monitoring":
            opportunities_count = len(result.get("learning_opportunities", []))
            recommendations_count = len(result.get("recommendations", []))
            return f"Monitored performance: {opportunities_count} opportunities, {recommendations_count} recommendations"
        
        elif activity_type == "pattern_discovery":
            patterns_count = len(result.get("patterns_found", []))
            return f"Discovered patterns: {patterns_count} patterns found"
        
        else:
            return f"Learning activity: {activity_type}"
    
    async def handle_task(self, task: Dict[str, Any]) -> Dict[str, Any]:
        """Handle tasks assigned to this agent"""
        task_type = task.get("type")
        
        if task_type == "monitor_performance":
            module_name = task.get("module_name", "unknown")
            metrics = task.get("metrics", {})
            return await self.monitor_performance(module_name, metrics)
        
        elif task_type == "learn_from_feedback":
            feedback_data = task.get("feedback_data", {})
            return await self.learn_from_feedback(feedback_data)
        
        elif task_type == "discover_patterns":
            data_sources = task.get("data_sources", [])
            analysis_type = task.get("analysis_type", "correlation")
            return await self.discover_patterns(data_sources, analysis_type)
        
        elif task_type == "optimize_parameters":
            return await self.optimize_learning_parameters()
        
        elif task_type == "get_learning_summary":
            return await self.get_learning_summary()
        
        else:
            return {"error": f"Unknown task type: {task_type}"}


# Global instance
_learning_agent = None


def get_learning_agent() -> LearningAgent:
    """Get the global learning agent instance"""
    global _learning_agent
    if _learning_agent is None:
        _learning_agent = LearningAgent()
    return _learning_agent


if __name__ == "__main__":
    async def test_agent():
        agent = LearningAgent()
        
        # Test performance monitoring
        test_metrics = {
            "accuracy": 0.85,
            "response_time": 1.2,
            "success_rate": 0.92
        }
        
        result = await agent.monitor_performance("test_module", test_metrics)
        print("Performance Monitoring Result:")
        print(json.dumps(result, indent=2, default=str))
        
        # Test feedback learning
        test_feedback = {
            "type": "user_feedback",
            "content": "The system is very accurate but quite slow",
            "context": {"module": "test_module", "task_type": "analysis"},
            "rating": 0.7
        }
        
        feedback_result = await agent.learn_from_feedback(test_feedback)
        print("\nFeedback Learning Result:")
        print(json.dumps(feedback_result, indent=2, default=str))
    
    asyncio.run(test_agent())

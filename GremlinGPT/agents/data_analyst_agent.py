#!/usr/bin/env python3

# ─────────────────────────────────────────────────────────────
# ⚠️ GremlinGPT Fair Use Only | Commercial Use Requires License
# Built under the GremlinGPT Dual License v1.0
# © 2025 StatikFintechLLC / AscendAI Project
# Contact: ascend.gremlin@gmail.com
# ─────────────────────────────────────────────────────────────

# GremlinGPT v1.0.3 :: Specialized Agent - Data Analysis & Anomaly Detection

import asyncio
import numpy as np
import pandas as pd
from datetime import datetime, timezone, timedelta
from pathlib import Path
import sys
import json
from typing import Dict, List, Any, Optional, Tuple
import statistics
import re
from dataclasses import dataclass

# Add project root to path for imports
project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root))

from backend.globals import CFG
from utils.logging_config import setup_module_logger
from memory.log_history import log_event
from memory.vector_store import embedder
from agent_core.task_queue import enqueue_task

logger = setup_module_logger("agents", "data_analyst")


@dataclass
class AnomalyReport:
    """Data structure for anomaly detection results"""
    anomaly_type: str
    severity: float  # 0.0 to 1.0
    description: str
    data_points: List[Any]
    confidence: float
    timestamp: datetime
    recommended_actions: List[str]


class DataAnalystAgent:
    """
    Specialized Agent for Data Analysis and Anomaly Detection
    
    Capabilities:
    - Real-time data stream analysis
    - Pattern recognition and anomaly detection
    - Statistical analysis and trend identification
    - Data quality assessment and validation
    - Automated insight generation
    """
    
    def __init__(self):
        self.agent_id = f"data_analyst_{datetime.now().strftime('%Y%m%d_%H%M%S')}"
        self.capabilities = [
            "data_analysis",
            "anomaly_detection",
            "pattern_recognition",
            "statistical_analysis",
            "data_validation",
            "insight_generation"
        ]
        
        self.analysis_history = []
        self.anomaly_patterns = {}
        self.baseline_metrics = {}
        
        # Analysis configuration
        self.config = CFG.get("data_analyst", {
            "anomaly_threshold": 2.5,  # Standard deviations
            "pattern_window": 50,      # Data points for pattern analysis
            "confidence_threshold": 0.7,
            "max_history": 1000
        })
        
        logger.info(f"[DATA_ANALYST] Initialized agent: {self.agent_id}")
    
    async def analyze_data_stream(self, data: List[Dict[str, Any]], stream_name: str) -> Dict[str, Any]:
        """Analyze a stream of data for patterns and anomalies"""
        start_time = datetime.now()
        
        try:
            results = {
                "stream_name": stream_name,
                "timestamp": start_time.isoformat(),
                "data_points": len(data),
                "analysis_results": {},
                "anomalies": [],
                "insights": [],
                "quality_score": 0.0
            }
            
            if not data:
                results["analysis_results"]["error"] = "No data provided"
                return results
            
            # Extract numeric features for statistical analysis
            numeric_features = self._extract_numeric_features(data)
            
            # Statistical analysis
            stats = self._perform_statistical_analysis(numeric_features)
            results["analysis_results"]["statistics"] = stats
            
            # Anomaly detection
            anomalies = await self._detect_anomalies(data, stream_name)
            results["anomalies"] = [self._anomaly_to_dict(a) for a in anomalies]
            
            # Pattern recognition
            patterns = self._recognize_patterns(numeric_features)
            results["analysis_results"]["patterns"] = patterns
            
            # Data quality assessment
            quality_score = self._assess_data_quality(data)
            results["quality_score"] = quality_score
            
            # Generate insights
            insights = self._generate_insights(stats, anomalies, patterns, quality_score)
            results["insights"] = insights
            
            # Update baseline metrics
            self._update_baseline_metrics(stream_name, stats)
            
            # Store analysis in history
            self.analysis_history.append(results)
            if len(self.analysis_history) > self.config["max_history"]:
                self.analysis_history.pop(0)
            
            execution_time = (datetime.now() - start_time).total_seconds()
            
            # Log the analysis
            log_event("data_analyst", "analysis_complete", {
                "stream_name": stream_name,
                "data_points": len(data),
                "anomalies_found": len(anomalies),
                "quality_score": quality_score,
                "execution_time": execution_time
            })
            
            # Embed analysis results for future learning
            analysis_text = f"Data analysis of {stream_name}: {len(data)} points, {len(anomalies)} anomalies, quality {quality_score:.2f}"
            vector = embedder.embed_text(analysis_text)
            embedder.package_embedding(
                text=analysis_text,
                vector=vector,
                meta={
                    "agent": "data_analyst",
                    "stream_name": stream_name,
                    "analysis_type": "data_stream",
                    "timestamp": start_time.isoformat(),
                    "watermark": "source:GremlinGPT_DataAnalyst"
                }
            )
            
            logger.info(f"[DATA_ANALYST] Analyzed {stream_name}: {len(data)} points, {len(anomalies)} anomalies, quality {quality_score:.2f}")
            
            return results
            
        except Exception as e:
            logger.error(f"[DATA_ANALYST] Analysis failed for {stream_name}: {e}")
            return {
                "stream_name": stream_name,
                "timestamp": start_time.isoformat(),
                "error": str(e),
                "analysis_results": {},
                "anomalies": [],
                "insights": [],
                "quality_score": 0.0
            }
    
    def _extract_numeric_features(self, data: List[Dict[str, Any]]) -> Dict[str, List[float]]:
        """Extract numeric features from data for analysis"""
        features = {}
        
        for item in data:
            for key, value in item.items():
                if isinstance(value, (int, float)) and not isinstance(value, bool):
                    if key not in features:
                        features[key] = []
                    features[key].append(float(value))
        
        return features
    
    def _perform_statistical_analysis(self, numeric_features: Dict[str, List[float]]) -> Dict[str, Any]:
        """Perform statistical analysis on numeric features"""
        stats = {}
        
        for feature_name, values in numeric_features.items():
            if not values:
                continue
                
            feature_stats = {
                "count": len(values),
                "mean": statistics.mean(values),
                "median": statistics.median(values),
                "std_dev": statistics.stdev(values) if len(values) > 1 else 0.0,
                "min": min(values),
                "max": max(values),
                "range": max(values) - min(values)
            }
            
            # Calculate percentiles
            if len(values) >= 4:
                sorted_values = sorted(values)
                feature_stats["q1"] = np.percentile(sorted_values, 25)
                feature_stats["q3"] = np.percentile(sorted_values, 75)
                feature_stats["iqr"] = feature_stats["q3"] - feature_stats["q1"]
            
            # Detect trends
            if len(values) >= 3:
                feature_stats["trend"] = self._calculate_trend(values)
            
            stats[feature_name] = feature_stats
        
        return stats
    
    def _calculate_trend(self, values: List[float]) -> str:
        """Calculate trend direction in data"""
        if len(values) < 3:
            return "insufficient_data"
        
        # Simple linear regression slope
        n = len(values)
        x = list(range(n))
        
        x_mean = sum(x) / n
        y_mean = sum(values) / n
        
        numerator = sum((x[i] - x_mean) * (values[i] - y_mean) for i in range(n))
        denominator = sum((x[i] - x_mean) ** 2 for i in range(n))
        
        if denominator == 0:
            return "flat"
        
        slope = numerator / denominator
        
        if slope > 0.1:
            return "increasing"
        elif slope < -0.1:
            return "decreasing"
        else:
            return "stable"
    
    async def _detect_anomalies(self, data: List[Dict[str, Any]], stream_name: str) -> List[AnomalyReport]:
        """Detect anomalies in the data using multiple methods"""
        anomalies = []
        
        # Statistical anomaly detection (Z-score method)
        numeric_features = self._extract_numeric_features(data)
        
        for feature_name, values in numeric_features.items():
            if len(values) < 3:
                continue
                
            mean_val = statistics.mean(values)
            std_val = statistics.stdev(values)
            
            if std_val == 0:
                continue
            
            for i, value in enumerate(values):
                z_score = abs((value - mean_val) / std_val)
                
                if z_score > self.config["anomaly_threshold"]:
                    anomaly = AnomalyReport(
                        anomaly_type="statistical_outlier",
                        severity=min(1.0, z_score / 5.0),  # Normalize to 0-1
                        description=f"Statistical outlier in {feature_name}: value {value} (z-score: {z_score:.2f})",
                        data_points=[{"index": i, "value": value, "z_score": z_score}],
                        confidence=min(1.0, z_score / 3.0),
                        timestamp=datetime.now(timezone.utc),
                        recommended_actions=["investigate_data_source", "validate_measurement", "check_for_errors"]
                    )
                    anomalies.append(anomaly)
        
        # Pattern-based anomaly detection
        pattern_anomalies = self._detect_pattern_anomalies(data, stream_name)
        anomalies.extend(pattern_anomalies)
        
        # Data quality anomalies
        quality_anomalies = self._detect_quality_anomalies(data)
        anomalies.extend(quality_anomalies)
        
        return anomalies
    
    def _detect_pattern_anomalies(self, data: List[Dict[str, Any]], stream_name: str) -> List[AnomalyReport]:
        """Detect anomalies based on pattern analysis"""
        anomalies = []
        
        # Check for sudden changes in data frequency
        if len(data) > 1:
            timestamps = []
            for item in data:
                if 'timestamp' in item:
                    try:
                        timestamps.append(datetime.fromisoformat(item['timestamp'].replace('Z', '+00:00')))
                    except:
                        continue
            
            if len(timestamps) > 2:
                intervals = [(timestamps[i+1] - timestamps[i]).total_seconds() for i in range(len(timestamps)-1)]
                
                if intervals:
                    mean_interval = statistics.mean(intervals)
                    std_interval = statistics.stdev(intervals) if len(intervals) > 1 else 0
                    
                    for i, interval in enumerate(intervals):
                        if std_interval > 0 and abs(interval - mean_interval) > 2 * std_interval:
                            anomaly = AnomalyReport(
                                anomaly_type="timing_anomaly",
                                severity=0.6,
                                description=f"Unusual timing interval: {interval:.2f}s (expected ~{mean_interval:.2f}s)",
                                data_points=[{"interval_index": i, "interval": interval, "expected": mean_interval}],
                                confidence=0.7,
                                timestamp=datetime.now(timezone.utc),
                                recommended_actions=["check_data_source_timing", "investigate_system_delays"]
                            )
                            anomalies.append(anomaly)
        
        return anomalies
    
    def _detect_quality_anomalies(self, data: List[Dict[str, Any]]) -> List[AnomalyReport]:
        """Detect data quality anomalies"""
        anomalies = []
        
        if not data:
            return anomalies
        
        # Check for missing data patterns
        total_items = len(data)
        items_with_missing = 0
        missing_fields = {}
        
        for item in data:
            has_missing = False
            for key, value in item.items():
                if value is None or value == "" or (isinstance(value, str) and value.lower() in ["null", "nan", "none"]):
                    missing_fields[key] = missing_fields.get(key, 0) + 1
                    has_missing = True
            
            if has_missing:
                items_with_missing += 1
        
        missing_rate = items_with_missing / total_items
        
        if missing_rate > 0.2:  # More than 20% missing data
            anomaly = AnomalyReport(
                anomaly_type="data_quality_missing",
                severity=missing_rate,
                description=f"High missing data rate: {missing_rate:.1%} of items have missing fields",
                data_points=[{"missing_rate": missing_rate, "missing_fields": missing_fields}],
                confidence=0.9,
                timestamp=datetime.now(timezone.utc),
                recommended_actions=["check_data_collection", "validate_data_pipeline", "implement_data_validation"]
            )
            anomalies.append(anomaly)
        
        return anomalies
    
    def _recognize_patterns(self, numeric_features: Dict[str, List[float]]) -> Dict[str, Any]:
        """Recognize patterns in numeric data"""
        patterns = {}
        
        for feature_name, values in numeric_features.items():
            if len(values) < self.config["pattern_window"]:
                continue
            
            feature_patterns = {}
            
            # Cyclical pattern detection
            if len(values) >= 10:
                feature_patterns["cyclical"] = self._detect_cyclical_pattern(values)
            
            # Seasonality detection (if timestamps available)
            feature_patterns["seasonality"] = self._detect_seasonality(values)
            
            # Volatility analysis
            if len(values) > 1:
                feature_patterns["volatility"] = {
                    "coefficient_of_variation": statistics.stdev(values) / statistics.mean(values) if statistics.mean(values) != 0 else 0,
                    "stability": "high" if statistics.stdev(values) / statistics.mean(values) < 0.1 else "low"
                }
            
            patterns[feature_name] = feature_patterns
        
        return patterns
    
    def _detect_cyclical_pattern(self, values: List[float]) -> Dict[str, Any]:
        """Detect cyclical patterns in data"""
        # Simple autocorrelation for cycle detection
        n = len(values)
        
        # Calculate autocorrelation for different lags
        max_lag = min(n // 4, 20)  # Check up to 1/4 of data length or 20 points
        autocorrelations = {}
        
        for lag in range(1, max_lag + 1):
            if lag >= n:
                break
            
            # Calculate correlation between values and values shifted by lag
            x = values[:-lag]
            y = values[lag:]
            
            if len(x) > 1 and len(y) > 1:
                try:
                    corr = np.corrcoef(x, y)[0, 1]
                    if not np.isnan(corr):
                        autocorrelations[lag] = abs(corr)
                except:
                    continue
        
        if autocorrelations:
            best_lag = max(autocorrelations.keys(), key=lambda k: autocorrelations[k])
            best_correlation = autocorrelations[best_lag]
            
            return {
                "detected": best_correlation > 0.5,
                "cycle_length": best_lag,
                "strength": best_correlation,
                "confidence": best_correlation
            }
        
        return {"detected": False, "cycle_length": None, "strength": 0, "confidence": 0}
    
    def _detect_seasonality(self, values: List[float]) -> Dict[str, Any]:
        """Detect seasonal patterns (placeholder for more advanced seasonality detection)"""
        # This is a simplified seasonality detection
        # In a real implementation, you might use FFT or more sophisticated methods
        
        if len(values) < 24:  # Need at least 24 points for daily seasonality
            return {"detected": False, "type": None, "confidence": 0}
        
        # Check for weekly pattern (7-day cycle)
        if len(values) >= 14:
            weekly_correlation = self._check_periodic_correlation(values, 7)
            if weekly_correlation > 0.6:
                return {"detected": True, "type": "weekly", "confidence": weekly_correlation}
        
        # Check for daily pattern (24-hour cycle if hourly data)
        if len(values) >= 48:
            daily_correlation = self._check_periodic_correlation(values, 24)
            if daily_correlation > 0.6:
                return {"detected": True, "type": "daily", "confidence": daily_correlation}
        
        return {"detected": False, "type": None, "confidence": 0}
    
    def _check_periodic_correlation(self, values: List[float], period: int) -> float:
        """Check correlation for a specific period"""
        if len(values) < 2 * period:
            return 0.0
        
        # Split into periods and calculate correlation
        periods = []
        for i in range(0, len(values) - period + 1, period):
            if i + period <= len(values):
                periods.append(values[i:i+period])
        
        if len(periods) < 2:
            return 0.0
        
        # Calculate average correlation between periods
        correlations = []
        for i in range(len(periods)):
            for j in range(i + 1, len(periods)):
                if len(periods[i]) == len(periods[j]):
                    try:
                        corr = np.corrcoef(periods[i], periods[j])[0, 1]
                        if not np.isnan(corr):
                            correlations.append(abs(corr))
                    except:
                        continue
        
        return statistics.mean(correlations) if correlations else 0.0
    
    def _assess_data_quality(self, data: List[Dict[str, Any]]) -> float:
        """Assess overall data quality score (0.0 to 1.0)"""
        if not data:
            return 0.0
        
        quality_factors = {}
        
        # Completeness: check for missing values
        total_fields = 0
        missing_fields = 0
        
        for item in data:
            for key, value in item.items():
                total_fields += 1
                if value is None or value == "" or (isinstance(value, str) and value.lower() in ["null", "nan", "none"]):
                    missing_fields += 1
        
        completeness = 1.0 - (missing_fields / total_fields) if total_fields > 0 else 0.0
        quality_factors["completeness"] = completeness
        
        # Consistency: check data type consistency
        field_types = {}
        type_inconsistencies = 0
        
        for item in data:
            for key, value in item.items():
                value_type = type(value).__name__
                if key not in field_types:
                    field_types[key] = value_type
                elif field_types[key] != value_type and value is not None:
                    type_inconsistencies += 1
        
        consistency = 1.0 - (type_inconsistencies / total_fields) if total_fields > 0 else 1.0
        quality_factors["consistency"] = consistency
        
        # Validity: check for reasonable ranges (basic checks)
        validity_score = 1.0
        numeric_features = self._extract_numeric_features(data)
        
        for feature_name, values in numeric_features.items():
            if values:
                # Check for extreme outliers that might indicate invalid data
                q1, q3 = np.percentile(values, [25, 75])
                iqr = q3 - q1
                lower_bound = q1 - 3 * iqr
                upper_bound = q3 + 3 * iqr
                
                outliers = sum(1 for v in values if v < lower_bound or v > upper_bound)
                outlier_rate = outliers / len(values)
                
                if outlier_rate > 0.1:  # More than 10% outliers
                    validity_score *= (1.0 - outlier_rate * 0.5)
        
        quality_factors["validity"] = max(0.0, validity_score)
        
        # Calculate weighted overall score
        weights = {"completeness": 0.4, "consistency": 0.3, "validity": 0.3}
        overall_score = sum(quality_factors[factor] * weights[factor] for factor in weights)
        
        return round(overall_score, 3)
    
    def _generate_insights(self, stats: Dict[str, Any], anomalies: List[AnomalyReport], 
                          patterns: Dict[str, Any], quality_score: float) -> List[str]:
        """Generate actionable insights from analysis results"""
        insights = []
        
        # Quality insights
        if quality_score < 0.7:
            insights.append(f"Data quality is below acceptable threshold ({quality_score:.1%}). Consider implementing data validation.")
        
        # Statistical insights
        for feature_name, feature_stats in stats.items():
            if "trend" in feature_stats:
                trend = feature_stats["trend"]
                if trend == "increasing":
                    insights.append(f"{feature_name} shows an increasing trend - monitor for sustainability")
                elif trend == "decreasing":
                    insights.append(f"{feature_name} shows a decreasing trend - investigate potential causes")
            
            # High variability insight
            if "std_dev" in feature_stats and "mean" in feature_stats:
                cv = feature_stats["std_dev"] / feature_stats["mean"] if feature_stats["mean"] != 0 else 0
                if cv > 0.5:
                    insights.append(f"{feature_name} shows high variability (CV: {cv:.2f}) - consider stabilization measures")
        
        # Anomaly insights
        high_severity_anomalies = [a for a in anomalies if a.severity > 0.7]
        if high_severity_anomalies:
            insights.append(f"Detected {len(high_severity_anomalies)} high-severity anomalies requiring immediate attention")
        
        # Pattern insights
        for feature_name, feature_patterns in patterns.items():
            if "cyclical" in feature_patterns and feature_patterns["cyclical"]["detected"]:
                cycle_length = feature_patterns["cyclical"]["cycle_length"]
                insights.append(f"{feature_name} exhibits cyclical behavior with {cycle_length}-point cycles")
            
            if "seasonality" in feature_patterns and feature_patterns["seasonality"]["detected"]:
                season_type = feature_patterns["seasonality"]["type"]
                insights.append(f"{feature_name} shows {season_type} seasonality - leverage for forecasting")
        
        return insights
    
    def _update_baseline_metrics(self, stream_name: str, current_stats: Dict[str, Any]):
        """Update baseline metrics for future anomaly detection"""
        if stream_name not in self.baseline_metrics:
            self.baseline_metrics[stream_name] = {}
        
        # Update baseline with exponential smoothing
        alpha = 0.1  # Smoothing factor
        
        for feature_name, feature_stats in current_stats.items():
            if feature_name not in self.baseline_metrics[stream_name]:
                self.baseline_metrics[stream_name][feature_name] = feature_stats.copy()
            else:
                baseline = self.baseline_metrics[stream_name][feature_name]
                for metric, value in feature_stats.items():
                    if isinstance(value, (int, float)):
                        baseline[metric] = alpha * value + (1 - alpha) * baseline.get(metric, value)
    
    def _anomaly_to_dict(self, anomaly: AnomalyReport) -> Dict[str, Any]:
        """Convert AnomalyReport to dictionary"""
        return {
            "type": anomaly.anomaly_type,
            "severity": anomaly.severity,
            "description": anomaly.description,
            "data_points": anomaly.data_points,
            "confidence": anomaly.confidence,
            "timestamp": anomaly.timestamp.isoformat(),
            "recommended_actions": anomaly.recommended_actions
        }
    
    async def get_analysis_summary(self) -> Dict[str, Any]:
        """Get summary of recent analysis activities"""
        recent_analyses = self.analysis_history[-10:] if self.analysis_history else []
        
        total_anomalies = sum(len(analysis.get("anomalies", [])) for analysis in recent_analyses)
        avg_quality = statistics.mean([analysis.get("quality_score", 0) for analysis in recent_analyses]) if recent_analyses else 0
        
        return {
            "agent_id": self.agent_id,
            "capabilities": self.capabilities,
            "recent_analyses": len(recent_analyses),
            "total_anomalies_found": total_anomalies,
            "average_quality_score": round(avg_quality, 3),
            "baseline_streams": list(self.baseline_metrics.keys()),
            "status": "active"
        }
    
    async def handle_task(self, task: Dict[str, Any]) -> Dict[str, Any]:
        """Handle tasks assigned to this agent"""
        task_type = task.get("type")
        
        if task_type == "analyze_data":
            data = task.get("data", [])
            stream_name = task.get("stream_name", "unknown")
            return await self.analyze_data_stream(data, stream_name)
        
        elif task_type == "get_analysis_summary":
            return await self.get_analysis_summary()
        
        elif task_type == "detect_anomalies":
            data = task.get("data", [])
            stream_name = task.get("stream_name", "anomaly_check")
            results = await self.analyze_data_stream(data, stream_name)
            return {"anomalies": results.get("anomalies", [])}
        
        else:
            return {"error": f"Unknown task type: {task_type}"}


# Global instance
_data_analyst_agent = None


def get_data_analyst_agent() -> DataAnalystAgent:
    """Get the global data analyst agent instance"""
    global _data_analyst_agent
    if _data_analyst_agent is None:
        _data_analyst_agent = DataAnalystAgent()
    return _data_analyst_agent


async def analyze_data_stream(data: List[Dict[str, Any]], stream_name: str) -> Dict[str, Any]:
    """Convenience function for data stream analysis"""
    agent = get_data_analyst_agent()
    return await agent.analyze_data_stream(data, stream_name)


if __name__ == "__main__":
    async def test_agent():
        agent = DataAnalystAgent()
        
        # Test with sample data
        test_data = [
            {"timestamp": "2024-01-01T10:00:00Z", "value": 100, "status": "normal"},
            {"timestamp": "2024-01-01T10:01:00Z", "value": 105, "status": "normal"},
            {"timestamp": "2024-01-01T10:02:00Z", "value": 98, "status": "normal"},
            {"timestamp": "2024-01-01T10:03:00Z", "value": 500, "status": "anomaly"},  # Anomaly
            {"timestamp": "2024-01-01T10:04:00Z", "value": 102, "status": "normal"},
        ]
        
        results = await agent.analyze_data_stream(test_data, "test_stream")
        print(json.dumps(results, indent=2))
    
    asyncio.run(test_agent())

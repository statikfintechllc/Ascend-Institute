#!/usr/bin/env python3

# ─────────────────────────────────────────────────────────────
# ⚠️ GremlinGPT Fair Use Only | Commercial Use Requires License
# Built under the GremlinGPT Dual License v1.0
# © 2025 StatikFintechLLC / AscendAI Project
# Contact: ascend.gremlin@gmail.com
# ─────────────────────────────────────────────────────────────

# GremlinGPT v1.0.3 :: Specialized Agent - Trading Strategy & Risk Management

import asyncio
import numpy as np
import pandas as pd
from datetime import datetime, timezone, timedelta
from pathlib import Path
import sys
import json
from typing import Dict, List, Any, Optional, Tuple, Union
import statistics
from dataclasses import dataclass
from enum import Enum

# Add project root to path for imports
project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root))

from backend.globals import CFG
from utils.logging_config import setup_module_logger
from memory.log_history import log_event
from memory.vector_store import embedder
from agent_core.task_queue import enqueue_task

logger = setup_module_logger("agents", "trading_strategist")


class SignalType(Enum):
    BUY = "buy"
    SELL = "sell"
    HOLD = "hold"
    STRONG_BUY = "strong_buy"
    STRONG_SELL = "strong_sell"


class RiskLevel(Enum):
    LOW = "low"
    MEDIUM = "medium"
    HIGH = "high"
    CRITICAL = "critical"


@dataclass
class TradingSignal:
    """Trading signal with comprehensive metadata"""
    symbol: str
    signal_type: SignalType
    confidence: float  # 0.0 to 1.0
    price_target: Optional[float]
    stop_loss: Optional[float]
    risk_level: RiskLevel
    reasoning: str
    supporting_indicators: List[str]
    timestamp: datetime
    expiry: Optional[datetime]
    position_size_recommendation: float  # Percentage of portfolio


@dataclass
class RiskAssessment:
    """Risk assessment for trading decisions"""
    risk_score: float  # 0.0 to 1.0
    risk_level: RiskLevel
    risk_factors: List[str]
    mitigation_strategies: List[str]
    max_position_size: float
    stop_loss_recommendation: float
    volatility_score: float


class TradingStrategistAgent:
    """
    Specialized Agent for Trading Strategy and Risk Management
    
    Capabilities:
    - Advanced trading signal generation
    - Multi-timeframe technical analysis
    - Risk assessment and position sizing
    - Portfolio optimization
    - Strategy backtesting and validation
    - Real-time market monitoring
    """
    
    def __init__(self):
        self.agent_id = f"trading_strategist_{datetime.now().strftime('%Y%m%d_%H%M%S')}"
        self.capabilities = [
            "signal_generation",
            "risk_management",
            "technical_analysis",
            "portfolio_optimization",
            "strategy_backtesting",
            "market_monitoring",
            "position_sizing"
        ]
        
        self.active_signals = {}
        self.portfolio_state = {}
        self.risk_metrics = {}
        self.strategy_performance = {}
        
        # Trading configuration
        self.config = CFG.get("trading_strategist", {
            "max_portfolio_risk": 0.02,  # 2% max risk per trade
            "risk_free_rate": 0.02,      # 2% annual risk-free rate
            "volatility_lookback": 20,   # Days for volatility calculation
            "signal_confidence_threshold": 0.6,
            "max_position_size": 0.1,    # 10% max position size
            "stop_loss_multiplier": 2.0  # Stop loss = 2x ATR
        })
        
        logger.info(f"[TRADING_STRATEGIST] Initialized agent: {self.agent_id}")
    
    async def generate_trading_signals(self, market_data: Dict[str, Any], 
                                     symbols: Optional[List[str]] = None) -> List[TradingSignal]:
        """Generate comprehensive trading signals for given symbols"""
        start_time = datetime.now()
        signals = []
        
        try:
            if symbols is None:
                symbols = list(market_data.keys())
            
            for symbol in symbols:
                if symbol not in market_data:
                    logger.warning(f"[TRADING_STRATEGIST] No data available for {symbol}")
                    continue
                
                symbol_data = market_data[symbol]
                signal = await self._analyze_symbol(symbol, symbol_data)
                
                if signal and signal.confidence >= self.config["signal_confidence_threshold"]:
                    signals.append(signal)
                    self.active_signals[symbol] = signal
            
            # Log signal generation
            execution_time = (datetime.now() - start_time).total_seconds()
            log_event("trading_strategist", "signals_generated", {
                "symbols_analyzed": len(symbols),
                "signals_generated": len(signals),
                "execution_time": execution_time
            })
            
            # Embed signals for learning
            signals_text = f"Generated {len(signals)} trading signals for {len(symbols)} symbols"
            vector = embedder.embed_text(signals_text)
            embedder.package_embedding(
                text=signals_text,
                vector=vector,
                meta={
                    "agent": "trading_strategist",
                    "signal_count": len(signals),
                    "symbols": symbols,
                    "timestamp": start_time.isoformat(),
                    "watermark": "source:GremlinGPT_TradingStrategist"
                }
            )
            
            logger.info(f"[TRADING_STRATEGIST] Generated {len(signals)} signals for {len(symbols)} symbols")
            return signals
            
        except Exception as e:
            logger.error(f"[TRADING_STRATEGIST] Signal generation failed: {e}")
            return []
    
    async def _analyze_symbol(self, symbol: str, data: Dict[str, Any]) -> Optional[TradingSignal]:
        """Analyze a single symbol and generate trading signal"""
        try:
            # Extract price data
            prices = self._extract_price_data(data)
            if not prices or len(prices) < 20:
                return None
            
            # Technical analysis
            technical_indicators = self._calculate_technical_indicators(prices)
            
            # Generate signal based on technical analysis
            signal_type, confidence = self._determine_signal(technical_indicators)
            
            if confidence < self.config["signal_confidence_threshold"]:
                return None
            
            # Risk assessment
            risk_assessment = self._assess_risk(symbol, prices, technical_indicators)
            
            # Calculate price targets and stop loss
            current_price = prices[-1]
            price_target = self._calculate_price_target(current_price, signal_type, technical_indicators)
            stop_loss = self._calculate_stop_loss(current_price, signal_type, technical_indicators)
            
            # Position sizing
            position_size = self._calculate_position_size(risk_assessment, current_price, stop_loss)
            
            # Create signal
            signal = TradingSignal(
                symbol=symbol,
                signal_type=signal_type,
                confidence=confidence,
                price_target=price_target,
                stop_loss=stop_loss,
                risk_level=risk_assessment.risk_level,
                reasoning=self._generate_reasoning(technical_indicators, signal_type),
                supporting_indicators=self._get_supporting_indicators(technical_indicators, signal_type),
                timestamp=datetime.now(timezone.utc),
                expiry=datetime.now(timezone.utc) + timedelta(hours=24),  # 24-hour expiry
                position_size_recommendation=position_size
            )
            
            return signal
            
        except Exception as e:
            logger.error(f"[TRADING_STRATEGIST] Analysis failed for {symbol}: {e}")
            return None
    
    def _extract_price_data(self, data: Dict[str, Any]) -> List[float]:
        """Extract price data from market data"""
        prices = []
        
        # Try different price field names
        price_fields = ['close', 'price', 'last', 'value']
        
        if isinstance(data, dict):
            # If data is a single price point
            for field in price_fields:
                if field in data and isinstance(data[field], (int, float)):
                    return [float(data[field])]
            
            # If data contains historical prices
            if 'prices' in data and isinstance(data['prices'], list):
                for price_point in data['prices']:
                    if isinstance(price_point, (int, float)):
                        prices.append(float(price_point))
                    elif isinstance(price_point, dict):
                        for field in price_fields:
                            if field in price_point:
                                prices.append(float(price_point[field]))
                                break
        
        elif isinstance(data, list):
            # If data is a list of prices or price objects
            for item in data:
                if isinstance(item, (int, float)):
                    prices.append(float(item))
                elif isinstance(item, dict):
                    for field in price_fields:
                        if field in item:
                            prices.append(float(item[field]))
                            break
        
        return prices
    
    def _calculate_technical_indicators(self, prices: List[float]) -> Dict[str, Any]:
        """Calculate technical indicators from price data"""
        if len(prices) < 20:
            return {}
        
        indicators = {}
        
        # Simple Moving Averages
        if len(prices) >= 20:
            indicators['sma_20'] = sum(prices[-20:]) / 20
            indicators['sma_50'] = sum(prices[-50:]) / 50 if len(prices) >= 50 else sum(prices) / len(prices)
        
        # Exponential Moving Average
        indicators['ema_12'] = self._calculate_ema(prices, 12)
        indicators['ema_26'] = self._calculate_ema(prices, 26)
        
        # MACD
        if 'ema_12' in indicators and 'ema_26' in indicators:
            indicators['macd'] = indicators['ema_12'] - indicators['ema_26']
            # Signal line (9-period EMA of MACD)
            macd_history = [indicators['macd']]  # Simplified - in real implementation, calculate for more periods
            indicators['macd_signal'] = indicators['macd']  # Simplified
            indicators['macd_histogram'] = indicators['macd'] - indicators['macd_signal']
        
        # RSI
        indicators['rsi'] = self._calculate_rsi(prices, 14)
        
        # Bollinger Bands
        if len(prices) >= 20:
            sma_20 = indicators['sma_20']
            std_dev = statistics.stdev(prices[-20:])
            indicators['bb_upper'] = sma_20 + (2 * std_dev)
            indicators['bb_lower'] = sma_20 - (2 * std_dev)
            indicators['bb_middle'] = sma_20
            
            # BB position
            current_price = prices[-1]
            indicators['bb_position'] = (current_price - indicators['bb_lower']) / (indicators['bb_upper'] - indicators['bb_lower'])
        
        # Average True Range (ATR)
        indicators['atr'] = self._calculate_atr(prices, 14)
        
        # Price momentum
        if len(prices) >= 10:
            indicators['momentum_10'] = (prices[-1] / prices[-10] - 1) * 100
        
        # Volatility
        if len(prices) >= 20:
            returns = [(prices[i] / prices[i-1] - 1) for i in range(1, len(prices))]
            indicators['volatility'] = statistics.stdev(returns[-20:]) * (252 ** 0.5)  # Annualized volatility
        
        return indicators
    
    def _calculate_ema(self, prices: List[float], period: int) -> float:
        """Calculate Exponential Moving Average"""
        if len(prices) < period:
            return sum(prices) / len(prices)
        
        multiplier = 2 / (period + 1)
        ema = sum(prices[:period]) / period  # Start with SMA
        
        for price in prices[period:]:
            ema = (price * multiplier) + (ema * (1 - multiplier))
        
        return ema
    
    def _calculate_rsi(self, prices: List[float], period: int = 14) -> float:
        """Calculate Relative Strength Index"""
        if len(prices) < period + 1:
            return 50.0  # Neutral RSI
        
        gains = []
        losses = []
        
        for i in range(1, len(prices)):
            change = prices[i] - prices[i-1]
            if change > 0:
                gains.append(change)
                losses.append(0)
            else:
                gains.append(0)
                losses.append(abs(change))
        
        if len(gains) < period:
            return 50.0
        
        avg_gain = sum(gains[-period:]) / period
        avg_loss = sum(losses[-period:]) / period
        
        if avg_loss == 0:
            return 100.0
        
        rs = avg_gain / avg_loss
        rsi = 100 - (100 / (1 + rs))
        
        return rsi
    
    def _calculate_atr(self, prices: List[float], period: int = 14) -> float:
        """Calculate Average True Range"""
        if len(prices) < period + 1:
            return 0.0
        
        true_ranges = []
        
        for i in range(1, len(prices)):
            high = prices[i]
            low = prices[i]
            prev_close = prices[i-1]
            
            tr = max(
                high - low,
                abs(high - prev_close),
                abs(low - prev_close)
            )
            true_ranges.append(tr)
        
        if len(true_ranges) < period:
            return sum(true_ranges) / len(true_ranges)
        
        return sum(true_ranges[-period:]) / period
    
    def _determine_signal(self, indicators: Dict[str, Any]) -> Tuple[SignalType, float]:
        """Determine trading signal based on technical indicators"""
        signals = []
        confidences = []
        
        current_price = indicators.get('current_price', 0)
        
        # RSI signals
        rsi = indicators.get('rsi', 50)
        if rsi < 30:
            signals.append(SignalType.BUY)
            confidences.append(0.7)
        elif rsi > 70:
            signals.append(SignalType.SELL)
            confidences.append(0.7)
        elif rsi < 40:
            signals.append(SignalType.BUY)
            confidences.append(0.5)
        elif rsi > 60:
            signals.append(SignalType.SELL)
            confidences.append(0.5)
        
        # Moving Average signals
        if 'sma_20' in indicators and 'sma_50' in indicators:
            if indicators['sma_20'] > indicators['sma_50']:
                signals.append(SignalType.BUY)
                confidences.append(0.6)
            else:
                signals.append(SignalType.SELL)
                confidences.append(0.6)
        
        # MACD signals
        if 'macd' in indicators and 'macd_signal' in indicators:
            if indicators['macd'] > indicators['macd_signal']:
                signals.append(SignalType.BUY)
                confidences.append(0.6)
            else:
                signals.append(SignalType.SELL)
                confidences.append(0.6)
        
        # Bollinger Bands signals
        if 'bb_position' in indicators:
            bb_pos = indicators['bb_position']
            if bb_pos < 0.2:  # Near lower band
                signals.append(SignalType.BUY)
                confidences.append(0.5)
            elif bb_pos > 0.8:  # Near upper band
                signals.append(SignalType.SELL)
                confidences.append(0.5)
        
        # Momentum signals
        if 'momentum_10' in indicators:
            momentum = indicators['momentum_10']
            if momentum > 5:
                signals.append(SignalType.BUY)
                confidences.append(0.4)
            elif momentum < -5:
                signals.append(SignalType.SELL)
                confidences.append(0.4)
        
        # Aggregate signals
        if not signals:
            return SignalType.HOLD, 0.5
        
        # Count signal types
        buy_signals = signals.count(SignalType.BUY)
        sell_signals = signals.count(SignalType.SELL)
        
        # Calculate weighted confidence
        buy_confidence = sum(conf for i, conf in enumerate(confidences) if signals[i] == SignalType.BUY)
        sell_confidence = sum(conf for i, conf in enumerate(confidences) if signals[i] == SignalType.SELL)
        
        if buy_signals > sell_signals:
            final_signal = SignalType.STRONG_BUY if buy_confidence > 2.0 else SignalType.BUY
            final_confidence = min(1.0, buy_confidence / len(signals))
        elif sell_signals > buy_signals:
            final_signal = SignalType.STRONG_SELL if sell_confidence > 2.0 else SignalType.SELL
            final_confidence = min(1.0, sell_confidence / len(signals))
        else:
            final_signal = SignalType.HOLD
            final_confidence = 0.5
        
        return final_signal, final_confidence
    
    def _assess_risk(self, symbol: str, prices: List[float], indicators: Dict[str, Any]) -> RiskAssessment:
        """Assess risk for the trading decision"""
        risk_factors = []
        risk_score = 0.0
        
        # Volatility risk
        volatility = indicators.get('volatility', 0.2)
        if volatility > 0.5:
            risk_factors.append("High volatility")
            risk_score += 0.3
        elif volatility > 0.3:
            risk_factors.append("Moderate volatility")
            risk_score += 0.2
        
        # RSI extreme levels
        rsi = indicators.get('rsi', 50)
        if rsi > 80 or rsi < 20:
            risk_factors.append("RSI at extreme levels")
            risk_score += 0.2
        
        # Price momentum risk
        momentum = indicators.get('momentum_10', 0)
        if abs(momentum) > 15:
            risk_factors.append("High momentum - potential reversal risk")
            risk_score += 0.2
        
        # ATR relative to price
        atr = indicators.get('atr', 0)
        if atr > 0 and len(prices) > 0:
            atr_percentage = atr / prices[-1]
            if atr_percentage > 0.05:  # 5%
                risk_factors.append("High intraday volatility")
                risk_score += 0.2
        
        # Determine risk level
        if risk_score >= 0.7:
            risk_level = RiskLevel.CRITICAL
        elif risk_score >= 0.5:
            risk_level = RiskLevel.HIGH
        elif risk_score >= 0.3:
            risk_level = RiskLevel.MEDIUM
        else:
            risk_level = RiskLevel.LOW
        
        # Calculate position sizing based on risk
        max_position_size = self.config["max_position_size"]
        if risk_level == RiskLevel.CRITICAL:
            max_position_size *= 0.25
        elif risk_level == RiskLevel.HIGH:
            max_position_size *= 0.5
        elif risk_level == RiskLevel.MEDIUM:
            max_position_size *= 0.75
        
        # Stop loss recommendation
        atr_multiplier = self.config["stop_loss_multiplier"]
        stop_loss_distance = atr * atr_multiplier if atr > 0 else prices[-1] * 0.02
        
        mitigation_strategies = self._generate_mitigation_strategies(risk_factors, risk_level)
        
        return RiskAssessment(
            risk_score=risk_score,
            risk_level=risk_level,
            risk_factors=risk_factors,
            mitigation_strategies=mitigation_strategies,
            max_position_size=max_position_size,
            stop_loss_recommendation=stop_loss_distance,
            volatility_score=volatility
        )
    
    def _generate_mitigation_strategies(self, risk_factors: List[str], risk_level: RiskLevel) -> List[str]:
        """Generate risk mitigation strategies"""
        strategies = []
        
        if "High volatility" in risk_factors:
            strategies.append("Reduce position size")
            strategies.append("Use tighter stop losses")
            strategies.append("Consider options strategies for hedging")
        
        if "RSI at extreme levels" in risk_factors:
            strategies.append("Wait for RSI normalization")
            strategies.append("Consider contrarian positioning")
        
        if "High momentum" in risk_factors:
            strategies.append("Monitor for reversal signals")
            strategies.append("Take partial profits")
        
        if risk_level in [RiskLevel.HIGH, RiskLevel.CRITICAL]:
            strategies.append("Use smaller position sizes")
            strategies.append("Diversify across multiple positions")
            strategies.append("Set strict stop losses")
        
        return strategies
    
    def _calculate_price_target(self, current_price: float, signal_type: SignalType, 
                               indicators: Dict[str, Any]) -> Optional[float]:
        """Calculate price target based on signal and indicators"""
        if signal_type in [SignalType.HOLD]:
            return None
        
        atr = indicators.get('atr', current_price * 0.02)
        
        if signal_type in [SignalType.BUY, SignalType.STRONG_BUY]:
            # Use resistance levels or ATR-based targets
            if 'bb_upper' in indicators:
                return indicators['bb_upper']
            else:
                return current_price + (atr * 2)
        
        elif signal_type in [SignalType.SELL, SignalType.STRONG_SELL]:
            # Use support levels or ATR-based targets
            if 'bb_lower' in indicators:
                return indicators['bb_lower']
            else:
                return current_price - (atr * 2)
        
        return None
    
    def _calculate_stop_loss(self, current_price: float, signal_type: SignalType, 
                            indicators: Dict[str, Any]) -> Optional[float]:
        """Calculate stop loss based on signal and indicators"""
        if signal_type == SignalType.HOLD:
            return None
        
        atr = indicators.get('atr', current_price * 0.02)
        stop_multiplier = self.config["stop_loss_multiplier"]
        
        if signal_type in [SignalType.BUY, SignalType.STRONG_BUY]:
            return current_price - (atr * stop_multiplier)
        
        elif signal_type in [SignalType.SELL, SignalType.STRONG_SELL]:
            return current_price + (atr * stop_multiplier)
        
        return None
    
    def _calculate_position_size(self, risk_assessment: RiskAssessment, 
                               current_price: float, stop_loss: Optional[float]) -> float:
        """Calculate optimal position size based on risk management"""
        max_risk_per_trade = self.config["max_portfolio_risk"]
        max_position_size = risk_assessment.max_position_size
        
        if stop_loss is None:
            return max_position_size * 0.5  # Conservative sizing without stop loss
        
        # Calculate risk per share
        risk_per_share = abs(current_price - stop_loss)
        
        if risk_per_share == 0:
            return max_position_size * 0.5
        
        # Position size based on fixed risk amount
        portfolio_value = 100000  # Assume $100k portfolio (should be dynamic)
        max_risk_amount = portfolio_value * max_risk_per_trade
        
        position_value = max_risk_amount / (risk_per_share / current_price)
        position_size = min(position_value / portfolio_value, max_position_size)
        
        return round(position_size, 4)
    
    def _generate_reasoning(self, indicators: Dict[str, Any], signal_type: SignalType) -> str:
        """Generate human-readable reasoning for the signal"""
        reasons = []
        
        rsi = indicators.get('rsi', 50)
        if rsi < 30:
            reasons.append(f"RSI oversold at {rsi:.1f}")
        elif rsi > 70:
            reasons.append(f"RSI overbought at {rsi:.1f}")
        
        if 'sma_20' in indicators and 'sma_50' in indicators:
            if indicators['sma_20'] > indicators['sma_50']:
                reasons.append("20-day SMA above 50-day SMA (bullish)")
            else:
                reasons.append("20-day SMA below 50-day SMA (bearish)")
        
        if 'macd' in indicators and 'macd_signal' in indicators:
            if indicators['macd'] > indicators['macd_signal']:
                reasons.append("MACD above signal line")
            else:
                reasons.append("MACD below signal line")
        
        if 'bb_position' in indicators:
            bb_pos = indicators['bb_position']
            if bb_pos < 0.2:
                reasons.append("Price near Bollinger Band lower bound")
            elif bb_pos > 0.8:
                reasons.append("Price near Bollinger Band upper bound")
        
        if not reasons:
            reasons.append("Mixed technical signals")
        
        return "; ".join(reasons)
    
    def _get_supporting_indicators(self, indicators: Dict[str, Any], signal_type: SignalType) -> List[str]:
        """Get list of supporting technical indicators"""
        supporting = []
        
        if signal_type in [SignalType.BUY, SignalType.STRONG_BUY]:
            if indicators.get('rsi', 50) < 40:
                supporting.append("RSI")
            if indicators.get('macd', 0) > indicators.get('macd_signal', 0):
                supporting.append("MACD")
            if indicators.get('bb_position', 0.5) < 0.3:
                supporting.append("Bollinger Bands")
            if indicators.get('momentum_10', 0) > 0:
                supporting.append("Price Momentum")
        
        elif signal_type in [SignalType.SELL, SignalType.STRONG_SELL]:
            if indicators.get('rsi', 50) > 60:
                supporting.append("RSI")
            if indicators.get('macd', 0) < indicators.get('macd_signal', 0):
                supporting.append("MACD")
            if indicators.get('bb_position', 0.5) > 0.7:
                supporting.append("Bollinger Bands")
            if indicators.get('momentum_10', 0) < 0:
                supporting.append("Price Momentum")
        
        return supporting
    
    async def optimize_portfolio(self, current_positions: Dict[str, Any], 
                               available_signals: List[TradingSignal]) -> Dict[str, Any]:
        """Optimize portfolio allocation based on current positions and new signals"""
        optimization_result = {
            "timestamp": datetime.now(timezone.utc).isoformat(),
            "current_portfolio_value": 0,
            "recommended_changes": [],
            "risk_metrics": {},
            "optimization_score": 0.0
        }
        
        try:
            # Calculate current portfolio metrics
            total_value = sum(pos.get('value', 0) for pos in current_positions.values())
            optimization_result["current_portfolio_value"] = total_value
            
            # Analyze portfolio risk
            portfolio_risk = self._calculate_portfolio_risk(current_positions)
            optimization_result["risk_metrics"] = portfolio_risk
            
            # Generate rebalancing recommendations
            recommendations = self._generate_rebalancing_recommendations(
                current_positions, available_signals, portfolio_risk
            )
            optimization_result["recommended_changes"] = recommendations
            
            # Calculate optimization score
            optimization_result["optimization_score"] = self._calculate_optimization_score(
                current_positions, recommendations
            )
            
            logger.info(f"[TRADING_STRATEGIST] Portfolio optimization complete. Score: {optimization_result['optimization_score']:.2f}")
            
        except Exception as e:
            logger.error(f"[TRADING_STRATEGIST] Portfolio optimization failed: {e}")
            optimization_result["error"] = str(e)
        
        return optimization_result
    
    def _calculate_portfolio_risk(self, positions: Dict[str, Any]) -> Dict[str, Any]:
        """Calculate portfolio-level risk metrics"""
        if not positions:
            return {"total_risk": 0.0, "diversification_score": 0.0, "concentration_risk": 0.0}
        
        total_value = sum(pos.get('value', 0) for pos in positions.values())
        
        # Calculate concentration risk
        position_weights = [pos.get('value', 0) / total_value for pos in positions.values() if total_value > 0]
        concentration_risk = max(position_weights) if position_weights else 0.0
        
        # Diversification score (inverse of concentration)
        diversification_score = 1.0 - concentration_risk if position_weights else 0.0
        
        # Estimate portfolio volatility (simplified)
        avg_volatility = 0.25  # Assume average 25% volatility
        portfolio_volatility = avg_volatility / (len(positions) ** 0.5)  # Diversification benefit
        
        return {
            "total_risk": portfolio_volatility,
            "diversification_score": diversification_score,
            "concentration_risk": concentration_risk,
            "position_count": len(positions)
        }
    
    def _generate_rebalancing_recommendations(self, current_positions: Dict[str, Any], 
                                            signals: List[TradingSignal], 
                                            portfolio_risk: Dict[str, Any]) -> List[Dict[str, Any]]:
        """Generate portfolio rebalancing recommendations"""
        recommendations = []
        
        # Get high-confidence signals
        strong_signals = [s for s in signals if s.confidence > 0.8]
        
        for signal in strong_signals:
            if signal.signal_type in [SignalType.BUY, SignalType.STRONG_BUY]:
                recommendation = {
                    "action": "buy",
                    "symbol": signal.symbol,
                    "recommended_size": signal.position_size_recommendation,
                    "reasoning": signal.reasoning,
                    "confidence": signal.confidence,
                    "risk_level": signal.risk_level.value
                }
                recommendations.append(recommendation)
            
            elif signal.signal_type in [SignalType.SELL, SignalType.STRONG_SELL]:
                if signal.symbol in current_positions:
                    recommendation = {
                        "action": "sell",
                        "symbol": signal.symbol,
                        "recommended_size": 1.0,  # Sell entire position
                        "reasoning": signal.reasoning,
                        "confidence": signal.confidence,
                        "risk_level": signal.risk_level.value
                    }
                    recommendations.append(recommendation)
        
        # Risk-based recommendations
        if portfolio_risk["concentration_risk"] > 0.3:
            # Recommend reducing largest positions
            if current_positions:
                largest_position = max(current_positions.items(), key=lambda x: x[1].get('value', 0))
                recommendations.append({
                    "action": "reduce",
                    "symbol": largest_position[0],
                    "recommended_size": 0.5,  # Reduce by 50%
                    "reasoning": "Reduce concentration risk",
                    "confidence": 0.8,
                    "risk_level": "medium"
                })
        
        return recommendations
    
    def _calculate_optimization_score(self, positions: Dict[str, Any], 
                                    recommendations: List[Dict[str, Any]]) -> float:
        """Calculate portfolio optimization score"""
        if not recommendations:
            return 0.5  # Neutral score
        
        # Score based on signal confidence and portfolio improvement potential
        total_confidence = sum(rec.get('confidence', 0) for rec in recommendations)
        avg_confidence = total_confidence / len(recommendations)
        
        # Bonus for diversification improvements
        diversification_bonus = 0.1 if len(recommendations) > 2 else 0.0
        
        return min(1.0, avg_confidence + diversification_bonus)
    
    def signal_to_dict(self, signal: TradingSignal) -> Dict[str, Any]:
        """Convert TradingSignal to dictionary"""
        return {
            "symbol": signal.symbol,
            "signal_type": signal.signal_type.value,
            "confidence": signal.confidence,
            "price_target": signal.price_target,
            "stop_loss": signal.stop_loss,
            "risk_level": signal.risk_level.value,
            "reasoning": signal.reasoning,
            "supporting_indicators": signal.supporting_indicators,
            "timestamp": signal.timestamp.isoformat(),
            "expiry": signal.expiry.isoformat() if signal.expiry else None,
            "position_size_recommendation": signal.position_size_recommendation
        }
    
    async def handle_task(self, task: Dict[str, Any]) -> Dict[str, Any]:
        """Handle tasks assigned to this agent"""
        task_type = task.get("type")
        
        if task_type == "generate_signals":
            market_data = task.get("market_data", {})
            symbols = task.get("symbols")
            signals = await self.generate_trading_signals(market_data, symbols)
            return {"signals": [self.signal_to_dict(s) for s in signals]}
        
        elif task_type == "optimize_portfolio":
            positions = task.get("positions", {})
            signals = task.get("signals", [])
            # Convert dict signals back to TradingSignal objects if needed
            return await self.optimize_portfolio(positions, signals)
        
        elif task_type == "assess_risk":
            symbol = task.get("symbol")
            data = task.get("data", {})
            prices = self._extract_price_data(data)
            if prices:
                indicators = self._calculate_technical_indicators(prices)
                if symbol is not None and isinstance(symbol, str):
                    risk_assessment = self._assess_risk(symbol, prices, indicators)
                    return {
                        "risk_score": risk_assessment.risk_score,
                        "risk_level": risk_assessment.risk_level.value,
                        "risk_factors": risk_assessment.risk_factors,
                        "mitigation_strategies": risk_assessment.mitigation_strategies
                    }
                else:
                    return {"error": "No valid symbol provided"}
            return {"error": "No valid price data"}
        
        else:
            return {"error": f"Unknown task type: {task_type}"}


# Global instance
_trading_strategist_agent = None


def get_trading_strategist_agent() -> TradingStrategistAgent:
    """Get the global trading strategist agent instance"""
    global _trading_strategist_agent
    if _trading_strategist_agent is None:
        _trading_strategist_agent = TradingStrategistAgent()
    return _trading_strategist_agent


if __name__ == "__main__":
    async def test_agent():
        agent = TradingStrategistAgent()
        
        # Test with sample market data
        test_data = {
            "AAPL": {
                "prices": [150, 151, 149, 152, 154, 153, 155, 157, 156, 158, 160, 159, 161, 163, 162, 164, 166, 165, 167, 169]
            }
        }
        
        signals = await agent.generate_trading_signals(test_data, ["AAPL"])
        
        for signal in signals:
            print(json.dumps(agent.signal_to_dict(signal), indent=2))
    
    asyncio.run(test_agent())

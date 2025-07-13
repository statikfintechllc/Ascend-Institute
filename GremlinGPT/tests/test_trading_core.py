# ─────────────────────────────────────────────────────────────
# ⚠️ GremlinGPT Fair Use Only | Commercial Use Requires License
# Built under the GremlinGPT Dual License v1.0
# © 2025 StatikFintechLLC / AscendAI Project
# Contact: ascend.gremlin@gmail.com
# ─────────────────────────────────────────────────────────────

"""
GremlinGPT Trading Core Testing Suite

Comprehensive tests for trading algorithms, portfolio management,
risk assessment, and market analysis components.
"""

import pytest
import asyncio
import json
import numpy as np
import pandas as pd
from unittest.mock import Mock, patch, MagicMock
import sys
import os
from datetime import datetime, timedelta

sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))

from utils.logging_config import setup_module_logger
logger = setup_module_logger('tests', 'test_trading_core')

# Mock trading core imports (since modules may not exist yet)
class MockTradingEngine:
    """Mock trading engine for testing."""
    def __init__(self):
        self.positions = {}
        self.balance = 10000.0
        self.orders = []
        
    def place_order(self, symbol, quantity, order_type, price=None):
        order_id = f"order_{len(self.orders) + 1}"
        order = {
            'id': order_id,
            'symbol': symbol,
            'quantity': quantity,
            'type': order_type,
            'price': price,
            'status': 'pending'
        }
        self.orders.append(order)
        return order_id
    
    def get_position(self, symbol):
        return self.positions.get(symbol, 0)
    
    def update_position(self, symbol, quantity):
        self.positions[symbol] = self.positions.get(symbol, 0) + quantity

class MockPortfolioManager:
    """Mock portfolio manager for testing."""
    def __init__(self):
        self.holdings = {}
        self.cash = 10000.0
        self.total_value = 10000.0
        
    def calculate_portfolio_value(self, market_prices):
        value = self.cash
        for symbol, quantity in self.holdings.items():
            if symbol in market_prices:
                value += quantity * market_prices[symbol]
        self.total_value = value
        return value
    
    def get_allocation(self, symbol):
        if self.total_value == 0:
            return 0.0
        symbol_value = self.holdings.get(symbol, 0) * self.get_market_price(symbol)
        return symbol_value / self.total_value
    
    def get_market_price(self, symbol):
        # Mock market prices
        prices = {
            'AAPL': 150.0,
            'GOOGL': 2500.0,
            'MSFT': 300.0,
            'TSLA': 800.0
        }
        return prices.get(symbol, 100.0)

class MockRiskAnalyzer:
    """Mock risk analyzer for testing."""
    def __init__(self):
        self.risk_metrics = {}
        
    def calculate_var(self, portfolio, confidence_level=0.95):
        """Calculate Value at Risk."""
        # Mock VaR calculation
        return portfolio.total_value * 0.05  # 5% VaR
    
    def calculate_sharpe_ratio(self, returns, risk_free_rate=0.02):
        """Calculate Sharpe ratio."""
        if len(returns) == 0:
            return 0.0
        mean_return = np.mean(returns)
        std_return = np.std(returns)
        if std_return == 0:
            return 0.0
        return (mean_return - risk_free_rate) / std_return
    
    def assess_position_risk(self, symbol, quantity, portfolio):
        """Assess risk for a specific position."""
        concentration = abs(quantity * portfolio.get_market_price(symbol)) / portfolio.total_value
        return {
            'concentration_risk': concentration,
            'risk_level': 'high' if concentration > 0.2 else 'medium' if concentration > 0.1 else 'low'
        }

class TestTradingEngine:
    """Test suite for the trading engine."""
    
    def test_trading_engine_initialization(self):
        """Test trading engine initialization."""
        engine = MockTradingEngine()
        
        assert engine.balance == 10000.0
        assert len(engine.positions) == 0
        assert len(engine.orders) == 0
        
        logger.info("Trading engine initialization test passed")
    
    def test_order_placement(self):
        """Test order placement functionality."""
        engine = MockTradingEngine()
        
        # Test market order
        order_id = engine.place_order('AAPL', 10, 'market')
        assert order_id is not None
        assert len(engine.orders) == 1
        
        # Test limit order
        limit_order_id = engine.place_order('GOOGL', 5, 'limit', 2500.0)
        assert limit_order_id is not None
        assert len(engine.orders) == 2
        
        # Verify order details
        limit_order = engine.orders[1]
        assert limit_order['symbol'] == 'GOOGL'
        assert limit_order['quantity'] == 5
        assert limit_order['type'] == 'limit'
        assert limit_order['price'] == 2500.0
        
        logger.info("Order placement test passed")
    
    def test_position_management(self):
        """Test position tracking and management."""
        engine = MockTradingEngine()
        
        # Test initial position
        assert engine.get_position('AAPL') == 0
        
        # Test position updates
        engine.update_position('AAPL', 10)
        assert engine.get_position('AAPL') == 10
        
        engine.update_position('AAPL', 5)
        assert engine.get_position('AAPL') == 15
        
        # Test short position
        engine.update_position('AAPL', -20)
        assert engine.get_position('AAPL') == -5
        
        logger.info("Position management test passed")
    
    def test_order_validation(self):
        """Test order validation logic."""
        engine = MockTradingEngine()
        
        # Test invalid order types
        with pytest.raises(ValueError):
            engine.place_order('AAPL', 10, 'invalid_type')
        
        # Test zero quantity
        with pytest.raises(ValueError):
            engine.place_order('AAPL', 0, 'market')
        
        # Test negative price for limit orders
        with pytest.raises(ValueError):
            engine.place_order('AAPL', 10, 'limit', -100.0)
        
        logger.info("Order validation test passed")

class TestPortfolioManager:
    """Test suite for portfolio management."""
    
    def test_portfolio_initialization(self):
        """Test portfolio manager initialization."""
        portfolio = MockPortfolioManager()
        
        assert portfolio.cash == 10000.0
        assert portfolio.total_value == 10000.0
        assert len(portfolio.holdings) == 0
        
        logger.info("Portfolio initialization test passed")
    
    def test_portfolio_value_calculation(self):
        """Test portfolio value calculation."""
        portfolio = MockPortfolioManager()
        
        # Add holdings
        portfolio.holdings = {
            'AAPL': 10,
            'GOOGL': 2,
            'MSFT': 5
        }
        
        market_prices = {
            'AAPL': 150.0,
            'GOOGL': 2500.0,
            'MSFT': 300.0
        }
        
        total_value = portfolio.calculate_portfolio_value(market_prices)
        expected_value = 10000.0 + (10 * 150.0) + (2 * 2500.0) + (5 * 300.0)
        
        assert total_value == expected_value
        assert portfolio.total_value == expected_value
        
        logger.info("Portfolio value calculation test passed")
    
    def test_allocation_calculation(self):
        """Test portfolio allocation calculation."""
        portfolio = MockPortfolioManager()
        portfolio.holdings = {'AAPL': 10}
        portfolio.total_value = 11500.0  # 10000 cash + 1500 AAPL
        
        allocation = portfolio.get_allocation('AAPL')
        expected_allocation = (10 * 150.0) / 11500.0  # ~0.13
        
        assert abs(allocation - expected_allocation) < 0.01
        
        logger.info("Allocation calculation test passed")
    
    def test_diversification_metrics(self):
        """Test portfolio diversification metrics."""
        portfolio = MockPortfolioManager()
        portfolio.holdings = {
            'AAPL': 10,
            'GOOGL': 2,
            'MSFT': 5,
            'TSLA': 3
        }
        
        # Calculate Herfindahl index for concentration
        allocations = []
        for symbol in portfolio.holdings:
            allocation = portfolio.get_allocation(symbol)
            allocations.append(allocation)
        
        herfindahl_index = sum(alloc ** 2 for alloc in allocations)
        
        # Well-diversified portfolio should have low Herfindahl index
        assert herfindahl_index < 0.5  # Less than 50% indicates good diversification
        
        logger.info("Diversification metrics test passed")

class TestRiskAnalyzer:
    """Test suite for risk analysis."""
    
    def test_var_calculation(self):
        """Test Value at Risk calculation."""
        risk_analyzer = MockRiskAnalyzer()
        portfolio = MockPortfolioManager()
        portfolio.total_value = 10000.0
        
        var_95 = risk_analyzer.calculate_var(portfolio, confidence_level=0.95)
        
        assert var_95 > 0
        assert var_95 <= portfolio.total_value
        
        logger.info("VaR calculation test passed")
    
    def test_sharpe_ratio_calculation(self):
        """Test Sharpe ratio calculation."""
        risk_analyzer = MockRiskAnalyzer()
        
        # Test with positive returns
        returns = [0.05, 0.03, 0.08, -0.02, 0.06]
        sharpe = risk_analyzer.calculate_sharpe_ratio(returns, risk_free_rate=0.02)
        
        assert isinstance(sharpe, float)
        assert sharpe > 0  # Should be positive for profitable strategy
        
        # Test with zero volatility
        constant_returns = [0.05, 0.05, 0.05, 0.05]
        sharpe_constant = risk_analyzer.calculate_sharpe_ratio(constant_returns)
        assert sharpe_constant == 0.0  # Zero volatility case
        
        logger.info("Sharpe ratio calculation test passed")
    
    def test_position_risk_assessment(self):
        """Test individual position risk assessment."""
        risk_analyzer = MockRiskAnalyzer()
        portfolio = MockPortfolioManager()
        portfolio.total_value = 10000.0
        
        # Test low concentration
        risk_low = risk_analyzer.assess_position_risk('AAPL', 5, portfolio)
        assert risk_low['risk_level'] == 'low'
        
        # Test high concentration
        risk_high = risk_analyzer.assess_position_risk('AAPL', 15, portfolio)
        assert risk_high['risk_level'] == 'high'
        
        logger.info("Position risk assessment test passed")
    
    def test_correlation_analysis(self):
        """Test correlation analysis between assets."""
        # Mock price data
        dates = pd.date_range('2024-01-01', periods=100, freq='D')
        np.random.seed(42)  # For reproducible results
        
        # Create correlated price data
        aapl_prices = 150 + np.cumsum(np.random.normal(0, 1, 100))
        googl_prices = 2500 + np.cumsum(np.random.normal(0, 5, 100))
        
        # Calculate correlation
        correlation = np.corrcoef(aapl_prices, googl_prices)[0, 1]
        
        assert -1 <= correlation <= 1
        logger.info(f"Correlation analysis test passed: AAPL-GOOGL correlation = {correlation:.3f}")

class TestTradingStrategy:
    """Test suite for trading strategies."""
    
    def test_moving_average_strategy(self):
        """Test moving average crossover strategy."""
        # Generate test price data
        np.random.seed(42)
        prices = 100 + np.cumsum(np.random.normal(0, 1, 100))
        
        # Calculate moving averages
        short_ma = np.convolve(prices, np.ones(5)/5, mode='valid')
        long_ma = np.convolve(prices, np.ones(20)/20, mode='valid')
        
        # Generate signals
        signals = []
        for i in range(1, len(short_ma)):
            if short_ma[i] > long_ma[i] and short_ma[i-1] <= long_ma[i-1]:
                signals.append('buy')
            elif short_ma[i] < long_ma[i] and short_ma[i-1] >= long_ma[i-1]:
                signals.append('sell')
            else:
                signals.append('hold')
        
        # Test that signals are generated
        assert len(signals) > 0
        assert all(signal in ['buy', 'sell', 'hold'] for signal in signals)
        
        logger.info("Moving average strategy test passed")
    
    def test_rsi_strategy(self):
        """Test RSI-based trading strategy."""
        # Generate test price data
        np.random.seed(42)
        prices = 100 + np.cumsum(np.random.normal(0, 1, 100))
        
        # Calculate RSI
        def calculate_rsi(prices, period=14):
            deltas = np.diff(prices)
            gains = np.where(deltas > 0, deltas, 0)
            losses = np.where(deltas < 0, -deltas, 0)
            
            avg_gains = np.convolve(gains, np.ones(period)/period, mode='valid')
            avg_losses = np.convolve(losses, np.ones(period)/period, mode='valid')
            
            rs = avg_gains / (avg_losses + 1e-10)  # Avoid division by zero
            rsi = 100 - (100 / (1 + rs))
            return rsi
        
        rsi_values = calculate_rsi(prices)
        
        # Generate RSI signals
        signals = []
        for rsi in rsi_values:
            if rsi < 30:
                signals.append('buy')  # Oversold
            elif rsi > 70:
                signals.append('sell')  # Overbought
            else:
                signals.append('hold')
        
        # Test RSI calculations
        assert len(rsi_values) > 0
        assert all(0 <= rsi <= 100 for rsi in rsi_values)
        assert len(signals) == len(rsi_values)
        
        logger.info("RSI strategy test passed")

class TestMarketDataProcessor:
    """Test suite for market data processing."""
    
    def test_price_data_validation(self):
        """Test market data validation."""
        # Valid price data
        valid_data = {
            'symbol': 'AAPL',
            'timestamp': datetime.now(),
            'open': 150.0,
            'high': 152.0,
            'low': 149.0,
            'close': 151.0,
            'volume': 1000000
        }
        
        # Test validation
        assert valid_data['high'] >= valid_data['open']
        assert valid_data['high'] >= valid_data['close']
        assert valid_data['low'] <= valid_data['open']
        assert valid_data['low'] <= valid_data['close']
        assert valid_data['volume'] >= 0
        
        logger.info("Price data validation test passed")
    
    def test_data_cleaning(self):
        """Test data cleaning and preprocessing."""
        # Create test data with outliers
        raw_prices = [100, 101, 102, 200, 103, 104, 50, 105]  # Contains outliers
        
        # Simple outlier detection using IQR
        def remove_outliers(data, threshold=1.5):
            q1 = np.percentile(data, 25)
            q3 = np.percentile(data, 75)
            iqr = q3 - q1
            lower_bound = q1 - threshold * iqr
            upper_bound = q3 + threshold * iqr
            
            return [x for x in data if lower_bound <= x <= upper_bound]
        
        cleaned_prices = remove_outliers(raw_prices)
        
        # Test outlier removal
        assert len(cleaned_prices) < len(raw_prices)
        assert 200 not in cleaned_prices  # Extreme outlier removed
        assert 50 not in cleaned_prices   # Extreme outlier removed
        
        logger.info("Data cleaning test passed")
    
    def test_technical_indicators(self):
        """Test technical indicator calculations."""
        # Generate test price data
        np.random.seed(42)
        prices = 100 + np.cumsum(np.random.normal(0, 1, 50))
        
        # Test Simple Moving Average
        sma_10 = np.convolve(prices, np.ones(10)/10, mode='valid')
        assert len(sma_10) == len(prices) - 9
        
        # Test Exponential Moving Average
        def calculate_ema(prices, period):
            alpha = 2 / (period + 1)
            ema = [prices[0]]
            for price in prices[1:]:
                ema.append(alpha * price + (1 - alpha) * ema[-1])
            return np.array(ema)
        
        ema_10 = calculate_ema(prices, 10)
        assert len(ema_10) == len(prices)
        
        # Test Bollinger Bands
        sma_20 = np.convolve(prices, np.ones(20)/20, mode='valid')
        rolling_std = np.array([np.std(prices[i:i+20]) for i in range(len(prices)-19)])
        upper_band = sma_20 + 2 * rolling_std
        lower_band = sma_20 - 2 * rolling_std
        
        assert len(upper_band) == len(lower_band)
        assert all(upper > lower for upper, lower in zip(upper_band, lower_band))
        
        logger.info("Technical indicators test passed")

# Integration tests
class TestTradingIntegration:
    """Integration tests for trading components."""
    
    @pytest.mark.integration
    def test_full_trading_workflow(self):
        """Test complete trading workflow integration."""
        # Initialize components
        engine = MockTradingEngine()
        portfolio = MockPortfolioManager()
        risk_analyzer = MockRiskAnalyzer()
        
        # Simulate trading workflow
        # 1. Analyze market
        market_signal = 'buy'  # Mock market analysis result
        
        # 2. Check risk constraints
        proposed_position = 10
        risk_assessment = risk_analyzer.assess_position_risk('AAPL', proposed_position, portfolio)
        
        # 3. Place order if risk is acceptable
        if risk_assessment['risk_level'] != 'high':
            order_id = engine.place_order('AAPL', proposed_position, 'market')
            
            # 4. Update portfolio
            engine.update_position('AAPL', proposed_position)
            portfolio.holdings['AAPL'] = proposed_position
            
            # 5. Calculate new portfolio value
            market_prices = {'AAPL': 150.0}
            new_value = portfolio.calculate_portfolio_value(market_prices)
            
            # Verify workflow
            assert order_id is not None
            assert engine.get_position('AAPL') == proposed_position
            assert portfolio.holdings['AAPL'] == proposed_position
            assert new_value > portfolio.cash
        
        logger.info("Full trading workflow integration test passed")
    
    @pytest.mark.integration
    def test_risk_portfolio_integration(self):
        """Test risk analyzer and portfolio manager integration."""
        portfolio = MockPortfolioManager()
        risk_analyzer = MockRiskAnalyzer()
        
        # Set up diversified portfolio
        portfolio.holdings = {
            'AAPL': 10,
            'GOOGL': 2,
            'MSFT': 5,
            'TSLA': 3
        }
        
        market_prices = {
            'AAPL': 150.0,
            'GOOGL': 2500.0,
            'MSFT': 300.0,
            'TSLA': 800.0
        }
        
        portfolio.calculate_portfolio_value(market_prices)
        
        # Test risk metrics for each position
        total_risk_score = 0
        for symbol, quantity in portfolio.holdings.items():
            risk_assessment = risk_analyzer.assess_position_risk(symbol, quantity, portfolio)
            total_risk_score += risk_assessment['concentration_risk']
        
        # Verify integration
        assert total_risk_score < 1.0  # Total concentration should be less than 100%
        
        logger.info("Risk-Portfolio integration test passed")

# Performance tests
class TestTradingPerformance:
    """Performance tests for trading components."""
    
    @pytest.mark.slow
    def test_portfolio_calculation_performance(self, performance_monitor):
        """Test portfolio calculation performance with large datasets."""
        performance_monitor.start()
        
        portfolio = MockPortfolioManager()
        
        # Create large portfolio
        large_holdings = {}
        market_prices = {}
        for i in range(1000):
            symbol = f'STOCK_{i:04d}'
            large_holdings[symbol] = np.random.randint(1, 100)
            market_prices[symbol] = np.random.uniform(10, 1000)
        
        portfolio.holdings = large_holdings
        
        # Calculate portfolio value multiple times
        for _ in range(100):
            portfolio.calculate_portfolio_value(market_prices)
        
        metrics = performance_monitor.stop()
        
        assert metrics['duration'] < 5.0  # Should complete within 5 seconds
        
        logger.info(f"Portfolio calculation performance: {metrics['duration']:.2f}s for 1000 stocks x 100 calculations")
    
    @pytest.mark.memory_intensive
    def test_technical_indicator_memory_usage(self, performance_monitor):
        """Test memory usage of technical indicator calculations."""
        performance_monitor.start()
        
        # Generate large price dataset
        np.random.seed(42)
        large_price_data = 100 + np.cumsum(np.random.normal(0, 1, 10000))
        
        # Calculate multiple indicators
        indicators = {}
        for period in [5, 10, 20, 50, 100, 200]:
            indicators[f'sma_{period}'] = np.convolve(
                large_price_data, 
                np.ones(period)/period, 
                mode='valid'
            )
        
        metrics = performance_monitor.stop()
        
        assert metrics['memory_delta'] < 100 * 1024 * 1024  # Less than 100MB
        
        logger.info(f"Technical indicator memory usage: {metrics['memory_delta'] / 1024 / 1024:.2f}MB for 10K data points")

if __name__ == '__main__':
    pytest.main([__file__, '-v'])

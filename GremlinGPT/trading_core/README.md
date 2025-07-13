# Trading Core Module

The `trading_core` module implements GremlinGPT's financial trading capabilities, including market analysis, portfolio management, signal generation, and automated trading operations.

## Components

### 📊 signal_generator.py
**Trading Signal Generation**
- Technical analysis and indicator calculation
- Market pattern recognition
- Buy/sell signal generation
- Risk assessment and validation

### 📈 portfolio_tracker.py
**Portfolio Management System**
- Position tracking and monitoring
- Performance analytics and reporting
- Risk management and exposure analysis
- Asset allocation optimization

### ⚖️ rules_engine.py
**Trading Rules and Logic**
- Trading rule definition and execution
- Strategy backtesting and validation
- Risk management rule enforcement
- Compliance and regulatory checks

### 💰 tax_estimator.py
**Tax Calculation and Optimization**
- Tax liability estimation
- Tax-loss harvesting strategies
- Wash sale rule compliance
- Tax-efficient trading recommendations

### 📰 stock_scraper.py
**Market Data Collection**
- Real-time market data scraping
- News and sentiment analysis
- Economic indicator monitoring
- Alternative data source integration

## Architecture

```text
┌─────────────────┐    ┌─────────────────┐    ┌─────────────────┐
│ Signal Generator│────│Portfolio Tracker│────│  Rules Engine   │
│   (Analysis)    │    │  (Management)   │    │   (Logic)       │
└─────────────────┘    └─────────────────┘    └─────────────────┘
         │                       │                       │
         └───────────────────────┼───────────────────────┘
                                 │
         ┌───────────────────────┼───────────────────────┐
         │                       │                       │
┌─────────────────┐    ┌─────────────────┐
│ Stock Scraper   │    │ Tax Estimator   │
│ (Data Source)   │    │ (Optimization)  │
└─────────────────┘    └─────────────────┘
```

## Key Features

- **Automated Trading**: Fully automated trading signal execution
- **Risk Management**: Comprehensive risk assessment and control
- **Tax Optimization**: Tax-efficient trading strategies
- **Real-time Analysis**: Live market data processing
- **Portfolio Management**: Complete portfolio tracking and optimization

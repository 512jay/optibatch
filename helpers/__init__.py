# File: helpers/enums.py

optimization_options = {
    "Disabled": "disabled",
    "Slow (complete algorithm)": "slow",
    "Fast (genetic based algorithm)": "fast",
    "All symbols in MarketWatch": "marketwatch",
}

result_priority_options = {
    "Balance Max": "balance max",
    "Profit Factor Max": "profit factor max",
    "Expected Payoff Max": "expected payoff max",
    "Drawdown Min": "drawdown min",
    "Recovery Factor Max": "recovery factor max",
    "Sharpe Ratio Max": "sharpe ratio max",
    "Custom Max": "custom max",
    "Complex Criterion Max": "complex criterion max",
}

forward_mode_map = {"NO": "0", "1/4": "1", "1/2": "2", "1/3": "3", "custom": "4"}

# helpers/enums.py

# core/constants/enums.py or wherever enums are defined

optimization_mode_map = {
    "Disabled": 0,
    "Slow (complete algorithm)": 1,
    "Fast (genetic based algorithm)": 2,
    "All symbols in MarketWatch": 3,
}

# Reverse map: int to readable label
optimization_mode_reverse = {v: k for k, v in optimization_mode_map.items()}


result_priority_map = {
    "Balance Max": 0,
    "Profit Factor Max": 1,
    "Expected Payoff Max": 2,
    "Drawdown Min": 3,
    "Recovery Factor Max": 4,
    "Sharpe Ratio Max": 5,
    "Custom Max": 6,
    "Complex Criterion Max": 7,
}

# Reverse mapping: int to readable name
result_priority_reverse = {v: k for k, v in result_priority_map.items()}


forward_mode_map = {
    "NO": 0,
    "1/2": 1,
    "1/3": 2,
    "1/4": 3,
    "Custom (date specified)": 4,
}

# Reverse map: int to readable label
forward_mode_reverse = {v: k for k, v in forward_mode_map.items()}

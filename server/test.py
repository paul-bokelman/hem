from lib.claude_tools import get_time, get_weather, get_stock_info, get_crypto_price

# Basic manual tests with print statements
print("Current time:", get_time())

# print("Stock Price", get_stock_info(["NVDA", "INTC"]))

# Test weather for a known city
print(get_weather("Austin"))

print( get_crypto_price("ethereum", "usd"))

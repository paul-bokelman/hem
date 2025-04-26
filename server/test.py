from lib.actions import Actions

test_action = Actions()

print(test_action.get_date())
print(test_action.get_weather("Atlanta"))
print(test_action.get_time())
print(test_action.get_crypto_price("bitcoin", "usd"))
print(test_action.get_stock_info(["NVDA", "INTC"]))
# main.py (or any other module)
import shioaji as sj
from login_test import login  # Assuming login_test.py is in the same directory
from shioaji.constant import Action, StockPriceType, OrderType

# Get the api object by calling the login() function
api = login()

# Check if api is successfully retrieved
if api is not None:
    contract = api.Contracts.Stocks["2330"]
    print("==================")
    print(f"Contract: {contract}")
    print("==================")
else:
    print("Failed to initialize the API.")


order = sj.order.StockOrder(
    action=Action.Buy, # Buy
    price=contract.reference, # Buy at the reference price
    quantity=1, # Order quantity
    price_type=StockPriceType.LMT, # Limit price order
    order_type=OrderType.ROD, # Effective for the day
    account=api.stock_account, # Use the default account
)
print(f"Order: {order}")
print("==================")
# send order
trade = api.place_order(contract=contract, order=order)
print(f"Trade: {trade}")
print("==================")
# Update the status
api.update_status()
print(f"Status: {trade.status}")
print("=======order_datetime=========")
print(trade.status.order_datetime)
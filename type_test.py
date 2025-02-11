from shioaji.constant import (
    FuturesPriceType,
    FuturesOCType,
)

import shioaji as sj
from login_test import login  # Assuming login_test.py is in the same directory
from shioaji.constant import Action, StockPriceType, OrderType
import time
from shioaji import TickFOPv1, BidAskFOPv1, Exchange

api = login()

contracts = [api.Contracts.Stocks['2330']]
snapshot = api.snapshots(contracts)
print("snapshot:", snapshot)

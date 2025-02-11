from datetime import datetime
import shioaji as sj
from shioaji import TickFOPv1, BidAskFOPv1, Exchange
from login_test import login  # Assuming login_test.py is in the same directory
import time
last_tick_time = None
last_bidask_time = None
api = login()



# Track last update times
last_tick_time = None
last_bidask_time = None

@api.on_tick_fop_v1()
def quote_callback(exchange, tick):
    global last_tick_time
    current_time = tick.datetime  # Tick's timestamp
    if last_tick_time:
        diff = (current_time - last_tick_time).total_seconds()
        print(f"=====Tick Update Interval: {diff:.6f} seconds=====")
    last_tick_time = current_time
    print(f"Exchange: {exchange}, Tick: {tick}")

@api.on_bidask_fop_v1()
def bidask_callback(exchange, bidask):
    global last_bidask_time
    current_time = bidask.datetime  # BidAsk's timestamp
    if last_bidask_time:
        diff = (current_time - last_bidask_time).total_seconds()
        print(f"BidAsk Update Interval: {diff:.6f} seconds")
    last_bidask_time = current_time
    print(f"Exchange: {exchange}, BidAsk: {bidask}")

# Subscribe to TMF Futures Contract (No update_interval)
ftu_tmf2502 = api.Contracts.Futures.TMF.TMF202502

api.quote.subscribe(
    ftu_tmf2502,
    quote_type=sj.constant.QuoteType.Tick,
    version=sj.constant.QuoteVersion.v1
)



print("Listening for market data updates for 5 seconds...")
time.sleep(5)  # Keeps the script running
print("Time is up! Exiting...")
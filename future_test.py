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

@api.on_tick_fop_v1()
def quote_callback(exchange: Exchange, tick: TickFOPv1):
    print("=====quote_callback=====")
    print(f"Exchange: {exchange}, Tick: {tick}")



@api.on_bidask_fop_v1()
def quote_callback(exchange: Exchange, bidask: BidAskFOPv1):
    print("=====bidask_fop=====")
    print(f"Exchange: {exchange}, BidAsk: {bidask}")


@api.quote.on_event
def event_callback(resp_code: int, event_code: int, info: str, event: str):
    print("=====on_event=====")
    print(f'Response code: {resp_code} | Event code: {event_code} | Event: {event}')


ftu_tmf2502 = api.Contracts.Futures.TMF.TMF202502

api.quote.subscribe(
    ftu_tmf2502,
    quote_type=sj.constant.QuoteType.Tick,
    version=sj.constant.QuoteVersion.v1
)

api.quote.subscribe(
    ftu_tmf2502,
    quote_type=sj.constant.QuoteType.BidAsk,
    version=sj.constant.QuoteVersion.v1
)

print("Listening for market data updates for 5 seconds...")
time.sleep(5)  # Keeps the script running
print("Time is up! Exiting...")
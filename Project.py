import logging


logging.basicConfig(
filename="bot.log",
level=logging.INFO,
format="%(asctime)s | %(levelname)s | %(message)s"
)


logger = logging.getLogger("trading_bot")
from binance.client import Client
from bot.logging_config import logger
import os


TESTNET_URL = "https://testnet.binancefuture.com"


class BinanceFuturesClient:
  def __init__(self):
   self.client = Client(
api_key=os.getenv("BINANCE_API_KEY"),
api_secret=os.getenv("BINANCE_API_SECRET")
)
   self.client.FUTURES_URL = TESTNET_URL
logger.info("Initialized Binance Futures Testnet client")
def validate_symbol(symbol: str):
  if not symbol.endswith("USDT"):
   raise ValueError("Only USDT-M symbols are supported")




def validate_side(side: str):
  if side not in {"BUY", "SELL"}:
   raise ValueError("Side must be BUY or SELL")




def validate_order_type(order_type: str):
  if order_type not in {"MARKET", "LIMIT", "STOP_LIMIT"}:
   raise ValueError("Invalid order type")




def validate_quantity(qty: float):
  if qty <= 0:
   raise ValueError("Quantity must be positive")




def validate_price(price):
  if price is None or price <= 0:
   raise ValueError("Price must be provided and positive")
from bot.logging_config import logger
from bot.validators import *


class OrderService:
  def __init__(self, client):
   self.client = client


def place_market(self, symbol, side, qty):
 validate_symbol(symbol)
 validate_side(side)
 validate_quantity(qty)


logger.info(f"Placing MARKET order: {symbol} {side} {qty}")
return self.client.futures_create_order(
symbol=symbol,
side=side,
type="MARKET",
quantity=qty
)


def place_limit(self, symbol, side, qty, price):
 validate_symbol(symbol)
 validate_side(side)
 validate_quantity(qty)
 validate_price(price)


logger.info(f"Placing LIMIT order: {symbol} {side} {qty} @ {price}")
return self.client.futures_create_order(
symbol=symbol,
side=side,
type="LIMIT",
quantity=qty,
price=price,
timeInForce="GTC"
)


def place_stop_limit(self, symbol, side, qty, stop_price, limit_price):
 validate_price(stop_price)
 validate_price(limit_price)


logger.info(f"Placing STOP-LIMIT order: {symbol} {side}")
 return self.client.futures_create_order(
symbol=symbol,
side=side,
type="STOP",
quantity=qty,
stopPrice=stop_price,
price=limit_price,
timeInForce="GTC"
)
 import argparse
 from bot.client import BinanceFuturesClient
 from bot.orders import OrderService
 from bot.logging_config import logger




 def main():
  parser = argparse.ArgumentParser(description="Binance Futures Testnet Bot")
  parser.add_argument("--symbol", required=True)
  parser.add_argument("--side", required=True, choices=["BUY", "SELL"])
  parser.add_argument("--type", required=True, choices=["MARKET", "LIMIT", "STOP_LIMIT"])
  parser.add_argument("--qty", required=True, type=float)
  parser.add_argument("--price", type=float)
  parser.add_argument("--stop_price", type=float)


 args = parser.parse_args()


 client = BinanceFuturesClient().client
 service = OrderService(client)


try:
 if args.type == "MARKET":
  res = service.place_market(args.symbol, args.side, args.qty)
 elif args.type == "LIMIT":
  res = service.place_limit(args.symbol, args.side, args.qty, args.price)
 else:
  res = service.place_stop_limit(
  args.symbol, args.side, args.qty, args.stop_price, args.price
)


print("\nOrder placed successfully")
print(f"Order ID: {res.get('orderId')}")
print(f"Status: {res.get('status')}")
print(f"Executed Qty: {res.get('executedQty')}")
print(f"Avg Price: {res.get('avgPrice', 'N/A')}")
logger.info(res)


 except Exception as e:
 logger.error(str(e))
 print("Order failed:", e)




 if __name__ == "__main__":
  main()
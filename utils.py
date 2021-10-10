# Util functions
import hmac
import hashlib
import base64
import time
import random
import string
from configs import logging
from configs import API_KEY, API_SECRET, UPDATE_TICK_RATE
incrementer = 0


def sign(endpoint: str, nonce: int, data: str = ''):
    strToBeSigned = ('v1/%s%d%s' % (endpoint, nonce, data)).encode('utf-8')
    hashBuffer = base64.b64encode(strToBeSigned)
    sign_data = hmac.new(
        API_SECRET.encode(),
        hashBuffer,
        hashlib.sha384
    ).hexdigest()
    return sign_data


# Generate a headers
def headers(endpoint: str, data: str = ''):
    nonce_now = nonce()
    return {
        "Content-Type": "application/json",
        "BSCNT-NONCE": str(nonce_now),
        "BSCNT-APIKEY": API_KEY,
        "BSCNT-SIGN": sign(endpoint, nonce_now, data),
    }


def nonce(): return int(time.time() * 1000000)  # Generate a nonce


def percent(value1, value2): return round(
    (float(value2) / float(value1) - 1) * 100, 3)  # Calculate percent by numbers


def can_buy(brl, min_brl=10): return float(brl) >= float(
    min_brl)  # verify if you have enough money


def btcToTrade(max_brl, quote_amount, base_amount): return (
    max_brl * base_amount) / quote_amount  # calculate min value of btc to trade from brl


# Log the current cycle every n times on loop
def showCycle(cycle_count, percent, at_every: int = 20):
    if cycle_count % at_every == 0:
        logging.info(f"Cycle {cycle_count} | Last percent : {percent} |")


def gen_random(size=17):
    return ''.join(random.choice(string.ascii_lowercase + string.digits) for _ in range(size))

# Generate params of offer


def genOfferParams(base='BTC', quote='BRL', op="buy", amount=0.0001, is_quote=False):
    params = {"base": base, "quote": quote, "op": op,
              "amount": "0.0001", "isQuote": is_quote, "requestId": gen_random()}
    return params

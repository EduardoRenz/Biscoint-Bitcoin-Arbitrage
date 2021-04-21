import time
from datetime import datetime as dt
from biscoint_api_python import Biscoint
from playsound import playsound
from utils import percent,btcToTrade
from configs import logging
from configs import API_KEY, API_SECRET, MIN_PERCENT_REQUIRED, BASE_URL, BRL_AMOUNT_TRADE, UPDATE_TICK_RATE

# Initial configs
bsc = Biscoint(API_KEY, API_SECRET)

#Return initial balance from Biscoint
initial_balance = last_balance = bsc.get_balance()
# Calculate the rate limit of request to Biscoint API
endpoints_meta = bsc.get_meta()
rate_limit_offer = endpoints_meta['endpoints']['offer']['post']['rateLimit']
sleep_time_offers = ((rate_limit_offer["windowMs"] / rate_limit_offer["maxRequests"]) / 1000) * 2
# Convert the BRL amount of trading to BTC
ticker = bsc.get_ticker()
amount_btc_to_trade = btcToTrade(BRL_AMOUNT_TRADE,ticker['askQuoteAmountRef'],ticker['bidBaseAmountRef'])

percent_record = -1 # Will refresh every time when a new positive spread is achived

logging.info(f"Initial balance: {initial_balance}",)
# Arbitrage Cycle
cycle_count = 1

def updateTick(cycle_count):
    if cycle_count % UPDATE_TICK_RATE == 0:
        try:
            ticker = bsc.get_ticker()
            amount_btc_to_trade = btcToTrade(BRL_AMOUNT_TRADE,ticker['askQuoteAmountRef'],ticker['bidBaseAmountRef'])
        except Exception as e:
            logging.error(f"Error on updating tick {e}")

# if spread is high, sleep, else speed up checks
def waitForNextCycle(calculated_percent):
    if calculated_percent < -0.3:
        time.sleep(sleep_time_offers)
    else:
        time.sleep(1)
        
# Log the current cycle every n times on loop
def showCycle(cycle_count, percent, at_every:int=20):
    if cycle_count % at_every == 0:
        logging.info(f"Cycle {cycle_count} | Last percent : {percent} |")

while True:
    try:
        start_time = dt.now()
        # Get buy and sell offers of this cycle
        buy = bsc.get_offer(op='buy',amount=str(amount_btc_to_trade),isQuote=False)
        sell = bsc.get_offer(op='sell',amount=str(amount_btc_to_trade),isQuote=False)
        # Calculate if arbitrage is possible
        calculated_percent = percent(buy['efPrice'],sell['efPrice'])

        showCycle(cycle_count,calculated_percent)
        
        if calculated_percent > percent_record:
            logging.info(f"Percent Record Reached!! : {calculated_percent}")
            percent_record = calculated_percent
        # If Arbitrage is possible, confirm offers
        if calculated_percent >= MIN_PERCENT_REQUIRED:
            logging.info(f"Arbitrage oportunity: buy:{buy['efPrice']}   sell:{sell['efPrice']}")
            playsound('beep.wav')
            #Execute orders
            executed_buy = bsc.confirm_offer(buy['offerId'])
            executed_sell = bsc.confirm_offer(sell['offerId'])
            logging.info(executed_buy)
            logging.info(executed_sell)

            last_balance = bsc.get_balance()
            logging.info(f"New Balance is: {last_balance}")
            

        end_time = dt.now()
        seconds_elapsed = (end_time - start_time).total_seconds()
        logging.debug(f"Cycle took {seconds_elapsed} seconds")
        cycle_count +=1

        updateTick(cycle_count)
        waitForNextCycle(calculated_percent)
    except Exception as e:
        logging.error(e)
import time
from datetime import datetime as dt
from biscoint_api_python import Biscoint
from playsound import playsound
from utils import percent,btcToTrade
from configs import logging
from configs import API_KEY, API_SECRET, AMOUNT, MIN_PERCENT_REQUIRED, BASE_URL, BRL_AMOUNT_TRADE

# Initial configs
bsc = Biscoint(API_KEY, API_SECRET)
endpoints_meta = bsc.get_meta()
rate_limit_offer = endpoints_meta['endpoints']['offer']['post']['rateLimit']
sleep_time_offers = ((rate_limit_offer["windowMs"] / rate_limit_offer["maxRequests"]) / 1000)*2
initial_balance = bsc.get_balance()
last_balance = initial_balance
ticker = bsc.get_ticker()
amount_btc_to_trade = btcToTrade(BRL_AMOUNT_TRADE,ticker['askQuoteAmountRef'],ticker['bidBaseAmountRef'])

logging.info(f"Initial balance: {initial_balance}",)
percent_record = -1

# Arbitrage Cycle
cycle_count = 1
while True:
    try:
        start_time = dt.now()

        buy = bsc.get_offer(op='buy',amount=str(amount_btc_to_trade),isQuote=False)
        sell = bsc.get_offer(op='sell',amount=str(amount_btc_to_trade),isQuote=False)

        calculated_percent = percent(buy['efPrice'],sell['efPrice'])
        logging.info(f"Percent is {calculated_percent} | Cycle {cycle_count}")

        if calculated_percent > percent_record:
            logging.info(f"Percent Record Reached!! : {calculated_percent}")
            percent_record = calculated_percent

        if(calculated_percent >= MIN_PERCENT_REQUIRED):
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

        #print(f"Took {seconds_elapsed} seconds")
        if cycle_count % 2 == 0:
            try:
                ticker = bsc.get_ticker()
                amount_btc_to_trade = btcToTrade(BRL_AMOUNT_TRADE,ticker['askQuoteAmountRef'],ticker['bidBaseAmountRef'])
            except Exception as e:
                pass

        cycle_count +=1

        # if spead is high, sleep
        if calculated_percent < -0.3:
            time.sleep(sleep_time_offers)
        else:
            time.sleep(2)
    except Exception as e:
        print(e)
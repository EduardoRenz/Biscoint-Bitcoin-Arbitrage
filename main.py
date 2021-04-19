import time
from datetime import datetime as dt
from biscoint_api_python import Biscoint
from playsound import playsound
from utils import percent
from configs import logging
from configs import API_KEY,API_SECRET,AMOUNT,MIN_PERCENT_REQUIRED,BASE_URL

# Initial configs
bsc = Biscoint(API_KEY, API_SECRET)
endpoints_meta = bsc.get_meta()
rate_limit_offer = endpoints_meta['endpoints']['offer']['post']['rateLimit']
sleep_time_offers = ((rate_limit_offer["windowMs"] / rate_limit_offer["maxRequests"]) / 1000)*2
initial_balance = bsc.get_balance()
last_balance = initial_balance
logging.info(f"Initial balance: {initial_balance}",)
percent_record = -1000

# Arbitrage Cycle
while True:
    start_time = dt.now()
    buy = bsc.get_offer(op='buy',amount=AMOUNT,isQuote=False)
    sell = bsc.get_offer(op='sell',amount=AMOUNT,isQuote=False)

    calculated_percent = percent(buy['efPrice'],sell['efPrice'])
    print(f"Percent is {calculated_percent}")

    if calculated_percent > percent_record:
        logging.info(f"Percent Record Reached!! : {calculated_percent}")
        percent_record = calculated_percent

    if(calculated_percent >= MIN_PERCENT_REQUIRED):
        logging.info(f"Arbitrage oportunity: buy:{buy['efPrice']}   sell:{sell['efPrice']}")
        playsound('beep.wav')
        #Execute orders
        executed_sell = bsc.confirm_offer(sell['offerId'])
        executed_buy = bsc.confirm_offer(buy['offerId'])
        last_balance = bsc.get_balance()
        logging.info(f"New Balance is: {last_balance}")
        break

    end_time = dt.now()
    seconds_elapsed = (end_time - start_time).total_seconds()
    logging.debug(f"Cycle took {seconds_elapsed} seconds")
    
    time.sleep(sleep_time_offers)
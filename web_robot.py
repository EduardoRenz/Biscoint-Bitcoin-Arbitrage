from selenium import webdriver
import time
import threading
from utils import amountToBase, showCycle, percent
from configs import logging, MIN_PERCENT_REQUIRED, BRL_AMOUNT_TRADE, UPDATE_TICK_RATE, LOGIN_TOKEN
from datetime import datetime as dt
from playsound import playsound
from classes.Robots import WebRobot, BiscointRobot
import argparse
parser = argparse.ArgumentParser(description='Process some integers.')
parser.add_argument('--base','-b', default='BTC',  type=str, choices=['BTC','ETH'], help='crypto to trade')

base =  parser.parse_args().base
logging.info(f"Starting arbitrage of {base}")

# Selenium
options = webdriver.FirefoxOptions()
options.add_argument('--headless')
driver = webdriver.Firefox(options=options)

driver.get("https://biscoint.io")
driver.execute_script(f"window.localStorage.setItem('Meteor.loginToken','{LOGIN_TOKEN}');")
driver.get("https://biscoint.io/dashboard/portfolio")

# Web Robot
web_robot = WebRobot(driver)
biscoint_robot = BiscointRobot()


# %%
def updateTick(cycle_count):
    global ticker
    global amount_btc_to_trade
    if cycle_count % UPDATE_TICK_RATE == 0:
        try:
            ticker = web_robot.api.get_ticker(base=base)
            amount_btc_to_trade =  amountToBase(BRL_AMOUNT_TRADE,ticker['askQuoteAmountRef'],ticker['bidBaseAmountRef'])
        except Exception as e:
            logging.error(f"Error on updating tick {e}")

# if spread is high, sleep, else speed up checks
def waitForNextCycle(calculated_percent):
    if calculated_percent < -0.1:
        time.sleep(sleep_time_offers)
    else:
        time.sleep(0.05)

def async_offer(robot, op:str,amount:str,isQuote:bool,base:str):
    global request_orders
    response = None
    try:
        response = robot.get_offer(op,amount,isQuote,base=base) 
        request_orders[op] = response
    except Exception as e:
        print(response)
        print("Erro ao rodar thread",e)


# %%
#Return initial balance from Biscoint
initial_balance = last_balance = web_robot.api.get_balance()
# Calculate the rate limit of request to Biscoint API
endpoints_meta = web_robot.api.get_meta()
rate_limit_offer = endpoints_meta['endpoints']['offer']['post']['rateLimit']
sleep_time_offers = ((rate_limit_offer["windowMs"] / rate_limit_offer["maxRequests"]) / 1000) * 1.5
# Convert the BRL amount of trading to BTC
ticker = web_robot.api.get_ticker(base=base)

amount_btc_to_trade = amountToBase(BRL_AMOUNT_TRADE,ticker['askQuoteAmountRef'], ticker['bidBaseAmountRef'])

percent_record = -1 # Will refresh every time when a new positive spread is achived

logging.info(f"Initial balance: {initial_balance}")
# Arbitrage Cycle
cycle_count = 1


# %%
assert async_offer
while True:
    try:
        start_time = dt.now()

        # Get Offers in thread
        request_orders = {}
        thread_buy = threading.Thread(target=async_offer, args=(web_robot, 'buy',str(amount_btc_to_trade), False, base))
        thread_sell = threading.Thread(target=async_offer, args=(biscoint_robot,'sell',str(amount_btc_to_trade), False, base))
        thread_buy.start()
        thread_sell.start()
        thread_buy.join()
        thread_sell.join()

        # Get buy and sell offers of this cycle
        buy = request_orders['buy']
        sell = request_orders['sell']

        # Calculate if arbitrage is possible
        calculated_percent = percent(buy['efPrice'],sell['efPrice'])

        showCycle(cycle_count,calculated_percent)
        
        if calculated_percent > percent_record:
            logging.info(f"Percent Record Reached!! : {calculated_percent} at {dt.now()}")
            percent_record = calculated_percent
        # If Arbitrage is possible, confirm offers
        if calculated_percent >= MIN_PERCENT_REQUIRED:
            logging.info(f"Arbitrage oportunity: buy:{buy['efPrice']}   sell:{sell['efPrice']}")
            playsound('beep.wav')
            
            #Execute orders
            if float(last_balance['BRL']) < float(BRL_AMOUNT_TRADE):
                executed_sell = web_robot.confirm_offer(sell['offerId'])
                executed_buy = web_robot.confirm_offer(buy['offerId'])
            else:
                executed_buy = web_robot.confirm_offer(buy['offerId'])
                executed_sell = web_robot.confirm_offer(sell['offerId'])

            last_balance = web_robot.api.get_balance()
            logging.info(f"New Balance is: {last_balance}")

            break
            

        end_time = dt.now()
        seconds_elapsed = (end_time - start_time).total_seconds()
        logging.debug(f"Cycle took {seconds_elapsed} seconds")
        cycle_count +=1

        updateTick(cycle_count)
        waitForNextCycle(calculated_percent)
    except Exception as e:
        logging.error(e)


# %%
driver.quit()



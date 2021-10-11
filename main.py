import time
from datetime import datetime as dt
from biscoint_api_python import Biscoint
from playsound import playsound
from utils import percent, amountToBase, showCycle
from configs import logging
from configs import API_KEY, API_SECRET, MIN_PERCENT_REQUIRED, BRL_AMOUNT_TRADE, UPDATE_TICK_RATE
from classes.Robots import BiscointRobot
import argparse
parser = argparse.ArgumentParser(description='Process some integers.')
parser.add_argument('--base','-b', default='BTC',  type=str, choices=['BTC','ETH'], help='crypto to trade')

base =  parser.parse_args().base

# Initial configs
bsc = Biscoint(API_KEY, API_SECRET)
robot = BiscointRobot(bsc)

# Return initial balance from Biscoint
initial_balance = last_balance = bsc.get_balance()
# Calculate the rate limit of request to Biscoint API
endpoints_meta = bsc.get_meta()
rate_limit_offer = endpoints_meta['endpoints']['offer']['post']['rateLimit']
sleep_time_offers = ((rate_limit_offer["windowMs"] / rate_limit_offer["maxRequests"]) / 1000) * 1.5
# Convert the BRL amount of trading to BTC
ticker = bsc.get_ticker(base=base)

amount_to_trade = amountToBase(BRL_AMOUNT_TRADE, ticker['askQuoteAmountRef'], ticker['bidBaseAmountRef'])

percent_record = -1  # Will refresh every time when a new positive spread is achived

logging.info(f"Initial balance: {initial_balance}")
# Arbitrage Cycle
cycle_count = 1


def updateTick(cycle_count):
    global ticker
    global amount_to_trade
    if cycle_count % UPDATE_TICK_RATE == 0:
        try:
            ticker = bsc.get_ticker()
            amount_to_trade = amountToBase( BRL_AMOUNT_TRADE, ticker['askQuoteAmountRef'], ticker['bidBaseAmountRef'])
        except Exception as e:
            logging.error(f"Error on updating tick {e}")

# if spread is high, sleep, else speed up checks


def waitForNextCycle(calculated_percent):
    if calculated_percent < -0.1:
        time.sleep(sleep_time_offers)
    else:
        time.sleep(1)


while True:
    try:
        start_time = dt.now()
        # Get buy and sell offers of this cycle
        buy = robot.get_offer(op='buy', base=base, amount=str(amount_to_trade), is_quote=False)
        sell = robot.get_offer(op='sell',base=base, amount=str(amount_to_trade), is_quote=False)
        # Calculate if arbitrage is possible
        calculated_percent = percent(buy['efPrice'], sell['efPrice'])

        showCycle(cycle_count, calculated_percent)

        if calculated_percent > percent_record:
            logging.info(f"Percent Record Reached!! : {calculated_percent} at {dt.now()}")
            percent_record = calculated_percent
        # If Arbitrage is possible, confirm offers
        if calculated_percent >= MIN_PERCENT_REQUIRED:
            logging.info(f"Arbitrage oportunity: buy:{buy['efPrice']}   sell:{sell['efPrice']}")
            playsound('beep.wav')

            # Execute orders
            if float(last_balance['BRL']) < float(55):
                executed_sell = robot.confirm_offer(sell['offerId'])
                executed_buy = robot.confirm_offer(buy['offerId'])
            else:
                executed_buy = robot.confirm_offer(buy['offerId'])
                executed_sell = robot.confirm_offer(sell['offerId'])

            last_balance = bsc.get_balance()
            logging.info(f"New Balance is: {last_balance}")

        end_time = dt.now()
        seconds_elapsed = (end_time - start_time).total_seconds()
        logging.debug(f"Cycle took {seconds_elapsed} seconds")
        cycle_count += 1

        updateTick(cycle_count)
        waitForNextCycle(calculated_percent)
    except Exception as e:
        logging.error(e)

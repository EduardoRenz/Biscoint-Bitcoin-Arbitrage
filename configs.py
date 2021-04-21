from dotenv import load_dotenv
import os
import logging
load_dotenv()

#Log config
logging.basicConfig(level=logging.INFO, filename="log.log", filemode="a+",format="%(asctime)-15s %(levelname)-8s %(message)s")
logging.getLogger().addHandler(logging.StreamHandler()) # Habilita para printar os logs na tela

# Constants
BASE_URL="https://api.biscoint.io/v1"
BRL_AMOUNT_TRADE = 55 # Amount of BRL to trade  in each transaction
MIN_PERCENT_REQUIRED = 0.1 # Minimal percentage of spread to do trade
UPDATE_TICK_RATE = 30 # Update information of ticker each n times
API_KEY = os.getenv('API_KEY') 
API_SECRET= os.getenv('API_SECRET') 
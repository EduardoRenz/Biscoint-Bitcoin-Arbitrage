from dotenv import load_dotenv
import os
load_dotenv()

# Constants
BASE_URL="https://api.biscoint.io/v1"
AMOUNT = '0.00001'
MIN_PERCENT_REQUIRED = 0.2
API_KEY = os.getenv('API_KEY') 
API_SECRET= os.getenv('API_SECRET') 
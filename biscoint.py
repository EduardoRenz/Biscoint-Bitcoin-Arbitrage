
import requests
import utils
from configs import API_KEY,BASE_URL

def get_rate_limit():
    response = requests.get(f'{BASE_URL}/meta').json()
    return response['data']['endpoints']['offer']['post']['rateLimit']

def get_balance():
    nonce = utils.nonce()
    signature = utils.sign('balance',nonce)
    headers = {
        'Content-Type': 'application/json', 
        'BSCNT-NONCE': str(nonce),
        'BSCNT-APIKEY':API_KEY,
        'BSCNT-SIGN': signature
    }
    response = requests.post(f'{BASE_URL}/balance',headers=headers).json()
    return response

import requests
import utils
import json
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

def get_offer(op:str,amount:str,isQuote:bool,increment_nonce:int=0):
    nonce = utils.nonce() + increment_nonce
    body = {
       'op':op,
       'amount':amount,
       'isQuote':isQuote
    }
    signature = utils.sign('offer',nonce,json.dumps(body))
    headers = {
        'Content-Type': 'application/json', 
        'BSCNT-NONCE': str(nonce),
        'BSCNT-APIKEY':API_KEY,
        'BSCNT-SIGN': signature
    }

    response = requests.post(f'{BASE_URL}/offer',headers=headers,json=body).json()
    if 'data' not in response:
        print(response)
        raise response
    return response['data']

def confirm_offer(offerId:str):
    nonce = utils.nonce()
    body = {
       'offerId':offerId,
    }
    signature = utils.sign('offer/confirm',nonce,json.dumps(body))
    headers = {
        'Content-Type': 'application/json', 
        'BSCNT-NONCE': str(nonce),
        'BSCNT-APIKEY':API_KEY,
        'BSCNT-SIGN': signature
    }

    response = requests.post(f'{BASE_URL}/offer/confirm',headers=headers,json=body).json()
    return response

import requests
import utils
import json
from configs import API_KEY,BASE_URL

def get_rate_limit():
    response = requests.get(f'{BASE_URL}/meta').json()
    return response['data']['endpoints']['offer']['post']['rateLimit']

def get_ticker():
    response = requests.get(f'{BASE_URL}/ticker?base=BTC&quote=BRL').json()
    return response

def get_balance():
    headers = utils.headers('balance')
    response = requests.post(f'{BASE_URL}/balance', headers=headers).json()
    return response

def get_offer(op:str,amount:str,isQuote:bool):
    body = { 'op':op, 'amount':amount, 'isQuote':isQuote }
    headers = utils.headers('offer', json.dumps(body))
    response = requests.post(f'{BASE_URL}/offer', headers=headers, json=body).json()

    if  response == None or 'data' not in response:
        raise Exception("Erro ao buscar oferta",response)
    return response['data']

def confirm_offer(offerId:str):
    body = { 'offerId':offerId }
    headers = utils.headers('offer/confirm', json.dumps(body))
    response = requests.post(f'{BASE_URL}/offer/confirm',headers=headers,json=body).json()
    return response
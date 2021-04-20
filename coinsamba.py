import requests
COINSAMBA_BASE_URL="https://api.coinsamba.com/v0"
def get_offers_coinsamba(op:str,amount:str):
    return requests.get(f'{COINSAMBA_BASE_URL}/bestPrice?refference=quote&side={op}&amount={amount}&base=BTC&quote=BRL').json()

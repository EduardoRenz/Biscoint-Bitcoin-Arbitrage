# Util functions
import hmac
import hashlib
import base64
import time
from configs import API_KEY,API_SECRET
incrementer = 0

def sign(endpoint:str,nonce:int,data:str=''):
        strToBeSigned = ('v1/%s%d%s' % (endpoint, nonce, data)).encode('utf-8')
        hashBuffer = base64.b64encode(strToBeSigned)
        sign_data = hmac.new(
            API_SECRET.encode(),
            hashBuffer,
            hashlib.sha384
        ).hexdigest()
        return sign_data


# Generate a headers
def headers(endpoint:str,data:str=''):
    nonce_now = nonce()
    return {
        "Content-Type": "application/json",
        "BSCNT-NONCE": str(nonce_now),
        "BSCNT-APIKEY": API_KEY,
        "BSCNT-SIGN": sign(endpoint,nonce_now,data),
    }


nonce = lambda  : int(time.time() * 1000000) # Generate a nonce
percent = lambda   value1, value2  :  round((float(value2) / float(value1) - 1) * 100,3) # Calculate percent by numbers
can_buy = lambda brl,min_brl=10 : float(brl) >= float(min_brl) # verify if you have enough money
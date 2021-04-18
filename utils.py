# Util functions
def sign(endpoint,nonce,data=''):
  param_string = f"v1/{endpoint}{nonce}{data}"
  encoded_param_string = param_string.encode('utf-8')
  base64_param_string = base64.b64encode(encoded_param_string)
  signature = hmac.new(API_SECRET.encode(), base64_param_string, hashlib.sha384).hexdigest()
  return signature

# Generate a headers
def headers(endpoint,data={}):
    nonce_now = nonce()
    return {
        "Content-Type": "application/json",
        "BSCNT-NONCE": nonce_now,
        "BSCNT-APIKEY": API_KEY,
        "BSCNT-SIGN": sign(endpoint,nonce_now,data),
    }


# Generate a nonce
nonce = lambda  : str(int(dt.now().timestamp() * 1000))
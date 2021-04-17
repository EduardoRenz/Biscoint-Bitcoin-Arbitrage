def sign(endpoint,nonce,data):
  total_params = f"v1/{endpoint}{nonce}{data}"
  total_params = total_params.encode('utf_8')
  signature = hmac.new(API_SECRET, total_params, hashlib.sha384).hexdigest()
  print("signature = {0}".format(signature))
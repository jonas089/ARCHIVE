import hashlib, pickle, base64, binascii
from Crypto.PublicKey import RSA
from Crypto.Signature import pkcs1_15 # / RSA algorithm to sign with priv(1) & verify with pub(1)
from Crypto.Hash import SHA384

def Validate(data):
    signature = binascii.unhexlify(data['signature'])
    message = data['x'] + data['y'] + data['timestamp']
    sigf = SHA384.new(message.encode('utf-8'))
    key = RSA.import_key(data['public_Key'])
    try:
        pkcs1_15.new(key).verify(sigf, signature)
        return True
    except (ValueError, TypeError):
        print("[V] Signature is Invalid.")
        return False

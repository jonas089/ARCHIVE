from Crypto.PublicKey import RSA
from Crypto.Signature import pkcs1_15
from Crypto.Hash import SHA384
import hashlib, time, os, pickle, requests, base64
import Account
import binascii


user = '1650799809'

def UpdatePosition(user, x, y):
    user_account = Account.Keys(user)
    timestamp = time.time()
    message = str(x) + str(y) + str(timestamp)
    print(str(x))
    # Message Hash
    sha = hashlib.sha384()
    message_hash = sha.update(message.encode('utf-8'))
    message_hash_hex = sha.hexdigest()

    # Message Signature
    sigf = SHA384.new(message.encode('utf-8'))
    user_account.Import_Private_Key()
    signature = pkcs1_15.new(RSA.import_key(user_account.private_key)).sign(sigf)
    print(signature)

    #print(signature)
    #print(user_account.public_key)
    data = {
    'signature' : binascii.hexlify(signature).decode('ascii'),
    'hash' : str(message_hash_hex),
    'public_Key' : user_account.public_key,
    'timestamp':str(timestamp),
    'x':str(x),
    'y':str(y)
    }
    r = requests.post('http://127.0.0.1:80/update', json=data)
def getPosition(user):
    r = requests.get('http://127.0.0.1:80/getPosition')
    return r.text
UpdatePosition(user, int(input('Enter x: ')),int(input('Enter y: ')))
print(getPosition(user))

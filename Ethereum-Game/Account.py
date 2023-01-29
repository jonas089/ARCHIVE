from Crypto.PublicKey import RSA
from Crypto.Signature import PKCS1_v1_5
from Crypto.Hash import SHA384
import hashlib, time, os, pickle

class Generator():
    def __init__(self, timestamp):
        self.key = RSA.generate(2048)
        self.timestamp = timestamp
    def SaveKey(self, key_type):
        if key_type == 'private':
            os.mkdir(str(self.timestamp))
            open(str(self.timestamp)+'/'+'private.pem', 'x')
            open(str(self.timestamp)+'/'+'public.pem', 'x')
            with open(str(self.timestamp)+'/'+'private.pem', 'wb') as private_key_file:
                private_key_file.write(self.key.exportKey('PEM'))
                private_key_file.close()
            return True

        elif key_type == 'public':
            if not os.path.exists(str(self.timestamp)):
                return False

            with open(str(self.timestamp)+'/'+'public.pem', 'wb') as public_key_file:
                public_key_file.write(self.key.publickey().exportKey('PEM'))
                public_key_file.close()
            return True

        else:
            return False

class Keys():
    def __init__(self, user): # as for now, user is timestamp
        with open(user+'/'+'private.pem', 'r') as private_key_file:
            self.private_key = private_key_file.read()
        private_key_file.close()
        with open(user+'/'+'public.pem', 'r') as public_key_file:
            self.public_key = public_key_file.read()
        public_key_file.close()
        self.user = user
        self.import_private_key = None
    def Import_Private_Key(self):
        with open(self.user+'/'+'private.pem', 'r') as private_key_file:
            self.import_private_key = RSA.importKey(private_key_file.read())
        return True

#Generate new Keypair / User:
#timestamp = int(time.time())
#print(timestamp)
#User_Keypair = Generator(timestamp)
#User_Keypair.SaveKey('private')
#User_Keypair.SaveKey('public')

#my_keys = Keys(str(timestamp))
#my_keys.Import_Private_Key()

#print(my_keys.import_private_key)

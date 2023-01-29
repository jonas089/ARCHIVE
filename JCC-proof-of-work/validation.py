import hashlib
from Crypto.PublicKey import RSA
#from Crypto.Cipher import PKCS1_OAEP   # / RSA algorithm to encrypt with pub(2) & decrypt with priv(2)
from Crypto.Signature import PKCS1_v1_5 # / RSA algorithm to sign with priv(1) & verify with pub(1)
from Crypto.Hash import SHA256 
from blockchain import *
# This defines which keys a Block dictionary may contain
required_variables = {
	'index' : int,
	'prev_hash' : str,
	'timestamp' : str,
	'amount' : float,
	'nnonce' : int,
	'address' : str,
	'pub_key' : bytes,
	'new_hash' : str,
	'clear' : bytes,
	'sign' : str,
	'signature' : bytes
}

class Validations(object):
	def __init__(self, dictionary):
		for i, value in dictionary.items():
			if i in required_variables:
				setattr(self, i, required_variables[i](value))
			else:
				setattr(self, i, value)
		Validations.block_is_valid(self)
	def validation_string(self):
		validation_string_contains = str(self.index) + self.prev_hash + self.timestamp + str(self.amount) + str(self.nnonce) + self.address
		return validation_string_contains
	def block_is_valid(self):
		CAmount_halving = 10
		CAmount_Subsidy = 1
		Halving_Height = int(self.index / 10)
		if Halving_Height >= 1:
			for i in range(0, Halving_Height):
				CAmount_Subsidy = CAmount_Subsidy / 2
		if self.amount != CAmount_Subsidy:
			print("Amount Error")
		sha = hashlib.sha256()
		validation_to_hash = Validations.validation_string(self)
		valid_string = sha.update(validation_to_hash.encode('utf-8'))
		compare_hash = sha.hexdigest()
		if compare_hash != self.new_hash:
			print("Hash Error")
		public_key = RSA.import_key(self.pub_key)
		sign = SHA256.new()
		sign.update(self.clear)
		verifier = PKCS1_v1_5.new(public_key)
		verified = verifier.verify(sign, self.signature)
		assert verified, '[BOO] Block is invalid or could not be validated !'
		chaindata = Blockchain.Load_Chain()
		correct_index = Blockchain.Fetch_New_Index(chaindata)
		if self.index != correct_index:
			print("Index Error")
		block_dictionary =  {
			'index' : self.index,
			'prev_hash' : self.prev_hash,
			'timestamp' : self.timestamp,
			'amount' : self.amount,
			'nnonce' : self.nnonce,
			'address' : self.address,
			'pub_key' : self.pub_key,
			'new_hash' : self.new_hash,
			'clear' : self.clear,
			'sign' : self.sign,
			'signature' : self.signature
		}
		Blockchain.Add_New_Block(block_dictionary)

class Validation_Genesis(object):
	def __init__(self, dictionary):
		for i, value in dictionary.items():
			if i in required_variables:
				setattr(self, i, required_variables[i](value))
			else:
				setattr(self, i, value)
		return Validation_Genesis.block_is_valid(self)
	def validation_string(self):
		validation_string_contains = str(self.index) + self.timestamp + str(self.amount) + str(self.nnonce) + self.address
		return validation_string_contains
	def block_is_valid(self):
		sha = hashlib.sha256()
		validation_to_hash = Validation_Genesis.validation_string(self)
		valid_string = sha.update(validation_to_hash.encode('utf-8'))
		compare_hash = sha.hexdigest()
		if compare_hash != self.new_hash:
			print("Hash Error")
		public_key = RSA.import_key(self.pub_key)

		sign = SHA256.new()
		sign.update(self.clear)
		verifier = PKCS1_v1_5.new(public_key)
		verified = verifier.verify(sign, self.signature)
		assert verified, '[BOO] Block is invalid or could not be validated !'
		#correct_index = Blockchain.Fetch_New_Index()
		if self.index != 0:
			print("Index Error")
		block_dictionary =  {
			'index' : self.index,
			'prev_hash' : self.prev_hash,
			'timestamp' : self.timestamp,
			'amount' : self.amount,
			'nnonce' : self.nnonce,
			'address' : self.address,
			'pub_key' : self.pub_key,
			'new_hash' : self.new_hash,
			'clear' : self.clear,
			'sign' : self.sign,
			'signature' : self.signature
		}
		Blockchain.Add_Genesis_Block(block_dictionary)
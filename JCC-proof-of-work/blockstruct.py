import hashlib
from validation import *
from Crypto.PublicKey import RSA

#from Crypto.Cipher import PKCS1_OAEP   # / RSA algorithm to encrypt with pub(2) & decrypt with priv(2)
from Crypto.Signature import PKCS1_v1_5 # / RSA algorithm to sign with priv(1) & verify with pub(1)
from Crypto.Hash import SHA256 


# This defines which keys a Block dictionary may contain
block_variables = {
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

class Generate_Genesis_Block(object):
	def __init__(self, dictionary):
		for i, value in dictionary.items():
			if i in block_variables:
				setattr(self, i, block_variables[i](value))
			else:
				setattr(self, i, value)
		return Generate_Genesis_Block.Block_Hash(self)
	def header_string(self):
		header_string_contains = str(self.index) + self.timestamp + str(self.amount) + str(self.nnonce) + self.address
		return header_string_contains
	def Block_Hash(self):
		while True:

			# Generate random hashes by adjusting the nnonce
			sha = hashlib.sha256()
			new_header = self.header_string()
			header_encoded = sha.update(new_header.encode('utf-8'))
			self.new_hash = sha.hexdigest()

			# Validate block hash by leading Zeros
			if self.new_hash[:5] != '0' * 5:
				self.nnonce += 1
			else:
				hash_encoded = self.new_hash.encode('utf-8')
				with open('keystore/private_key.pem' , 'r') as private_key_file:
					private_key = RSA.import_key(private_key_file.read())
				signing = SHA256.new()
				signing.update(hash_encoded)
				self.clear = hash_encoded
				self.sign = signing
				cipher = PKCS1_v1_5.new(private_key)
				ciphercontent = cipher.sign(signing)
				self.signature = ciphercontent

				print(self.new_hash + ' [VALID]')
				Validation_Genesis(self.Block_Dictionary())
				break

	# Initialize Block Dictionary
	def Block_Dictionary(self):
		self.Block_data = {
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
		return self.Block_data

# Block class requires a dictionary containing DATA to be passed when called as function
class Block(object):
	def __init__(self, dictionary):
		for i, value in dictionary.items():
			if i in block_variables:
				setattr(self, i, block_variables[i](value))
			else:
				setattr(self, i, value)
		return Block.Block_Hash(self)
	def header_string(self):
		header_string_contains = str(self.index) + self.prev_hash + self.timestamp + str(self.amount) + str(self.nnonce) + self.address
		return header_string_contains
	def Block_Hash(self):
		while True:

			# Generate random hashes by adjusting the nnonce
			sha = hashlib.sha256()
			new_header = self.header_string()
			header_encoded = sha.update(new_header.encode('utf-8'))
			self.new_hash = sha.hexdigest()

			# Validate block hash by leading Zeros
			if self.new_hash[:5] != '0' * 5:
				self.nnonce += 1
			else:
				hash_encoded = self.new_hash.encode('utf-8')
				with open('keystore/private_key.pem' , 'r') as private_key_file:
					private_key = RSA.import_key(private_key_file.read())
				signing = SHA256.new()
				signing.update(hash_encoded)
				self.clear = hash_encoded
				self.sign = signing
				cipher = PKCS1_v1_5.new(private_key)
				ciphercontent = cipher.sign(signing)
				self.signature = ciphercontent

				print(self.new_hash + ' [VALID]')
				Validations(self.Block_Dictionary())
				break

	# Initialize Block Dictionary
	def Block_Dictionary(self):
		self.Block_data = {
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
		return self.Block_data
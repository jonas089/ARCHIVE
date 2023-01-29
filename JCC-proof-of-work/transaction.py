import hashlib
from Crypto.PublicKey import RSA
from Crypto.Signature import PKCS1_v1_5 
from Crypto.Hash import SHA256 
import os
import pickle

transaction_variables = {
	'height' : int,
	'timestamp' : str,
	'sender' : str,
	'recipient' : str,
	'amount' : float,
	'pub_key' : bytes,
	'hash' : str,
	'clear' : bytes,
	'sign' : str,
	'signature' : bytes,
}
class Transaction(object):
	def __init__(self, dictionary):
		for i, value in dictionary.items():
			if i in transaction_variables:
				setattr(self, i, transaction_variables[i](value))
			else:
				setattr(self, i, value)
		return Transaction.Validate_Tx(self)
	def Validate_Tx(self):
		sha = hashlib.sha256()
		hash_data_str = str(self.height) + self.timestamp + self.sender + self.recipient + str(self.amount)
		hash_data_encoded = hash_data_str.encode('utf-8')
		hashed_data = sha.update(hash_data_encoded)
		hashed_data_hex = sha.hexdigest()
		print(hashed_data_hex)
		print(self.hash)
		if hashed_data_hex != self.hash:
			print('[BOO] Transaction hash could not be reconstructed !')
		public_key = RSA.import_key(self.pub_key)
		sign = SHA256.new()
		sign.update(self.clear)
		verifier = PKCS1_v1_5.new(public_key)
		verified = verifier.verify(sign, self.signature)
		assert verified, '[BOO] Transaction is invalid or could not be validated !'
		Transaction.Tx_Dictionary(self)
		
	def Tx_Dictionary(self):
		self.Tx_data = {
		'height' : self.height,
		'timestamp' : self.timestamp,
		'sender' : self.sender,
		'recipient' : self.recipient,
		'amount' : self.amount,
		'pub_key' : self.pub_key,
		'hash' : self.hash,
		'clear' : self.clear,
		'sign' : self.sign,
		'signature' : self.signature
		}
		print('[YAY] Transaction is valid !')
		Transaction.Add_Transaction_To_TxPool(self.Tx_data)
	def Add_Transaction_To_TxPool(txdata):
		try:
			open('wallet.dat', 'x')
		except Exception as exists:
			pass
		try:
			with open('wallet.dat', 'rb') as backup:
				backup_data = pickle.load(backup)
				new_index = len(backup_data)
				backup_data.append(new_index)
		except Exception as not_exists:
			backup_data = []
			backup_data.append(0)
			new_index = 0
		backup_data[new_index] = txdata
		with open('wallet.dat', 'wb') as wallet_data:
			pickle.dump(backup_data, wallet_data)

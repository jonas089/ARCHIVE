from transaction import *
import time
import hashlib
from Crypto.PublicKey import RSA
import pickle

#from Crypto.Cipher import PKCS1_OAEP   # / RSA algorithm to encrypt with pub(2) & decrypt with priv(2)
from Crypto.Signature import PKCS1_v1_5 # / RSA algorithm to sign with priv(1) & verify with pub(1)
from Crypto.Hash import SHA256 

class Wallet:
	def New_Transaction():
		with open('keystore/private_key.pem', 'r') as private_key_file:
			private_key = RSA.import_key(private_key_file.read())
		with open('keystore/public_key.pem' , 'r') as public_key_file:
			public_key = RSA.import_key(public_key_file.read())
		tx_data = {}
		tx_data['height'] = 0
		tx_data['timestamp'] = str(time.time())
		tx_data['sender'] = '1'
		tx_data['recipient'] = '0'
		tx_data['amount'] = 10.0
		tx_data['pub_key'] = public_key.export_key('PEM')
		sha = hashlib.sha256()
		tx_hash = str(tx_data['height']) + tx_data['timestamp'] + tx_data['sender'] + tx_data['recipient'] + str(tx_data['amount'])
		# warning : due to hash validation, amount always has to be of type float !
		tx_hash_encoded = tx_hash.encode('utf-8')
		tx_hashing = sha.update(tx_hash_encoded)
		tx_hashed = sha.hexdigest()
		tx_data['hash'] = tx_hashed
		sign = SHA256.new()
		sign.update(tx_hash_encoded)
		tx_data['clear'] = tx_hash_encoded
		tx_data['sign'] = sign
		cipher = PKCS1_v1_5.new(private_key)
		ciphertext = cipher.sign(sign)
		tx_data['signature'] = ciphertext
		if Wallet.Read_Local_Wallet(tx_data['sender']) >= tx_data['amount']:
			Transaction(tx_data)
		else:
			print("Balance too Low !")
	def Read_Local_Wallet(owner):
		try:
			balance = 0.0
			with open('wallet.dat', 'rb') as walletdata:
				wallet_dat = pickle.load(walletdata)
				for i in range(0, len(wallet_dat)):
					if wallet_dat[i]['recipient'] == owner:
						balance += wallet_dat[i]['amount']
					if wallet_dat[i]['sender'] == owner:
						balance -= wallet_dat[i]['amount']
			print('Tx: ' + str(balance))
		except Exception as no_tx:
			print("No Transactions")
		try:
			with open('chaindata/block.dat', 'rb') as BlockData:
				block_dat = pickle.load(BlockData)
				for i in range(0, len(block_dat)):
					if block_dat[i]['address'] == owner:
						balance += block_dat[i]['amount']
			print('Over All: ' + str(balance))
		except Exception as no_blocks:
			print("No Blocks")
		return balance
Address = '1'
choice = input("T for new Transaction with Default values, B for Balance with Default Address... ")
if choice == "T":
	Wallet.New_Transaction()
elif choice == "B":
	Wallet.Read_Local_Wallet(Address)
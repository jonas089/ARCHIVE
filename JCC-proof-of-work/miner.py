from Crypto.PublicKey import RSA
import hashlib
from Crypto.Hash import SHA256 
import time
from blockstruct import *
from blockchain import *
class Miner:
	def _Rounds():
		for i in range(0, 500):
			Miner.Mine_From_Previous()
	def Mine_From_Previous():
		chain = Blockchain.Load_Chain()
		index = Blockchain.Fetch_New_Index(chain)
		prev_hash = Blockchain.Fetch_Prev_Hash(chain)
		timestamp = str(time.time())
		nnonce = 0 # default
		amount = 1 # default
		# Twice / CAmount params are declared here (generation) and validation.py 
		CAmount_halving = 10
		CAmount_Subsidy = 1
		Halving_Height = int(index / 10)
		if Halving_Height >= 1:
			for i in range(0, Halving_Height):
				CAmount_Subsidy = CAmount_Subsidy / 2
		amount = 1
		address = '1'
		new_hash = None
		clear = b'none'
		sign = None
		signature = b'none'
		with open('keystore/public_key.pem' , 'r') as public_key_file:
			public_key = RSA.import_key(public_key_file.read())
		pub_key_export = public_key.export_key('PEM')

		block_data = {
			'index' : index,
			'prev_hash' : prev_hash,
			'timestamp' : timestamp,
			'amount' : amount,
			'nnonce' : nnonce,
			'address' : address,
			'pub_key' : pub_key_export,
			'new_hash' : new_hash,
			'clear' : clear,
			'sign' : sign,
			'signature' : signature
		}
		Block(block_data)
	def Generate_Genesis():
		index = 0
		prev_hash = None
		timestamp = str(time.time())
		nnonce = 0 # default
		amount = 1 # default
		address = '1'
		new_hash = None
		clear = b'none'
		sign = None
		signature = b'none'
		with open('keystore/public_key.pem' , 'r') as public_key_file:
			public_key = RSA.import_key(public_key_file.read())
		pub_key_export = public_key.export_key('PEM')
		
		block_data = {
			'index' : index,
			'prev_hash' : prev_hash,
			'timestamp' : timestamp,
			'amount' : amount,
			'nnonce' : nnonce,
			'address' : address,
			'pub_key' : pub_key_export,
			'new_hash' : new_hash,
			'clear' : clear,
			'sign' : sign,
			'signature' : signature
		}
		Generate_Genesis_Block(block_data)
while True:
	choice = input("G for Genesis, B for Block, E for Exit... ")
	if choice == "G":
		Miner.Generate_Genesis()
	elif choice == "B":
		Miner.Mine_From_Previous()
	elif choice == "R":
		Miner._Rounds()
	elif choice == "E":
		break
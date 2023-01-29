import os
from Crypto.PublicKey import RSA

class Keys:
	# Generates Keypair And Saves Both PRIVATE and PUBLIC KEY to your LOCAL Drive
	def Generate_Keypair():
		key = RSA.generate(2048)
		try:
			os.mkdir('keystore/')
		except Exception as exists:
			pass
		try:
			open('keystore/private_key.pem', 'x')
		except Exception as exists:
			pass
		try:
			open('keystore/public_key.pem', 'x')
		except Exception as exists:
			pass

		with open('keystore/private_key.pem', 'wb') as private_key_file:
			private_key_file.write(key.export_key('PEM'))
			private_key_file.close()
		with open('keystore/public_key.pem', 'wb') as public_key_file:
			public_key_file.write(key.publickey().export_key('PEM'))
			public_key_file.close()
Keys.Generate_Keypair()
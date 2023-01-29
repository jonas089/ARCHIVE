from flask import Flask, jsonify, request
import requests
import pickle
import json
import utils
from validation import *
from config import *

node = Flask(__name__)

@node.route('blockchain.json', methods=['GET'])
def return_blockchain():
	try:
		with open('chaindata/block.dat', 'rb') as block_data:
			blockchain_list = pickle.load(block_data)
	except Exception as empty:
		blockchain_list = []
	return blockchain_list
@node.route('txpool.json', methods=['GET'])
def return_txpool():
	try:
		with open('wallet.dat', 'rb') as txdata_file:
			txdata = pickle.load(txdata_file)
	except Exception as empty:
		txdata = []
	return txdata
@node.route('/block', methods=['POST'])
def receive_work():
	possible_block = request.get_json()
	#return Validations(possible_block)
	print(str(Validations(possible_block)))

if __name__ == '__main__':
  parser = argparse.ArgumentParser(description='JCC Node')
  parser.add_argument('--port', '-p', default='5000',
                    help='port')
  parser.add_argument('--mine', '-m', dest='mine', action='store_true')
  args = parser.parse_args()
  node.run(host='127.0.0.1', port=args.port)

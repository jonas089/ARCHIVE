from blockstruct import *
import pickle
import os

class Blockchain(object):
	def Load_Chain():
		try:
			os.mkdir('chaindata/')
		except Exception as exists:
			pass
		try:
			open('chaindata/block.dat', 'x')
		except Exception as exists:
			pass
		with open('chaindata/block.dat', 'rb') as chaindata:
			Local_Chain = pickle.load(chaindata)
		return Local_Chain
	def Fetch_New_Index(Local_Chain):
		return len(Local_Chain)
	def Fetch_Prev_Hash(Local_Chain):
		return Local_Chain[len(Local_Chain) - 1]['new_hash']
	def Add_New_Block(Block_Data):
		with open('chaindata/block.dat', 'rb') as backup_file:
			backup = pickle.load(backup_file)
		with open('chaindata/block.dat', 'wb') as blockchain_write:
			backup.append(Block_Data['index'])
			backup[Block_Data['index']] = Block_Data
			pickle.dump(backup, blockchain_write)
		return True
	def Add_Genesis_Block(Block_Data):
		try:
			os.mkdir('chaindata/')
		except Exception as exists:
			pass
		try:
			open('chaindata/block.dat', 'x')
		except Exception as exists:
			pass
		with open('chaindata/block.dat', 'wb') as blockchain_write:
			Blockchain_total = []
			Blockchain_total.append(0)
			Blockchain_total[0] = Block_Data
			pickle.dump(Blockchain_total, blockchain_write)
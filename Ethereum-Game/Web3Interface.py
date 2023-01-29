#0x0af9EFCc8b9b6c1867289dC851707fB36eC88541

# DEV PRIVATE KEY
#0157f0aec02643f9eab46c376db8f2fecae1801fb82c6c642fa899e0759a38f2
# DEV ADDRESS
#0x83035aEa6Ce4AECbbC7106D62853386Ba36c65c9
''' ABI '''

'''
[
	{
		"inputs": [],
		"name": "get_x",
		"outputs": [
			{
				"internalType": "string",
				"name": "",
				"type": "string"
			}
		],
		"stateMutability": "nonpayable",
		"type": "function"
	},
	{
		"inputs": [],
		"name": "get_y",
		"outputs": [
			{
				"internalType": "string",
				"name": "",
				"type": "string"
			}
		],
		"stateMutability": "nonpayable",
		"type": "function"
	},
	{
		"inputs": [
			{
				"internalType": "string",
				"name": "_x",
				"type": "string"
			}
		],
		"name": "set_x",
		"outputs": [],
		"stateMutability": "nonpayable",
		"type": "function"
	},
	{
		"inputs": [
			{
				"internalType": "string",
				"name": "_y",
				"type": "string"
			}
		],
		"name": "set_y",
		"outputs": [],
		"stateMutability": "nonpayable",
		"type": "function"
	}
]
'''
from web3 import Web3

def GanacheContract(action, value):
    w3 = Web3(Web3.HTTPProvider('http://127.0.0.1:7545'))
    print('CONNECTED: ' + str(w3.isConnected()))

    game_Contract = w3.eth.contract(address='0x0dCc9Ef29b86E02Eaf10Fc1dcDC5b27FdF4deCfB',
    abi=[
    	{
    		"inputs": [],
    		"name": "get_x",
    		"outputs": [
    			{
    				"internalType": "string",
    				"name": "",
    				"type": "string"
    			}
    		],
    		"stateMutability": "nonpayable",
    		"type": "function"
    	},
    	{
    		"inputs": [],
    		"name": "get_y",
    		"outputs": [
    			{
    				"internalType": "string",
    				"name": "",
    				"type": "string"
    			}
    		],
    		"stateMutability": "nonpayable",
    		"type": "function"
    	},
    	{
    		"inputs": [
    			{
    				"internalType": "string",
    				"name": "_x",
    				"type": "string"
    			}
    		],
    		"name": "set_x",
    		"outputs": [],
    		"stateMutability": "nonpayable",
    		"type": "function"
    	},
    	{
    		"inputs": [
    			{
    				"internalType": "string",
    				"name": "_y",
    				"type": "string"
    			}
    		],
    		"name": "set_y",
    		"outputs": [],
    		"stateMutability": "nonpayable",
    		"type": "function"
    	}
    ])
    if action == 'get_x':
        return game_Contract.functions.get_x().call()
    elif action == 'get_y':
        return game_Contract.functions.get_y().call()
    elif action == 'set_x':
        return game_Contract.functions.set_x(str(value)).transact({'from': w3.eth.accounts[0], 'gas': 100000})
    elif action == 'set_y':
        return game_Contract.functions.set_y(str(value)).transact({'from': w3.eth.accounts[0], 'gas': 100000})
    else:
        return False

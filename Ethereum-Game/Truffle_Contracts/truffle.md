npm init
npm install truffle
./node_modules/.bin/truffle init

./node_modules/.bin/truffle compile
*truffle migrate

specify the build/contracts/CONTRACT.json in readabi.js to read the ABI of a deployed contract
use web3.js to interact with contracts.


------------------------------------------------------

truffle console

// you will see a CLI

//create  a var to store an instance of the contract
truffle(development)> let instance = await StoreValue.deployed()

//set stored value to 42
truffle(development)> instance.set(42)

//get stored value
truffle(development)> instance.get()

-----------------------------------------------------

const fs = require('fs'); // equivalent to python OS
const contract = JSON.parse(fs.readFileSync('./build/contracts/Token.json', 'utf8'));
console.log(JSON.stringify(contract.abi));

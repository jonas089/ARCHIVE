const gameContract = artifacts.require("gameContract");
module.exports = function (deployer) {
	deployer.deploy(gameContract); // 1 Billion Tokens
};

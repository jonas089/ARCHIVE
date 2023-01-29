pragma solidity ^0.7.0;

import './IERC20.sol';
import './SafeMath.sol';
import './Defl8.sol';

contract MintDCrash{
  using SafeMath for uint;

  struct Earning{
    // address claiming the coins
    address claimer;
    uint amount;
    uint last_claimed;
  }

  mapping(address => Earning) public claim;
  uint public claimable_amount;
  uint public availableTokens;
  uint public claim_interval;
  Token public token;

  constructor(
      address tokenAddress,
      uint _claimable_amount,
      uint _claim_interval,
      uint _availableTokens
      )
  {
      token = Token(tokenAddress);

      require(_claimable_amount > 0, 'claimable_amount should be > 0');
      require(
        _availableTokens > 0 && _availableTokens <= token.maxTotalSupply(),
        '_availableTokens should be > 0 and <= maxTotalSupply'
      );

      claimable_amount = _claimable_amount;
      claim_interval = _claim_interval;
      availableTokens = _availableTokens;
  }

  function Claim()
      external
  {
      Earning storage claimer = claim[msg.sender];
      uint claimed_last = claimer.last_claimed;
      require(block.timestamp >= claim[msg.sender].last_claimed + claim_interval, 'you need to wait, before you can claim again.');
      token.mint(address(this), claimable_amount);
      claim[msg.sender] = Earning(
          msg.sender,
          claimed_last + claimable_amount,
          block.timestamp
      );
      // Transfer claimed amount to actual wallet
      Earning storage claims = claim[msg.sender];
      //require(claim.amount > 0, 'nothing claimed!'); // not required when calling inside Claim()
      token.transfer(claims.claimer, claims.amount);
  }

  function canIclaim() public view returns(uint){
    if(claim[msg.sender].last_claimed + claim_interval < block.timestamp){
        return 1;
    }
    else{
        return 0;
    }
  }

  function TotalAmountMinted() public view returns(uint){
      return (token.totalSupply() /(10**18) + token.balanceOf(address(0)) /(10**18));
  }

/*
  function withdrawTokens()
      external
  {
      Earning storage claim = claim[msg.sender];
      require(claim.amount > 0, 'nothing claimed!');
      token.transfer(claim.claimer, Service_Fee_Owner, claim.service_fee);
  }
*/
}

pragma solidity ^0.8.7;

contract GameContract{
    string y;
    string x;
    address admin = msg.sender;
    function get_x() public returns(string memory){
        return x;
    }
    function get_y() public returns(string memory){
        return y;
    }
    function set_x(string memory _x) public{
        require(msg.sender == admin, 'only admin');
        x = _x;
    }
    function set_y(string memory _y) public{
        require(msg.sender == admin, 'only admin');
        y = _y;
    }
}

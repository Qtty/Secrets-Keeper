// SPDX-License-Identifier: GPL-3.

pragma solidity ^0.8.1;

contract Proxy {
    address public contractAddress;
    
    
    constructor(address _contractAddress) {
        contractAddress = _contractAddress;
    }
}
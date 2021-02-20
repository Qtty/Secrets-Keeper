// SPDX-License-Identifier: GPL-3.

pragma solidity ^0.8.1;

contract Keeper {

    address owner;
    uint256[] public labels;
    mapping(uint256 => uint256) public targets;
    
    constructor() {
        owner = msg.sender;
    }

    modifier onlyOwner {
        require(msg.sender == owner, 'Not Owner');
        _;
    }
    
    function addPassword(uint256 _label, uint256 _target) external onlyOwner {
        labels.push(_label);
        targets[_label] = _target;
    }
    
    function getLabelsLength() external onlyOwner view returns(uint256) {
        return labels.length;
    }
    
    function removeLabel(uint256 _index) external onlyOwner {
        assert(_index < labels.length);
        labels[_index] = labels[labels.length - 1];  
        labels.pop();
    }
}
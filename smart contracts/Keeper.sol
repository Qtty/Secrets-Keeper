// SPDX-License-Identifier: GPL-3.

pragma solidity ^0.8.1;

contract Keeper {

    uint256[] public labels;
    mapping(uint256 => uint256) public targets;
    
    function addPassword(uint256 _label, uint256 _target) public {
        labels.push(_label);
        targets[_label] = _target;
    }
    
    function getLabelsLength() public view returns(uint256) {
        return labels.length;
    }
}
// SPDX-License-Identifier: GPL-3.

pragma solidity ^0.8.1;

contract Keeper {

    string[] public labels;
    mapping(string => string) public targets;
    
    function addPassword(string calldata _label, string calldata _target) public {
        require(bytes(_label).length <= 21 && bytes(_label).length >= 1, "Label must be between 1 and 20 characters long");

        labels.push(_label);
        targets[_label] = _target;
    }
    
    function getLabelsLength() public view returns(uint256) {
        return labels.length;
    }
}
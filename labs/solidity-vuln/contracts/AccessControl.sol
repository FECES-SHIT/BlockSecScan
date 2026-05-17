// SPDX-License-Identifier: MIT
pragma solidity ^0.8.0;

contract AccessControlVuln {
    address public owner;

    constructor() {
        owner = msg.sender;
    }

    function setOwner(address newOwner) external {
        owner = newOwner;
    }

    function withdrawAll() external {
        (bool ok, ) = msg.sender.call{value: address(this).balance}("");
        require(ok, "transfer failed");
    }
}

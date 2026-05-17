// SPDX-License-Identifier: MIT
pragma solidity ^0.8.0;

contract TxOriginVuln {
    address public owner;

    constructor() {
        owner = tx.origin;
    }

    function transferOwnership(address newOwner) external {
        require(tx.origin == owner, "not owner");
        owner = newOwner;
    }
}

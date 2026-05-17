// SPDX-License-Identifier: MIT
pragma solidity ^0.8.0;

contract UncheckedCallVuln {
    function forward(address payable target, bytes memory data) external payable {
        target.call{value: msg.value}(data);
    }

    function unsafeSend(address payable to, uint256 amount) external {
        to.send(amount);
    }
}

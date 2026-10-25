// SPDX-License-Identifier: MIT
pragma solidity ^0.8.20;

contract AuditRegistry {
    address public owner;

    struct AuditRecord {
        address targetContract;
        string riskScore;
        string reportHash;
        uint256 timestamp;
    }

    mapping(address => AuditRecord[]) public auditHistory;
    event AuditLogged(address indexed target, string riskScore, uint256 timestamp);

    // Restrict access to the AI Agent only
    modifier onlyOwner() {
        require(msg.sender == owner, "Only the Sentinel AI Agent can log audits");
        _;
    }

    constructor() {
        owner = msg.sender;
    }

    function recordAudit(
        address _targetContract, 
        string memory _riskScore, 
        string memory _reportHash
    ) public onlyOwner {
        AuditRecord memory newRecord = AuditRecord({
            targetContract: _targetContract,
            riskScore: _riskScore,
            reportHash: _reportHash,
            timestamp: block.timestamp
        });

        auditHistory[_targetContract].push(newRecord);
        emit AuditLogged(_targetContract, _riskScore, block.timestamp);
    }

    function getLatestAudit(address _targetContract) public view returns (AuditRecord memory) {
        require(auditHistory[_targetContract].length > 0, "No audit found");
        return auditHistory[_targetContract][auditHistory[_targetContract].length - 1];
    }
}

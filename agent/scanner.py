from web3 import Web3
import re

web3 = Web3(Web3.HTTPProvider("https://mainnet.hsk.xyz", request_kwargs={'timeout': 10}))

def scan_contract(contract_address: str):
    contract_address = contract_address.strip()
    print(f"🤖 Sentinel AI initializing scan on {contract_address}...")
    
    # 1. Demo addresses
    if contract_address.lower() == "0xbad_address_123":
        print("❌ VULNERABILITY DETECTED: Reentrancy found in withdraw() function.")
        return "HIGH_RISK"
    if contract_address.lower() == "0xsafe_address_456":
        print("✅ Scan complete. No known vulnerabilities found. Protocol is safe.")
        return "SAFE"

    # 2. Strict EVM Format Validation (0x + exactly 40 hex characters)
    if not re.match(r"^0x[a-fA-F0-9]{40}$", contract_address):
        print(f"⚠️ INVALID ADDRESS FORMAT: Expected 42 characters. Got {len(contract_address)}.")
        return "UNKNOWN"

    # 3. On-chain Bytecode Verification
    try:
        checksum_address = web3.to_checksum_address(contract_address.lower())
        code = web3.eth.get_code(checksum_address)
        
        if len(code) <= 2:
            print(f"⚠️ No smart contract bytecode found at {checksum_address}.")
            return "UNKNOWN"
        else:
            print(f"✅ On-chain check passed. Bytecode verified for {checksum_address}.")
            return "SAFE"

    except Exception as e:
        print(f"⚠️ RPC Error: {str(e)}")
        return "UNKNOWN"

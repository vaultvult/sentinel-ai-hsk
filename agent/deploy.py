import os
from web3 import Web3
from solcx import compile_standard, install_solc
from dotenv import load_dotenv

# Load private key from .env
load_dotenv()
PRIVATE_KEY = os.getenv("PRIVATE_KEY")

# HSK Testnet RPC
RPC_URL = "https://mainnet.hsk.xyz"
web3 = Web3(Web3.HTTPProvider(RPC_URL))

# 1. Compile the Solidity Contract
print("Compiling contract...")
install_solc("0.8.20") # Install the compiler version

with open("./contracts/AuditRegistry.sol", "r") as file:
    contract_source = file.read()

compiled_sol = compile_standard(
    {
        "language": "Solidity",
        "sources": {"AuditRegistry.sol": {"content": contract_source}},
        "settings": {
            "outputSelection": {
                "*": {"*": ["abi", "metadata", "evm.bytecode", "evm.sourceMap"]}
            }
        },
    },
    solc_version="0.8.20",
)

# 2. Extract Bytecode and ABI
bytecode = compiled_sol["contracts"]["AuditRegistry.sol"]["AuditRegistry"]["evm"]["bytecode"]["object"]
abi = compiled_sol["contracts"]["AuditRegistry.sol"]["AuditRegistry"]["abi"]

# 3. Deploy the Contract
account = web3.eth.account.from_key(PRIVATE_KEY)
print(f"Deploying from address: {account.address}")

AuditRegistry = web3.eth.contract(abi=abi, bytecode=bytecode)

# Build transaction
transaction = AuditRegistry.constructor().build_transaction({
    "chainId": 177,
    "gas": 3000000,
    "maxFeePerGas": web3.to_wei("500", "gwei"),
    "maxPriorityFeePerGas": web3.to_wei("400", "gwei"),
    "nonce": web3.eth.get_transaction_count(account.address),
})

# Sign and send
signed_txn = web3.eth.account.sign_transaction(transaction, private_key=PRIVATE_KEY)
print("Sending deployment transaction...")
tx_hash = web3.eth.send_raw_transaction(signed_txn.raw_transaction)

print(f"Transaction sent! Hash: {web3.to_hex(tx_hash)}")
print("Waiting for receipt...")
tx_receipt = web3.eth.wait_for_transaction_receipt(tx_hash)

print(f"🎉 Contract successfully deployed to: {tx_receipt.contractAddress}")
print("👉 COPY THIS ADDRESS AND PUT IT IN web3_bridge.py")

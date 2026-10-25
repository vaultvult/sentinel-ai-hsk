import json
from web3 import Web3
import os
from dotenv import load_dotenv

load_dotenv()

# Working HSK Testnet RPC
RPC_URL = "https://mainnet.hsk.xyz"
web3 = Web3(Web3.HTTPProvider(RPC_URL))

def log_audit_to_chain(target_contract, risk_score, report_hash):
    private_key = os.getenv("PRIVATE_KEY")
    account = web3.eth.account.from_key(private_key)
    
    # PASTE YOUR DEPLOYED CONTRACT ADDRESS HERE (From the previous step)
    contract_address = "0xNEW_MAINNET_ADDRESS"
    
    abi = json.loads('[{"inputs":[{"internalType":"address","name":"_targetContract","type":"address"},{"internalType":"string","name":"_riskScore","type":"string"},{"internalType":"string","name":"_reportHash","type":"string"}],"name":"recordAudit","outputs":[],"stateMutability":"nonpayable","type":"function"}]')
    
    contract = web3.eth.contract(address=contract_address, abi=abi)
    
    print(f"Connecting to HSK Chain to log audit for {target_contract}...")
    
    nonce = web3.eth.get_transaction_count(account.address)
    tx = contract.functions.recordAudit(
        target_contract, 
        risk_score, 
        report_hash
    ).build_transaction({
        'chainId': 177,
        'gas': 200000,
        'maxFeePerGas': web3.to_wei('2', 'gwei'),
        'maxPriorityFeePerGas': web3.to_wei('1', 'gwei'),
        'nonce': nonce,
    })
    
    signed_tx = web3.eth.account.sign_transaction(tx, private_key)
    
    # Notice we use raw_transaction here now!
    tx_hash = web3.eth.send_raw_transaction(signed_tx.raw_transaction)
    
    print(f"✅ Transaction sent! Hash: {web3.to_hex(tx_hash)}")

if __name__ == "__main__":
    log_audit_to_chain("0x000000000000000000000000000000000000dEaD", "SAFE", "hash_12345")

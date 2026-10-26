import time
from web3 import Web3
import os
from dotenv import load_dotenv

load_dotenv()

RPC_URL = "https://mainnet.hsk.xyz"
web3 = Web3(Web3.HTTPProvider(RPC_URL))

# HSKSwap Router Address (Found from Block Explorer)
HSK_SWAP_ROUTER = "0xd61261f13340c8296E0C4B7b52f7bEEa5c14644f"

# Standard ERC20 ABI for Approvals
ERC20_ABI = '[{"inputs":[{"internalType":"address","name":"spender","type":"address"},{"internalType":"uint256","name":"amount","type":"uint256"}],"name":"approve","outputs":[{"internalType":"bool","name":"","type":"bool"}],"stateMutability":"nonpayable","type":"function"},{"inputs":[{"internalType":"address","name":"owner","type":"address"},{"internalType":"address","name":"spender","type":"address"}],"name":"allowance","outputs":[{"internalType":"uint256","name":"","type":"uint256"}],"stateMutability":"view","type":"function"}]'

# Standard V2 Router ABI for Swaps
ROUTER_ABI = '[{"inputs":[{"internalType":"uint256","name":"amountIn","type":"uint256"},{"internalType":"uint256","name":"amountOutMin","type":"uint256"},{"internalType":"address[]","name":"path","type":"address[]"},{"internalType":"address","name":"to","type":"address"},{"internalType":"uint256","name":"deadline","type":"uint256"}],"name":"swapExactTokensForTokens","outputs":[{"internalType":"uint256[]","name":"amounts","type":"uint256[]"}],"stateMutability":"nonpayable","type":"function"}]'

def approve_token(private_key, token_address, amount_wei):
    """Approves the HSKSwap router to spend the token."""
    account = web3.eth.account.from_key(private_key)
    token_contract = web3.eth.contract(address=token_address, abi=ERC20_ABI)
    
    # Check existing allowance
    allowance = token_contract.functions.allowance(account.address, HSK_SWAP_ROUTER).call()
    if allowance >= amount_wei:
        return "Already Approved"

    print(f"Approving {token_address} for swap...")
    tx = token_contract.functions.approve(HSK_SWAP_ROUTER, amount_wei).build_transaction({
        'chainId': 177,
        'gas': 100000,
        'maxFeePerGas': web3.to_wei('2', 'gwei'),
        'maxPriorityFeePerGas': web3.to_wei('1', 'gwei'),
        'nonce': web3.eth.get_transaction_count(account.address),
    })
    
    signed_tx = web3.eth.account.sign_transaction(tx, private_key)
    tx_hash = web3.eth.send_raw_transaction(signed_tx.raw_transaction)
    web3.eth.wait_for_transaction_receipt(tx_hash)
    return "Approval Successful"

def execute_hsk_swap(private_key, token_in_address, token_out_address, amount_in_wei):
    """Executes the actual swap on HSKSwap."""
    account = web3.eth.account.from_key(private_key)
    router_contract = web3.eth.contract(address=HSK_SWAP_ROUTER, abi=ROUTER_ABI)
    
    # 1. Ensure Approval
    approve_token(private_key, token_in_address, amount_in_wei)
    
    print("Executing swap...")
    path = [token_in_address, token_out_address]
    deadline = int(time.time()) + 1200 # 20 minutes from now
    
    tx = router_contract.functions.swapExactTokensForTokens(
        amount_in_wei,
        0, # amountOutMin (0 for MVP, set slippage in production)
        path,
        account.address,
        deadline
    ).build_transaction({
        'chainId': 177,
        'gas': 300000,
        'maxFeePerGas': web3.to_wei('2', 'gwei'),
        'maxPriorityFeePerGas': web3.to_wei('1', 'gwei'),
        'nonce': web3.eth.get_transaction_count(account.address),
    })
    
    signed_tx = web3.eth.account.sign_transaction(tx, private_key)
    tx_hash = web3.eth.send_raw_transaction(signed_tx.raw_transaction)
    
    return web3.to_hex(tx_hash)

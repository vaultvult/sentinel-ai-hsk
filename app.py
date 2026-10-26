from flask import Flask, request, jsonify, render_template
from agent.scanner import scan_contract
from agent.web3_bridge import execute_hsk_swap
import time
import threading
import webbrowser
import os
import random

app = Flask(__name__)

# Real Token Addresses on HSK Mainnet
USDT_ADDRESS = "0xf1B50eD67A9e2CC94Ad3c477779E2d4cBfF9029"
# You must verify the official WHSK address on the explorer, using a placeholder for now
WHSK_ADDRESS = "0x...WHSK_ADDRESS_HERE..." 

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/api/chat', methods=['POST'])
def chat():
    data = request.json
    user_msg = data.get('message').lower()
    
    time.sleep(1)
    
    if "buy" in user_msg or "trade" in user_msg:
        words = user_msg.split()
        target_address = next((w for w in words if w.startswith('0x')), None)
        
        if not target_address:
            return jsonify({"response": "Please provide a valid contract address (0x...)."})
            
        # 1. RUN SENTINEL SECURITY SCAN
        risk_score = scan_contract(target_address)
        
        if risk_score == "HIGH_RISK":
            return jsonify({
                "response": f"🚨 SECURITY ALERT: I analyzed {target_address}. A vulnerability was detected. I have BLOCKED the trade to protect your funds."
            })
            
        elif risk_score == "SAFE":
            # 2. EXECUTE REAL SWAP (If using the safe address, we swap 1 USDT to WHSK as a test)
            if target_address.lower() == "0xsafe_address_456":
                try:
                    # 1 USDT (6 decimals)
                    amount_in_wei = 1000000 
                    tx_hash = execute_hsk_swap(
                        private_key=os.getenv("PRIVATE_KEY"),
                        token_in_address=USDT_ADDRESS,
                        token_out_address=WHSK_ADDRESS,
                        amount_in_wei=amount_in_wei
                    )
                    return jsonify({
                        "response": f"✅ ANALYSIS CLEAN. I have executed the trade on HSKSwap!\n\nTx Hash: {tx_hash}"
                    })
                except Exception as e:
                    return jsonify({
                        "response": f"✅ ANALYSIS CLEAN. But swap failed. Check wallet funds/approvals.\n\nError: {str(e)}"
                    })
            else:
                # Fallback for dummy addresses
                mock_tx = "0x" + "".join(random.choices("0123456789abcdef", k=64))
                return jsonify({
                    "response": f"✅ ANALYSIS CLEAN for {target_address}. Simulating swap...\nTx Hash: {mock_tx}"
                })
                
    elif "market" in user_msg or "price" in user_msg:
         return jsonify({"response": "📈 Market Monitor: HSK is up 4.2% in the last hour. DeFi volume is increasing."})
    else:
        return jsonify({"response": "I am Sentinel AI. Ask me to monitor markets or execute trades."})

@app.route('/api/scan', methods=['POST'])
def scan():
    data = request.json
    target_address = data.get('address')
    if not target_address:
        return jsonify({"status": "error", "message": "No address provided"}), 400

    risk_score = scan_contract(target_address)
    
    if risk_score == "HIGH_RISK":
        return jsonify({"status": "blocked", "message": "🚨 VULNERABILITY DETECTED. Trade execution BLOCKED."})
    elif risk_score == "SAFE":
        return jsonify({"status": "success", "message": "✅ SCAN CLEAN. Ready for execution.", "tx_hash": "0x4bff367a732e7c44f9018bc6cbdab85161dd36f1dc1d81555d574ad8b3106fb1"})
    else:
        return jsonify({"status": "warning", "message": "⚠️ UNKNOWN CONTRACT. Manual review required."})

@app.route('/shutdown', methods=['POST'])
def shutdown():
    os._exit(0)

def open_browser():
    webbrowser.open_new("http://127.0.0.1:5000")

if __name__ == '__main__':
    threading.Timer(1.5, open_browser).start()
    app.run(debug=False, port=5000)

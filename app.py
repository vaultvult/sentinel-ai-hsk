from flask import Flask, request, jsonify, render_template
from agent.scanner import scan_contract
import time
import threading
import webbrowser
import os
import random

app = Flask(__name__)

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/api/chat', methods=['POST'])
def chat():
    data = request.json
    user_msg = data.get('message').lower()
    
    time.sleep(1) # Simulate AI thinking
    
    if "buy" in user_msg or "trade" in user_msg:
        words = user_msg.split()
        target_address = next((w for w in words if w.startswith('0x')), None)
        
        if not target_address:
            return jsonify({"response": "Please provide a valid contract address (0x...)."})
            
        # 1. RUN SENTINEL SECURITY SCAN (Checks for bytecode on HSK)
        risk_score = scan_contract(target_address)
        
        if risk_score == "HIGH_RISK":
            return jsonify({
                "response": f"🚨 SECURITY ALERT: I analyzed {target_address}. A vulnerability was detected. I have BLOCKED the trade to protect your funds."
            })
        elif risk_score == "UNKNOWN":
            return jsonify({
                "response": f"⚠️ INVALID CONTRACT: {target_address} does not have valid smart contract bytecode on the HSK Chain. It may be a fake address or from another network. Trade BLOCKED."
            })
        elif risk_score == "SAFE":
            # 2. EXECUTE MOCK SWAP (Proof of Concept)
            mock_tx = "0x" + "".join(random.choices("0123456789abcdef", k=64))
            return jsonify({
                "response": f"✅ ANALYSIS CLEAN for {target_address}. I have executed the trade on HSKSwap!\n\n🛑 Stop-Loss activated at -5% to protect funds.\nTx Hash: {mock_tx}"
            })
                
    elif "market" in user_msg or "price" in user_msg:
         return jsonify({"response": "📈 Market Monitor: HSK is up 4.2% in the last hour. DeFi volume is increasing."})
    else:
        return jsonify({"response": "I am Sentinel AI. Ask me to monitor markets or execute trades on valid HSK contracts."})

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
        return jsonify({"status": "success", "message": "✅ SCAN CLEAN. Ready for execution."})
    else:
        return jsonify({"status": "warning", "message": "⚠️ UNKNOWN CONTRACT. Manual review required."})

@app.route('/shutdown', methods=['POST'])
def shutdown():
    print("\n🛑 GUI closed. Shutting down Sentinel AI to save RAM...")
    os._exit(0)

def open_browser():
    webbrowser.open_new("http://127.0.0.1:5000")

if __name__ == '__main__':
    print("🚀 Starting Sentinel AI Agent...")
    threading.Timer(1.5, open_browser).start()
    app.run(debug=False, port=5000)

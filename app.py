from flask import Flask, request, jsonify, render_template
from agent.scanner import scan_contract
import time
import threading
import webbrowser
import os

app = Flask(__name__)

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/api/scan', methods=['POST'])
def scan():
    data = request.json
    target_address = data.get('address')
    
    if not target_address:
        return jsonify({"status": "error", "message": "No address provided"}), 400

    risk_score = scan_contract(target_address)
    
    if risk_score == "HIGH_RISK":
        return jsonify({
            "status": "blocked",
            "message": "🚨 VULNERABILITY DETECTED. Trade execution BLOCKED.",
            "risk": risk_score
        })
    elif risk_score == "SAFE":
        time.sleep(1.5)
        mock_tx_hash = "0x4bff367a732e7c44f9018bc6cbdab85161dd36f1dc1d81555d574ad8b3106fb1"
        return jsonify({
            "status": "success",
            "message": "✅ SCAN CLEAN. Proceeding with trade and logging proof.",
            "risk": risk_score,
            "tx_hash": mock_tx_hash
        })
    else:
        return jsonify({
            "status": "warning",
            "message": "⚠️ UNKNOWN CONTRACT. Manual review required.",
            "risk": risk_score
        })

# New Route: Kills the server when the browser tab is closed
@app.route('/shutdown', methods=['POST'])
def shutdown():
    print("\n🛑 GUI closed. Shutting down Sentinel AI to save RAM...")
    os._exit(0) # Instantly kills the Python process

def open_browser():
    webbrowser.open_new("http://127.0.0.1:5000")

if __name__ == '__main__':
    print("🚀 Starting Sentinel AI Agent...")
    # Open browser after a 1.5 second delay to let Flask start up
    threading.Timer(1.5, open_browser).start()
    # debug=False is crucial here so the shutdown command works perfectly
    app.run(debug=False, port=5000)

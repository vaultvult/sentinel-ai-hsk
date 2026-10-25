# 🛡️ Sentinel AI: Security-First Trading Agent for HSK Chain

## 📖 Overview
Sentinel AI is an AI-agent-based automated trading system built for the **HSK Chain Horizon Hackathon**. 

While most AI trading bots focus purely on profit maximization, they blindly interact with unverified DeFi protocols, exposing users to devastating smart contract exploits. Sentinel AI solves this by acting as a **trust and security layer**. Before executing any trade, the AI agent performs a real-time vulnerability scan of the target contract and logs the immutable audit proof on the HSK Chain.

## 🏆 Hackathon Track Alignment
*   **Track:** AI Agent Trading
*   **Why it wins:** It directly addresses the biggest fear in AI-driven DeFi: *malicious contracts*. By combining a trading agent with a built-in real-time smart contract vulnerability scanner, Sentinel AI brings institutional-grade compliance and safety to the HSK ecosystem.

## ⚙️ How It Works
1. **Target Identification:** The user (or an automated strategy) inputs a target DeFi contract address.
2. **AI Security Scan:** The agent runs a static analysis vulnerability check.
3. **Execution Gate:** 
   * If the risk is **HIGH**, the trade is instantly blocked to protect funds.
   * If the contract is **SAFE**, the agent proceeds.
4. **Immutable On-Chain Proof:** Before executing the trade, the agent sends a transaction to our `AuditRegistry` smart contract on HSK Chain, permanently logging the security clearance.

## 🛠️ Tech Stack
*   **Smart Contracts:** Solidity (`AuditRegistry.sol`)
*   **AI Agent / Backend:** Python, Web3.py, Flask
*   **Frontend:** Custom Vanilla HTML/CSS/JS Dashboard
*   **Network:** HSK Chain (Testnet)

## 🚀 How to Run Locally
1. Clone the repo: `git clone https://github.com/vaultvult/sentinel-ai-hsk.git`
2. Create a virtual environment: `python3 -m venv venv && source venv/bin/activate`
3. Install dependencies: `pip install -r requirements.txt` (or `pip install web3 python-dotenv flask`)
4. Add your private key to a `.env` file: `PRIVATE_KEY=your_key`
5. Launch the Agent: `python app.py`

## 🔮 The "Military-Grade" Roadmap
This MVP is the foundation. Our long-term vision for Sentinel AI includes:
*   Integration of full LLM-driven threat modeling (e.g., OpenAI/Claude) for zero-day exploit detection.
*   Integration with Chainlink CCIP for cross-chain audit verification.
*   A decentralized network of security auditors that the AI can query in real-time.

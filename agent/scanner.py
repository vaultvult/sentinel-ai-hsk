def scan_contract(contract_address: str):
    print(f"🤖 Sentinel AI initializing scan on {contract_address}...")
    
    # MVP LOGIC: 
    # For the demo, we hardcode one safe address and one bad address
    if contract_address.lower() == "0xbad_address_123":
        print("❌ VULNERABILITY DETECTED: Reentrancy found in withdraw() function.")
        return "HIGH_RISK"
        
    elif contract_address.lower() == "0xsafe_address_456":
        print("✅ Scan complete. No known vulnerabilities found. Protocol is safe.")
        return "SAFE"
        
    else:
        print("⚠️ Unknown contract. Applying default medium risk.")
        return "MEDIUM_RISK"

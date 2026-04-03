import os
import requests
import time
import dotenv

# 1. Load your hidden secrets from .env
dotenv.load_dotenv()
RPC_URL = os.getenv("RPC_URL")
TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")
CHAT_ID = os.getenv("TELEGRAM_CHAT_ID")

# Raydium Liquidity Pool V4 Address
RAY_PROG = "675kPX9MHTjS2zt1qfr1NYHuzeLXfQM9H24wFSUt1Mp8"

def send_telegram(message):
    """Sends a real-time alert to your Telegram App"""
    url = f"https://api.telegram.org/bot{TOKEN}/sendMessage"
    payload = {"chat_id": CHAT_ID, "text": message}
    try:
        # We use a short timeout so a slow network doesn't freeze the bot
        requests.post(url, json=payload, timeout=5)
    except Exception as e:
        print(f"❌ Telegram Error: {e}")

def get_latest_signatures():
    """Fetches the 5 most recent transactions from the Raydium Program"""
    payload = {
        "jsonrpc": "2.0", "id": 1,
        "method": "getSignaturesForAddress",
        "params": [RAY_PROG, {"limit": 5}]
    }
    try:
        response = requests.post(RPC_URL, json=payload, timeout=10).json()
        return response.get('result', [])
    except:
        return []

def is_new_pool(sig):
    """Deep-scans a transaction for the 'Initialize2' instruction"""
    payload = {
        "jsonrpc": "2.0", "id": 1,
        "method": "getTransaction",
        "params": [sig, {"encoding": "json", "maxSupportedTransactionVersion": 0}]
    }
    try:
        res = requests.post(RPC_URL, json=payload, timeout=10).json()
        meta = res.get('result', {}).get('meta', {})
        if not meta: return False
        
        # 'initialize2' is the specific signal for a new pool birth
        logs = str(meta.get('logMessages', []))
        if "initialize2" in logs.lower():
            return True
        return False
    except:
        return False

if __name__ == "__main__":
    print("🎯 SNIPER MODE: Active")
    print("📡 Monitoring Raydium for New Token Launches...")
    
    # --- THE TEST PING ---
    # This confirms your Telegram connection is 100% ready immediately
    send_telegram("🚀 Sniper Bot is officially ONLINE and watching Raydium!")
    
    seen_sigs = set()
    
    while True:
        signatures = get_latest_signatures()
        
        for item in signatures:
            sig = item['signature']
            
            if sig not in seen_sigs:
                seen_sigs.add(sig)
                
                # Check if this specific signature is a new pool creation
                if is_new_pool(sig):
                    msg = f"🔥 NEW TOKEN POOL DETECTED!\n\nView on Solscan:\nhttps://solscan.io/tx/{sig}"
                    print(msg)
                    send_telegram(msg)
        
        # Memory Management: Clears the 'seen' list after 100 items for your 4GB RAM
        if len(seen_sigs) > 100:
            seen_sigs.clear()
            
        time.sleep(3) # Scans every 3 seconds


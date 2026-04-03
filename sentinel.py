import os
import requests
import time
from dotenv import load_dotenv

# Load all secrets
load_dotenv()
RPC_URL = os.getenv("RPC_URL")
TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")
CHAT_ID = os.getenv("TELEGRAM_CHAT_ID")

def send_telegram_msg(text):
    url = f"https://api.telegram.org/bot{TOKEN}/sendMessage"
    payload = {"chat_id": CHAT_ID, "text": text, "parse_mode": "Markdown"}
    try:
        requests.post(url, json=payload)
    except Exception as e:
        print(f"❌ Telegram Error: {e}")

def get_block_height():
    payload = {"jsonrpc": "2.0", "id": 1, "method": "getBlockHeight"}
    try:
        response = requests.post(RPC_URL, json=payload).json()
        return response.get('result')
    except:
        return None

def monitor():
    print("🐋 Sentinel Live: Monitoring Solana Mainnet...")
    send_telegram_msg("🚀 *Sentinel Online:* I am now monitoring the Solana Mainnet for you.")
    
    last_height = get_block_height()
    
    while True:
        try:
            current_height = get_block_height()
            if current_height and current_height > last_height:
                msg = f"📦 *New Block Confirmed:* `{current_height}`"
                print(msg)
                # To save API credits and avoid spam, we won't telegram every block
                # but you can see it working in your terminal!
                last_height = current_height
            
            time.sleep(20) # Stay safe within Free Tier limits
        except Exception as e:
            print(f"⚠️ Reconnecting... {e}")
            time.sleep(10)

if __name__ == "__main__":
    monitor()


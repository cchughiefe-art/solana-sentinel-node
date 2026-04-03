import os
import requests
import time
from dotenv import load_dotenv

load_dotenv()
RPC_URL = os.getenv("RPC_URL")

def get_block_height():
    payload = {"jsonrpc": "2.0", "id": 1, "method": "getBlockHeight"}
    response = requests.post(RPC_URL, json=payload).json()
    return response.get('result')

def monitor():
    print("🐋 Sentinel is now scanning Solana Mainnet for Whales...")
    last_height = get_block_height()
    
    while True:
        try:
            current_height = get_block_height()
            if current_height > last_height:
                print(f"📦 New Block Detected: {current_height}")
                # This is where we will eventually add logic to 
                # scan every transaction in the block.
                last_height = current_height
            
            time.sleep(10) # Protect your free API credits
        except Exception as e:
            print(f"⚠️ Network lag... reconnecting: {e}")
            time.sleep(5)

if __name__ == "__main__":
    monitor()


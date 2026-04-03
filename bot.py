import os
import requests
import base58
from dotenv import load_dotenv

load_dotenv()
PK_B58 = os.getenv("SOLANA_PRIVATE_KEY")
RPC_URL = os.getenv("RPC_URL")

def derive_public_key(priv_key_b58):
    # Manually extract the public key from the secret key string
    # This avoids using the heavy 'solders' library
    decoded = base58.b58decode(priv_key_b58)
    # Solana keys are 64 bytes; the public part is the second half
    return base58.b58encode(decoded[32:64]).decode('utf-8')

def get_sol_balance(address):
    payload = {
        "jsonrpc": "2.0",
        "id": 1,
        "method": "getBalance",
        "params": [address]
    }
    response = requests.post(RPC_URL, json=payload).json()
    return response['result']['value'] / 1_000_000_000

if __name__ == "__main__":
    if not PK_B58:
        print("❌ Error: Add your SOLANA_PRIVATE_KEY to .env first!")
    else:
        address = derive_public_key(PK_B58)
        balance = get_sol_balance(address)
        print(f"✅ Bot Online")
        print(f"🔗 Address: {address}")
        print(f"💰 Balance: {balance} SOL")


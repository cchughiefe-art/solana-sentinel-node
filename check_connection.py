import requests

# Your QuickNode Endpoint
RPC_URL = "https://thrilling-bitter-general.solana-mainnet.quiknode.pro/81f9280b4959cf6926dcdf2d25904e29aeb3a9c7/"

def test_connection():
    payload = {
        "jsonrpc": "2.0",
        "id": 1,
        "method": "getHealth"
    }
    
    print("📡 Sending ping to Solana Mainnet...")
    # Using a session can help with connection stability
    session = requests.Session()
    try:
        response = session.post(RPC_URL, json=payload, timeout=10).json()
        if response.get('result') == 'ok':
            print("✅ SUCCESS: You are officially connected to the Solana Blockchain.")
        else:
            print(f"⚠️ RPC Error: {response}")
    except Exception as e:
        print(f"❌ Connection Error. Tip: Try switching from 4G to 3G or use a VPN.")
        print(f"Details: {e}")

if __name__ == "__main__":
    test_connection()


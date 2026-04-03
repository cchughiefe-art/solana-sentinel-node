import os
from dotenv import load_dotenv
from solders.keypair import Keypair

load_dotenv()
pk_string = os.getenv("SOLANA_PRIVATE_KEY")

if not pk_string:
    print("❌ ERROR: No key found in .env file!")
else:
    try:
        user_wallet = Keypair.from_base58_string(pk_string)
        print("✅ IDENTITY VERIFIED")
        print(f"🔗 Bot Public Address: {user_wallet.pubkey()}")
        print("\nYour bot is now authorized to sign trades.")
    except Exception as e:
        print(f"❌ ERROR: Invalid Key Format. {e}")


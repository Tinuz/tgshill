import asyncio
import random
import os
import requests
from telethon.sync import TelegramClient
from telethon.errors import FloodWaitError
from telethon.errors.rpcerrorlist import FloodWaitError, RPCError
from telethon.sessions import StringSession
from dotenv import load_dotenv  # <-- add this

load_dotenv()  # <-- load .env file

# Constants (replace with your real values or load from a config)
API_ID = os.getenv('API_ID')  # <-- get from .env
API_HASH = os.getenv('API_HASH')  # <-- get from .env
SESSION_STRING = os.getenv('SESSION_STRING')

REMOTE_API_URL = os.getenv('REMOTE_API_URL')

GROUPS = [
    'https://t.me/shillgrow',
    'https://t.me/GubbinLounge',
    'https://t.me/nano_caps',
    'https://t.me/suitscallsEUA',
    'https://t.me/anbucryptotalk',
    'https://t.me/RobShillingGemOfficial',
    'https://t.me/cryptoprodsshills',
    'https://t.me/diamondhandsB',
    'https://t.me/latinosBSC',
    'https://t.me/Shillqueen',
    'https://t.me/whalevomitdisc',
    'https://t.me/moneyshiill',
    'https://t.me/neverscamagain',
    'https://t.me/nanowhalesbsc',
    'https://t.me/gemsroombsc',
    'https://t.me/TheWolfCallChat',
    'https://t.me/cryptofrogslounge',
    'https://t.me/Hiddengemsearly',
    'https://t.me/mememecoins',
    'https://t.me/safedegens_bsc',
    'https://t.me/Shillvillebsc',
    #'https://t.me/lotusshill',
    #'https://t.me/hard_shill',
    #'https://t.me/chuletashill',
    #'https://t.me/NipseyCallsHouse',
    #'https://t.me/sgsbsc',
    #'https://t.me/airdroplink3',
    #'https://t.me/newsitelink',
    #'https://t.me/SpartaTG',
]

MESSAGES = [
    """🔥 $FOOF is HERE and it’s breaking all the rules! 🔥

Looking for the next big thing in Web3? 👀
Say less — $FOOF is pure chaos wrapped in a coin.

🧠 Built by devs who maybe know what they’re doing
🛠 Powered by Solana
📉 Designed for degens, not believers
✅ Burn tokens in a microwave: https://foofurburnchaos.vercel.app
✅ 100% community confusion
✅ No roadmap, just vibes

💥 Ticker: $FOOF
📉 Price: 0.000004406
💰 MC: 4.28K
📜 CA: EU1SX1z4J7RtZzDkRWPTfFsXBu3Jzn6p3fU7NF8Upump
🧨 Burn contest: https://foofurburnchaos.vercel.app
🌐 Website: https://foofurskatje-3uuf.vercel.app/
💬 Telegram: https://t.me/+gE6sb9xW8d5kZjI8
🐦 X: https://x.com/foofurskatje?s=21&t=S4OrVfGUBPJZJmlWZohR8A

This is just the beginning. Or the end. Hard to say.""",
    """🚨 Enter the $FOOF zone 🚨
No roadmap. No promises. Just absurdity.

🌀 Solana-powered chaos
🧠 Devs building with mild confusion
🔥 Tokens burn in a microwave
👀 Community fueled by bad decisions

💥 Ticker: $FOOF
📉 Price: 0.000004406
💰 MC: 4.28K
📜 CA: EU1SX1z4J7RtZzDkRWPTfFsXBu3Jzn6p3fU7NF8Upump
🧨 Burn contest: https://foofurburnchaos.vercel.app
🌐 Website: https://foofurskatje-3uuf.vercel.app/
💬 Telegram: https://t.me/+gE6sb9xW8d5kZjI8
🐦 X: https://x.com/foofurskatje?s=21&t=S4OrVfGUBPJZJmlWZohR8A

Just vibes. Just $FOOF.
The toaster is waiting."""
]

IMAGES_DIR = 'images'  # Map met afbeeldingen

def get_random_image():
    if not os.path.isdir(IMAGES_DIR):
        return None
    images = [os.path.join(IMAGES_DIR, f) for f in os.listdir(IMAGES_DIR)
              if f.lower().endswith(('.png', '.jpg', '.jpeg', '.gif', '.webp'))]
    if not images:
        return None
    return random.choice(images)

async def send_shill_message(client, group, message):
    try:
        image_path = get_random_image()
        sent_with_image = False
        if random.random() < 0.7 and image_path:
            try:
                await client.send_file(group, image_path, caption=message)
                sent_with_image = True
            except RPCError as e:
                if getattr(e, 'code', None) == 403 and 'CHAT_SEND_PHOTOS_FORBIDDEN' in str(e):
                    print(f"⚠️ Can't send photo to {group}, sending text only.")
                    await client.send_message(group, message)
                else:
                    raise
        else:
            await client.send_message(group, message)
        print(f"✅ Sent to {group}")
        # Log naar API sturen
        try:
            requests.post(
                f"{REMOTE_API_URL}/api/logs",
                json={
                    "group": group,
                    "message": "Posted with image" if sent_with_image else "Posted text only"
                }
            )
        except Exception as log_exc:
            print(f"⚠️ Failed to log to API: {log_exc}")
    except FloodWaitError as e:
        print(f"⏳ Flood wait triggered: sleeping {e.seconds} seconds for group {group}")
        await asyncio.sleep(e.seconds + 10)
    except Exception as e:
        print(f"❌ Failed to send to {group}: {e}")
        # Log fout naar API
        try:
            requests.post(
                f"{REMOTE_API_URL}/api/logs",
                json={
                    "group": group,
                    "message": f"Failed: {e}"
                }
            )
        except Exception as log_exc:
            print(f"⚠️ Failed to log error to API: {log_exc}")

async def main():
    async with TelegramClient(StringSession(SESSION_STRING), API_ID, API_HASH) as client:
        groups_to_send = GROUPS
        random.shuffle(groups_to_send)
        total_groups = len(groups_to_send)
        min_wait = 10    # minimaal 10 seconden tussen berichten
        max_wait = 90    # maximaal 90 seconden tussen berichten (pas aan naar wens)
        for idx, group in enumerate(groups_to_send):
            msg = random.choice(MESSAGES)
            await send_shill_message(client, group, msg)
            if idx < len(groups_to_send) - 1:
                await asyncio.sleep(random.uniform(min_wait, max_wait))  # random wachttijd

asyncio.run(main())

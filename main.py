import asyncio
import time
import os
from datetime import datetime
from pyrogram import Client, filters, idle
from pyrogram.types import Message
from dotenv import load_dotenv
from ytthumb import download_thumbnail
from pyrogram.errors import BadMsgNotification

# Load environment variables
load_dotenv()

API_ID = os.getenv("API_ID")
API_HASH = os.getenv("API_HASH")
BOT_TOKEN = os.getenv("BOT_TOKEN")

# Initialize Pyrogram Client
app = Client("GroupBot", api_id=API_ID, api_hash=API_HASH, bot_token=BOT_TOKEN)

@app.on_message(filters.private & filters.command("start"))
async def start(client: Client, message: Message):
    await message.reply_text("🤖 Hello! I'm your group management bot. I can also download YouTube thumbnails!")

@app.on_message(filters.command("thumb"))
async def youtube_thumbnail(client: Client, message: Message):
    if len(message.command) < 2:
        await message.reply_text("❌ Please provide a valid YouTube video URL.")
        return

    video_url = message.command[1]
    file_name = download_thumbnail(video_url)
    if file_name:
        await message.reply_photo(photo=file_name)
    else:
        await message.reply_text("❌ Unable to fetch the thumbnail. Please check the YouTube video URL.")

# ✅ Fix: Sync Time Using Python (Instead of ntpdate)
async def sync_time():
    try:
        # Get current time from an online server
        import requests
        response = requests.get("http://worldtimeapi.org/api/timezone/Etc/UTC")
        current_time = response.json()["unixtime"]
        os.environ["TZ"] = "UTC"
        time.tzset()
        print(f"✅ Time synchronized: {datetime.utcfromtimestamp(current_time)} UTC")
    except Exception as e:
        print(f"⚠️ Time sync failed: {e}")

async def start_bot():
    await sync_time()  # First, sync time before starting the bot
    retries = 5  # Number of retries
    delay = 10  # Wait time between retries

    for attempt in range(retries):
        try:
            print("🚀 Bot is starting...")
            await app.start()
            print("✅ Bot is running!")
            await idle()
            break
        except BadMsgNotification as e:
            print(f"❌ Time sync error: {e}")
            if attempt < retries - 1:
                print(f"🔄 Retrying... Attempt {attempt + 1}/{retries}")
                await asyncio.sleep(delay)
            else:
                print("❌ Failed to synchronize time after multiple attempts.")
                break
        except Exception as e:
            print(f"❌ General error: {e}")
            if attempt < retries - 1:
                print(f"🔄 Retrying... Attempt {attempt + 1}/{retries}")
                await asyncio.sleep(delay)
            else:
                print("❌ Bot startup failed after multiple attempts.")
                break

if __name__ == "__main__":
    asyncio.run(start_bot())

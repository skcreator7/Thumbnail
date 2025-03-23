import asyncio
from pyrogram import Client, filters, idle
from pyrogram.types import Message
from dotenv import load_dotenv
import os
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

async def start_bot():
    try:
        print("🚀 Bot is starting...")
        await app.start()
        print("✅ Bot is running!")
        await idle()  # Keeps the bot running
    except Exception as e:
        print(f"❌ Bot startup failed: {e}")

if __name__ == "__main__":
    asyncio.run(start_bot())  # ✅ Corrected Code

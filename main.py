import asyncio
import os
from fastapi import FastAPI
from pyrogram import Client, filters
from pyrogram.types import Message
from dotenv import load_dotenv
from ytthumb import download_thumbnail  # YouTube Thumbnail Downloader

# Load environment variables
load_dotenv()

API_ID = int(os.getenv("API_ID"))
API_HASH = os.getenv("API_HASH")
BOT_TOKEN = os.getenv("BOT_TOKEN")

# Initialize FastAPI App
app = FastAPI()

# Initialize Pyrogram Client
bot = Client("GroupBot", api_id=API_ID, api_hash=API_HASH, bot_token=BOT_TOKEN)

@app.get("/")
def home():
    return {"message": "🚀 Telegram Bot is Running with FastAPI!"}

@bot.on_message(filters.private & filters.command("start"))
async def start(client: Client, message: Message):
    await message.reply_text("🤖 Hello! I'm your group management bot. I can also download YouTube thumbnails!")

@bot.on_message(filters.command("thumb"))
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

# ✅ Start Bot in Background
async def start_bot():
    print("🚀 Bot is starting...")
    await bot.start()
    print("✅ Bot is running!")

asyncio.create_task(start_bot())  # Run Pyrogram bot in background

import asyncio
from pyrogram import Client, filters
from pyrogram.types import Message
from dotenv import load_dotenv
import os
from ytthumb import download_thumbnail  # Import the YouTube thumbnail downloader

# Load environment variables
load_dotenv()

API_ID = os.getenv("API_ID")
API_HASH = os.getenv("API_HASH")
BOT_TOKEN = os.getenv("BOT_TOKEN")

# Initialize Pyrogram Client
app = Client("GroupBot", api_id=API_ID, api_hash=API_HASH, bot_token=BOT_TOKEN)

### ✅ Bot Start Message
@app.on_message(filters.private & filters.command("start"))
async def start(client: Client, message: Message):
    await message.reply_text("🤖 Hello! I'm your group management bot. I can also download YouTube thumbnails!")

### ✅ YouTube Thumbnail Downloader
@app.on_message(filters.command("thumb"))
async def youtube_thumbnail(client: Client, message: Message):
    if len(message.command) < 2:
        await message.reply_text("❌ Please provide a valid YouTube video URL.")
        return

    video_url = message.command[1]
    
    # Download and send the thumbnail image
    file_name = download_thumbnail(video_url)
    if file_name:
        await message.reply_photo(photo=file_name)
    else:
        await message.reply_text("❌ Unable to fetch the thumbnail. Please check the YouTube video URL.")

### ✅ Auto-Delete Non-Admin Messages After 5 Minutes
@app.on_message(filters.group & ~filters.service)
async def auto_delete_messages(client: Client, message: Message):
    from group_manager import is_admin  # Import admin check function

    if await is_admin(client, message.chat.id, message.from_user.id):
        return  # Don't delete admin messages

    await asyncio.sleep(300)  # Wait for 5 minutes

    try:
        # Check if the message still exists
        await message.delete()
    except Exception as e:
        print(f"Error deleting message: {e}")

### ✅ Bot Startup
async def main():
    print("🚀 Bot is starting...")
    await app.start()
    print("✅ Bot is running!")
    await idle()

if __name__ == "__main__":
    asyncio.run(main())

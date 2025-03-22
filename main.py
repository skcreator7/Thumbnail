import os
import re
import asyncio
import threading
from dotenv import load_dotenv
from pyrogram import Client, filters
from pyrogram.types import Message, InlineKeyboardMarkup, InlineKeyboardButton, InputMediaPhoto
from pyrogram.errors import FloodWait
import ytthumb
from fastapi import FastAPI
import uvicorn

# Load environment variables
load_dotenv()

# Initialize bot
app = Client(
    "YouTube-Thumbnail-Downloader",
    bot_token=os.environ.get("BOT_TOKEN"),
    api_id=int(os.environ.get("API_ID")),
    api_hash=os.environ.get("API_HASH")
)

# FastAPI for Koyeb health check
web_app = FastAPI()

@web_app.get("/")
def home():
    return {"status": "running"}

# Function to run the web server in a separate thread
def run_web_server():
    uvicorn.run(web_app, host="0.0.0.0", port=8000)

# Function to delete a message after 5 minutes
async def delete_message(message: Message):
    await asyncio.sleep(300)  # 5 minutes
    await message.delete()

# START Message & Buttons
START_TEXT = """Hello {},
I am a simple YouTube thumbnail downloader and group manager bot.

- **Send a YouTube video link or ID**, and I'll send the thumbnail.
- **Send a YouTube video link with quality** (e.g., `rokGy0huYEA | sd`):
  - `sd` - Standard Quality
  - `mq` - Medium Quality
  - `hq` - High Quality
  - `maxres` - Maximum Resolution
"""

START_BUTTONS = InlineKeyboardMarkup(
    [
        [InlineKeyboardButton("📢 Update Channel", url='https://t.me/SkFilmbox')],
        [InlineKeyboardButton("☎️ Admin", url='https://t.me/Skadminrobot')]
    ]
)

# Handler for "/start" and "/help" commands
@app.on_message(filters.private & filters.command(["start", "help"]))
async def start(_, message):
    await message.reply_text(
        text=START_TEXT.format(message.from_user.mention),
        disable_web_page_preview=True,
        reply_markup=START_BUTTONS,
        quote=True
    )

# YouTube Thumbnail Downloader
@app.on_message(filters.private & filters.text)
async def send_thumbnail(_, message):
    msg = await message.reply_text("`Analyzing...`", quote=True)
    try:
        if " | " in message.text:
            video, quality = message.text.split(" | ")
        else:
            video, quality = message.text, "sd"

        thumbnail = ytthumb.thumbnail(video=video, quality=quality)
        await message.reply_photo(photo=thumbnail, quote=True)
        await msg.delete()
    except Exception:
        await msg.edit_text("❌ Invalid video ID or URL.")

# Group Message Moderation (Delete links, usernames & non-admin messages)
@app.on_message(filters.group)
async def handle_group_message(client: Client, message: Message):
    # Ignore messages from admins
    user = await client.get_chat_member(message.chat.id, message.from_user.id)
    if user.status in ["administrator", "creator"]:
        return  

    # Check if message contains a link or username
    if re.search(r"(https?:\/\/|@[A-Za-z0-9_]+)", message.text):
        await message.reply_text("❌ Sending links or usernames is not allowed!")
        return

    # Schedule message deletion after 5 minutes
    asyncio.create_task(delete_message(message))

# Main function
async def main():
    # Start the web server in a separate thread
    threading.Thread(target=run_web_server, daemon=True).start()

    async with app:
        await app.run()

# Run the bot
if __name__ == "__main__":
    asyncio.run(main())

import os
import asyncio
import ytthumb
from dotenv import load_dotenv
from pyrogram import Client, filters
from pyrogram.types import InlineKeyboardMarkup, InlineKeyboardButton, InputMediaPhoto
from pyrogram.errors import FloodWait

# Load environment variables
load_dotenv()

# Initialize bot client
app = Client(
    "YouTube-Thumbnail-Downloader",
    bot_token=os.getenv("BOT_TOKEN"),
    api_id=int(os.getenv("API_ID")),
    api_hash=os.getenv("API_HASH")
)

# Start message
START_TEXT = """Hello {},
I am a YouTube thumbnail downloader bot.

- Send a YouTube video link or video ID.
- I will send the thumbnail.
- You can also specify quality (e.g., `rokGy0huYEA | maxres`).

Qualities:
  - sd → Standard Quality
  - mq → Medium Quality
  - hq → High Quality
  - maxres → Maximum Resolution
"""

START_BUTTONS = InlineKeyboardMarkup([
    [InlineKeyboardButton("📢 Updates", url="https://t.me/SkFilmbox")],
    [InlineKeyboardButton("☎️ Admin", url="https://t.me/Skadminrobot")]
])

# Command: /start
@app.on_message(filters.private & filters.command(["start", "help"]))
async def start(_, message):
    await message.reply_text(
        text=START_TEXT.format(message.from_user.mention),
        disable_web_page_preview=True,
        reply_markup=START_BUTTONS
    )

# Handle text messages (YouTube links)
@app.on_message(filters.private & filters.text)
async def send_thumbnail(_, message):
    processing = await message.reply_text("`Fetching thumbnail...`")

    try:
        if " | " in message.text:
            video, quality = message.text.split(" | ")
        else:
            video, quality = message.text, "sd"

        thumbnail = ytthumb.thumbnail(video=video, quality=quality)

        await message.reply_photo(photo=thumbnail)
        await processing.delete()
    except Exception:
        await processing.edit_text(
            text="Error fetching thumbnail! Please try again.",
            disable_web_page_preview=True,
            reply_markup=START_BUTTONS
        )

async def main():
    async with app:
        await app.run()

if __name__ == "__main__":
    asyncio.run(main())

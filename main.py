import os
import ytthumb
from dotenv import load_dotenv
from pyrogram import Client, filters
from pyrogram.types import InlineKeyboardMarkup, InlineKeyboardButton, InputMediaPhoto
from pyrogram.errors import FloodWait
import asyncio

# Load environment variables
load_dotenv()

app = Client(
    "YouTube-Thumbnail-Downloader",
    bot_token=os.environ.get("BOT_TOKEN"),
    api_id=int(os.environ.get("API_ID")),
    api_hash=os.environ.get("API_HASH")
)

START_TEXT = """Hello {},
I am a simple YouTube thumbnail downloader Telegram bot.

- Send a YouTube video link or video ID.
- I will send the thumbnail.
- You can also send a YouTube video link or video ID with quality. (like: `rokGy0huYEA | sd`)
  - sd - Standard Quality
  - mq - Medium Quality
  - hq - High Quality
  - maxres - Maximum Resolution
"""

START_BUTTONS = InlineKeyboardMarkup([
    [InlineKeyboardButton("🎬 WhatsApp Movies Channel", url='https://whatsapp.com/channel/0029VaCUrJwEAKW5rDJXz23h')],
    [InlineKeyboardButton("🎬 WhatsApp Movies Channel 2", url='https://whatsapp.com/channel/0029Va69Ts2C6ZvmEWsHNo3c')],
    [InlineKeyboardButton("🔎 Movies Search Group", url='https://t.me/+_AWkWy0499dlZjQ1')],
    [InlineKeyboardButton("🔎 Movies Search Group 2", url='https://t.me/+cxiYHGE4jW9jOTY9')],
    [InlineKeyboardButton("📢 Update Channel", url='https://t.me/SkFilmbox')],
    [InlineKeyboardButton("☎️ Admin", url='https://t.me/Skadminrobot')]
])

@app.on_callback_query()
async def cb_data(_, callback_query):
    data = callback_query.data.lower()
    if data in ytthumb.qualities():
        thumbnail = ytthumb.thumbnail(
            video=callback_query.message.reply_to_message.text,
            quality=data
        )
        await callback_query.answer('Updating')
        await callback_query.edit_message_media(media=InputMediaPhoto(media=thumbnail))
        await callback_query.answer('Updated Successfully')

@app.on_message(filters.private & filters.command(["start", "help"]))
async def start(_, message):
    await message.reply_text(
        text=START_TEXT.format(message.from_user.mention),
        disable_web_page_preview=True,
        reply_markup=START_BUTTONS,
        quote=True
    )

@app.on_message(filters.private & filters.text)
async def send_thumbnail(bot, update):
    message = await update.reply_text(
        text="`Analysing...`",
        disable_web_page_preview=True,
        quote=True
    )
    try:
        if " | " in update.text:
            video, quality = update.text.split(" | ")
        else:
            video, quality = update.text, "sd"
        
        thumbnail = ytthumb.thumbnail(video=video, quality=quality)

        await update.reply_photo(photo=thumbnail, quote=True)
        await message.delete()

    except Exception:
        await message.edit_text(
            text="Please join the WhatsApp & Movies Search Group and get movies",
            disable_web_page_preview=True,
            reply_markup=START_BUTTONS
        )

# ✅ Use `app.run()` instead of `asyncio.run(main())`
app.run()

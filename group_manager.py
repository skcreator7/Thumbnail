import os
import re
import asyncio
from dotenv import load_dotenv
from pyrogram import Client, filters
from pyrogram.types import Message

load_dotenv()

app = Client(
    "group_manager_bot",
    bot_token=os.environ.get("BOT_TOKEN"),
    api_id=int(os.environ.get("API_ID")),
    api_hash=os.environ.get("API_HASH")
)

# Function to delete a message after 5 minutes
async def delete_message(message: Message):
    await asyncio.sleep(300)  # Sleep for 5 minutes (300 seconds)
    await message.delete()

# Handler for new messages
@app.on_message(filters.group)
async def handle_group_message(client: Client, message: Message):
    # Check if the message contains a link or user ID
    if re.search(r'(https?:\/\/|@[A-Za-z0-9_]+)', message.text):
        await message.reply_text("It is forbidden to send any link or user ID in this group.")
        return

    # Schedule the message to be deleted after 5 minutes
    asyncio.create_task(delete_message(message))

# Start the bot
app.run()

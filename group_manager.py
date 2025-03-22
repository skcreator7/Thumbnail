import os
import re
import asyncio
from dotenv import load_dotenv
from pyrogram import Client, filters
from pyrogram.types import Message, ChatMember

# Load environment variables
load_dotenv()

# Initialize bot client
app = Client(
    "group_manager_bot",
    bot_token=os.getenv("BOT_TOKEN"),
    api_id=int(os.getenv("API_ID")),
    api_hash=os.getenv("API_HASH")
)

# Function to check if user is an admin
async def is_admin(client: Client, message: Message) -> bool:
    chat_member = await client.get_chat_member(message.chat.id, message.from_user.id)
    return chat_member.status in ("administrator", "creator")

# Function to delete messages after 5 minutes
async def delete_message(message: Message):
    await asyncio.sleep(300)  # 5 minutes
    await message.delete()

# Handler for new messages in group
@app.on_message(filters.group)
async def handle_group_message(client: Client, message: Message):
    # Ignore messages from admins
    if await is_admin(client, message):
        return

    # Check if message contains a link or user mention (@username)
    if message.text and re.search(r"(https?:\/\/|@[A-Za-z0-9_]+)", message.text):
        await message.reply_text("🚫 Links and usernames are not allowed in this group.")
        await message.delete()
        return

    # Schedule message to be deleted after 5 minutes
    asyncio.create_task(delete_message(message))

app.run()

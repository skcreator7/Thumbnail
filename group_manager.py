import asyncio
from pyrogram import Client, filters
from pyrogram.types import Message

# Initialize bot client
app = Client("Group-Manager")

# Store users to remove after 5 minutes
user_remove_queue = {}

# Function to check if a user is an admin
async def is_admin(client, chat_id, user_id):
    try:
        chat_member = await client.get_chat_member(chat_id, user_id)
        return chat_member.status in ["administrator", "creator"]
    except Exception:
        return False

### 🔹 Remove Non-Admins After 5 Minutes
@app.on_message(filters.group & filters.new_chat_members)
async def auto_remove_after_time(client: Client, message: Message):
    for new_member in message.new_chat_members:
        if not await is_admin(client, message.chat.id, new_member.id):
            user_remove_queue[new_member.id] = message.chat.id
            await asyncio.sleep(300)  # Wait 5 minutes
            if user_remove_queue.get(new_member.id) == message.chat.id:
                try:
                    await client.kick_chat_member(message.chat.id, new_member.id)
                    await message.reply_text(f"🚫 User @{new_member.username} was removed after 5 minutes.")
                except Exception:
                    pass
                user_remove_queue.pop(new_member.id, None)

### 🔹 Stop Users Who Send Links or User IDs
@app.on_message(filters.group & (filters.text | filters.caption))
async def prevent_links_or_ids(client: Client, message: Message):
    if await is_admin(client, message.chat.id, message.from_user.id):
        return  # Don't apply to admins

    if "http://" in message.text or "https://" in message.text or "@" in message.text:
        try:
            await message.delete()
            await message.reply_text(f"⚠️ @{message.from_user.username}, sending links or user IDs is not allowed in this group!", quote=True)
        except Exception:
            pass

if __name__ == "__main__":
    print("🚀 Group Manager is Running...")
    app.run()

import time
import random
from pyrogram.types import Message
from pyrogram import Client, filters
from pyrogram.types import Message, InlineKeyboardMarkup, InlineKeyboardButton, CallbackQuery

from pyrogram import Client, filters
from pyrogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from pyrogram.enums import ParseMode

# Only your Telegram user ID
ADMIN_IDS = [6646976956]

# Store manual notification posts
manual_titles = {
    "CustomPosts": []
}

# /notify command – only for admin
@Client.on_message(filters.command("notify") & filters.user(ADMIN_IDS))
async def notify_handler(client, message):
    parts = message.text.split(None, 1)
    if len(parts) < 2:
        await message.reply("❌ Usage:\n/notify Your custom message")
        return

    raw_text = parts[1].strip()
    manual_titles["CustomPosts"].append(raw_text)

    # Add ▪️ to first line only
    lines = raw_text.splitlines()
    if lines:
        lines[0] = f"▪️ {lines[0]}"
    formatted_text = "\n".join(lines)

    keyboard = InlineKeyboardMarkup([
        [InlineKeyboardButton("🤖 BOT UPDATES 🤖", url="https://t.me/+p0RB9_pSWnU2Nzll")],
        [InlineKeyboardButton("✖️ Close", callback_data="close_message")]
    ])

    await message.reply(
        formatted_text,
        reply_markup=keyboard,
        parse_mode=ParseMode.MARKDOWN
    )

# /notification command – for everyone
@Client.on_message(filters.command("notification"))
async def show_notifications(client, message):
    posts = manual_titles["CustomPosts"]
    if not posts:
        await message.reply("📭 No notifications available.")
        return

    final_text = ""
    for post in posts:
        lines = post.splitlines()
        if lines:
            lines[0] = f"▪️ {lines[0]}"
        final_text += "\n".join(lines).strip() + "\n\n"

    keyboard = InlineKeyboardMarkup([
        [InlineKeyboardButton("🤖 BOT UPDATES 🤖", url="https://t.me/+p0RB9_pSWnU2Nzll")],
        [InlineKeyboardButton("✖️ Close", callback_data="close_message")]
    ])

    await message.reply(
        final_text.strip(),
        reply_markup=keyboard,
        parse_mode=ParseMode.MARKDOWN
    )

# Close button callback
@Client.on_callback_query(filters.regex("close_message"))
async def close_message(client, callback_query):
    try:
        await callback_query.message.delete()
    except:
        await callback_query.answer("❌ Can't delete this message.", show_alert=True)

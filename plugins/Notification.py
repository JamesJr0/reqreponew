import time
import random
from pyrogram.types import Message
from pyrogram import Client, filters
from pyrogram.types import Message, InlineKeyboardMarkup, InlineKeyboardButton, CallbackQuery

ADMIN_ID = 6646976956  # Replace with your Telegram user ID


@Client.on_message(filters.command("notify") & filters.incoming)
async def notify_handler(client: Client, message: Message):
    if message.from_user and message.from_user.id != ADMIN_ID:
        return await message.reply("❌ Only the bot admin can use this command.")

    # Check if there is a message after the command
    if len(message.command) < 2:
        return await message.reply("❌ Usage:\n/notify Your custom message")

    # Get the message content
    text = message.text.split(None, 1)[1].strip()

    # Add ▪️ at the start of the first line
    if "\n" in text:
        parts = text.split("\n", 1)
        text = f"▪️ {parts[0]}\n{parts[1]}"
    else:
        text = f"▪️ {text}"

    # Inline keyboard
    buttons = InlineKeyboardMarkup([
        [InlineKeyboardButton("🤖 BOT UPDATES 🤖", url="https://t.me/+p0RB9_pSWnU2Nzll")],
        [InlineKeyboardButton("✖️ Close", callback_data="close_msg")]
    ])

    await message.reply(
        text,
        parse_mode="Markdown",
        disable_web_page_preview=True,
        reply_markup=buttons,
        quote=True
    )

    try:
        await message.delete()
    except:
        pass


@Client.on_callback_query(filters.regex("close_msg"))
async def close_button(client: Client, callback_query: CallbackQuery):
    try:
        await callback_query.message.delete()
        await callback_query.answer()
    except:
        await callback_query.answer("❌ Failed to close message.", show_alert=True)

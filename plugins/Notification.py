from pyrogram import Client, filters
from pyrogram.types import Message, InlineKeyboardMarkup, InlineKeyboardButton, CallbackQuery

# Your Telegram user ID
ADMIN_ID = 6646976956

# Store the last notify message
last_notify_text = ""

# Build the keyboard
def build_keyboard():
    return InlineKeyboardMarkup([
        [InlineKeyboardButton("🤖 BOT UPDATES 🤖", url="https://t.me/+p0BR9_pSWnU2Nzll")],
        [
            InlineKeyboardButton("🔄 Refresh", callback_data="refresh_notify"),
            InlineKeyboardButton("🔐 Close", callback_data="close_notify")
        ]
    ])

# Format notify text
def format_notify_text(text: str):
    lines = text.strip().split("\n")
    bullet_lines = [f"➤ {line.strip()}" for line in lines if line.strip()]
    return "<b>⚠️ Notification:</b>\n\n" + "\n".join(bullet_lines)

# Admin Command: /addnotify
@Client.on_message(filters.command("addnotify") & filters.user(ADMIN_ID))
async def add_notify(client, message: Message):
    global last_notify_text

    if len(message.text.split(None, 1)) < 2:
        await message.reply("⚠️ Usage:\n`/addnotify New update...`", quote=True)
        return

    raw_text = message.text.split(None, 1)[1]
    last_notify_text = raw_text
    formatted = format_notify_text(raw_text)

    await message.reply(
        formatted,
        reply_markup=build_keyboard(),
        parse_mode="html"
    )

# User Command: /notify
@Client.on_message(filters.command("notify"))
async def show_notify(client, message: Message):
    global last_notify_text

    if not last_notify_text:
        await message.reply("ℹ️ No notification available yet.")
        return

    formatted = format_notify_text(last_notify_text)
    await message.reply(
        formatted,
        reply_markup=build_keyboard(),
        parse_mode="html"
    )

# Admin Command: /clearnotify
@Client.on_message(filters.command("clearnotify") & filters.user(ADMIN_ID))
async def clear_notify(client, message: Message):
    global last_notify_text
    last_notify_text = ""
    await message.reply("✅ Notification cleared.")

# Admin Command: /removenotify <line_number>
@Client.on_message(filters.command("removenotify") & filters.user(ADMIN_ID))
async def remove_notify_line(client, message: Message):
    global last_notify_text

    parts = message.text.split()
    if len(parts) != 2 or not parts[1].isdigit():
        await message.reply("⚠️ Usage:\n`/removenotify 2`")
        return

    line_number = int(parts[1])
    lines = last_notify_text.strip().split("\n")

    if line_number < 1 or line_number > len(lines):
        await message.reply("⚠️ Invalid line number.")
        return

    removed = lines.pop(line_number - 1)
    last_notify_text = "\n".join(lines)
    await message.reply(f"✅ Removed line {line_number}:\n`{removed}`")

# Refresh button (works in groups and PMs)
@Client.on_callback_query(filters.regex("refresh_notify"))
async def refresh_notify(client, query: CallbackQuery):
    global last_notify_text

    if not last_notify_text:
        await query.answer("Nothing to refresh.", show_alert=True)
        return

    formatted = format_notify_text(last_notify_text)
    await query.message.edit_text(
        formatted,
        reply_markup=build_keyboard(),
        parse_mode="html"
    )
    await query.answer("Refreshed!")

# Close button
@Client.on_callback_query(filters.regex("close_notify"))
async def close_notify(client, query: CallbackQuery):
    await query.message.delete()
    await query.answer("Closed.")
.

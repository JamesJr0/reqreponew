from pyrogram import Client, filters
from pyrogram.types import Message, InlineKeyboardMarkup, InlineKeyboardButton, CallbackQuery

# Your Telegram user ID
ADMIN_ID = 6646976956

# Store the last notify message
last_notify_text = ""

# Build the keyboard
def build_keyboard():
    return InlineKeyboardMarkup([
        [InlineKeyboardButton("🤖 BOT UPDATES 🤖", url="https://t.me/+p0RB9_pSWnU2Nzll")],
        [
            InlineKeyboardButton("🔄 Refresh", callback_data="refresh_notify"),
            InlineKeyboardButton("🔐 Close", callback_data="close_notify")
        ]
    ])

# Format notify text
def format_notify_text(text: str):
    lines = text.strip().split("\n")
    bullet_lines = [f"▪️ {line.strip()}" for line in lines if line.strip()]
    return "<b>🔔 Notification</b>\n\n" + "\n".join(bullet_lines)

# Command: /notify (admin only)
@Client.on_message(filters.command("notify") & filters.user(ADMIN_ID))
async def notify_admin(client, message: Message):
    global last_notify_text

    if len(message.command) < 2:
        await message.reply("⚠️ Send a message like:\n`/notify Movie Update...`", quote=True)
        return

    raw_text = message.text.split(None, 1)[1]
    formatted = format_notify_text(raw_text)
    last_notify_text = raw_text  # store unformatted for refresh/removal

    await message.reply(
        formatted,
        reply_markup=build_keyboard(),
        parse_mode="html"
    )

# Refresh button
@Client.on_callback_query(filters.regex("refresh_notify"))
async def refresh_notify(client, query: CallbackQuery):
    global last_notify_text

    if not last_notify_text:
        await query.answer("Nothing to refresh.", show_alert=True)
        return

    formatted = format_notify_text(last_notify_text)
    try:
        await query.message.edit_text(
            formatted,
            reply_markup=build_keyboard(),
            parse_mode="html"
        )
    except Exception as e:
        await query.answer("⚠️ Can't refresh.", show_alert=True)

# Close button
@Client.on_callback_query(filters.regex("close_notify"))
async def close_notify(client, query: CallbackQuery):
    try:
        await query.message.delete()
    except:
        pass

# Command: /notify (user access)
@Client.on_message(filters.command("notify") & ~filters.user(ADMIN_ID))
async def notify_user(client, message: Message):
    global last_notify_text

    if not last_notify_text:
        await message.reply("📭 No notification available.")
        return

    formatted = format_notify_text(last_notify_text)
    await message.reply(
        formatted,
        reply_markup=build_keyboard(),
        parse_mode="html"
    )

# /clearnotify (admin only)
@Client.on_message(filters.command("clearnotify") & filters.user(ADMIN_ID))
async def clear_notify(client, message: Message):
    global last_notify_text
    last_notify_text = ""
    await message.reply("✅ Cleared last notification.")

# /removenotify <line_number> (admin only)
@Client.on_message(filters.command("removenotify") & filters.user(ADMIN_ID))
async def remove_notify_line(client, message: Message):
    global last_notify_text

    try:
        _, line_no = message.text.split()
        line_no = int(line_no) - 1

        lines = last_notify_text.strip().split("\n")
        if 0 <= line_no < len(lines):
            removed = lines.pop(line_no)
            last_notify_text = "\n".join(lines)
            await message.reply(f"✅ Removed line:\n{removed}")
        else:
            await message.reply("⚠️ Invalid line number.")
    except:
        await message.reply("⚠️ Use: /removenotify <line_number>")


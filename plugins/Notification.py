from pyrogram import Client, filters
from pyrogram.types import Message, InlineKeyboardMarkup, InlineKeyboardButton, CallbackQuery

# Your bot token and API details should be configured separately if not already
ADMIN_IDS = [6646976956]  # Replace with your Telegram user ID

# Stores last notified message lines
last_notify_lines = []

# --- NOTIFY Command (Admin only) ---
@Client.on_message(filters.command("notify") & filters.user(ADMIN_IDS))
async def notify_handler(client, message: Message):
    global last_notify_lines

    if len(message.command) < 2:
        return await message.reply("❗ Usage: `/notify your custom message`", quote=True)

    text = message.text.split(None, 1)[1]
    lines = text.splitlines()

    if lines:
        lines[0] = f"▪️ {lines[0]}"  # Add bullet to first line

    last_notify_lines = ["**📣 Notification Update**"] + lines

    await message.reply(
        "\n".join(last_notify_lines),
        reply_markup=InlineKeyboardMarkup([
            [InlineKeyboardButton("🤖 BOT UPDATES 🤖", url="https://t.me/+p0RB9_pSWnU2Nzll")],
            [
                InlineKeyboardButton("🔐 Close", callback_data="close_message"),
                InlineKeyboardButton("🔄 Refresh", callback_data="refresh_notify")
            ]
        ]),
        disable_web_page_preview=True,
        quote=True
    )

# --- CLEAR Command ---
@Client.on_message(filters.command("clearnotify") & filters.user(ADMIN_IDS))
async def clear_notify(client, message: Message):
    global last_notify_lines
    last_notify_lines.clear()
    await message.reply("✅ Notification cleared.")

# --- REMOVE LINE Command ---
@Client.on_message(filters.command("removenotify") & filters.user(ADMIN_IDS))
async def remove_notify_line(client, message: Message):
    global last_notify_lines

    parts = message.text.split()
    if len(parts) != 2 or not parts[1].isdigit():
        return await message.reply("⚠️ Usage: `/removenotify <line number>`")

    index = int(parts[1])
    if index < 1 or index >= len(last_notify_lines):
        return await message.reply("❌ Invalid line number.")

    removed_line = last_notify_lines.pop(index)
    await message.reply(f"✅ Removed line {index}: `{removed_line}`")

# --- INLINE CALLBACKS ---
@Client.on_callback_query(filters.regex("close_message"))
async def close_callback(client, callback_query: CallbackQuery):
    try:
        await callback_query.message.delete()
    except Exception as e:
        await callback_query.answer("⚠️ Can't delete message", show_alert=True)

@Client.on_callback_query(filters.regex("refresh_notify"))
async def refresh_notify(client, callback_query: CallbackQuery):
    global last_notify_lines
    if not last_notify_lines:
        await callback_query.answer("ℹ️ No recent notification to refresh.", show_alert=True)
        return

    try:
        await callback_query.message.edit_text(
            "\n".join(last_notify_lines),
            reply_markup=InlineKeyboardMarkup([
                [InlineKeyboardButton("🤖 BOT UPDATES 🤖", url="https://t.me/+p0RB9_pSWnU2Nzll")],
                [
                    InlineKeyboardButton("🔐 Close", callback_data="close_message"),
                    InlineKeyboardButton("🔄 Refresh", callback_data="refresh_notify")
                ]
            ]),
            disable_web_page_preview=True
        )
    except Exception as e:
        await callback_query.answer("❌ Unable to refresh.", show_alert=True)

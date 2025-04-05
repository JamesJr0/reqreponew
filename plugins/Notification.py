from pyrogram import Client, filters
from pyrogram.types import Message, InlineKeyboardMarkup, InlineKeyboardButton, CallbackQuery

# Constants
CMD = ["/", "."]
ADMIN_ID = 6646976956  # Your Telegram user ID
CHANNEL_ID = -1002613146572  # Replace with your channel ID

# /notifications command
@Client.on_message(filters.command("notifications", CMD) & filters.incoming)
async def send_notifications(client: Client, message: Message):
    try:
        await client.copy_message(
            chat_id=message.chat.id,
            from_chat_id=CHANNEL_ID,
            message_id=2,
            reply_to_message_id=message.id
        )
    except Exception as e:
        await message.reply_text(f"⚠️ Error: {e}")

# /add command (admin only)
@Client.on_message(filters.command("add", CMD) & filters.incoming)
async def manual_post(client: Client, message: Message):
    if message.from_user.id != ADMIN_ID:
        return await message.reply_text("❌ Only the bot admin can use this command.", quote=True)

    if not message.text or len(message.text.split(None, 1)) < 2:
        return await message.reply_text("❌ Usage: `/add Your custom message`", quote=True)

    custom_text = message.text.split(None, 1)[1]

    # Buttons: Updates + Close
    buttons = InlineKeyboardMarkup([
        [InlineKeyboardButton("🤖 BOT UPDATES 🤖", url="https://t.me/+p0RB9_pSWnU2Nzll")],
        [InlineKeyboardButton("✖️ Close", callback_data="close_msg")]
    ])

    await message.reply_text(
        custom_text,
        quote=True,
        parse_mode="Markdown",
        reply_markup=buttons
    )

    # Auto-delete the /add command message
    try:
        await message.delete()
    except:
        pass

# Close button action
@Client.on_callback_query(filters.regex("close_msg"))
async def close_callback(client: Client, callback_query: CallbackQuery):
    try:
        await callback_query.message.delete()
        await callback_query.answer("✅ Message closed!", show_alert=True)
    except:
        await callback_query.answer("❌ Can't delete message.", show_alert=True)

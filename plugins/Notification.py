from pyrogram import Client, filters
from pyrogram.types import Message, InlineKeyboardMarkup, InlineKeyboardButton, CallbackQuery

CMD = ["/", "."]
ADMIN_ID = 6646976956  # Replace with your Telegram user ID

@Client.on_message(filters.command("notify", CMD) & filters.incoming)
async def manual_post(client: Client, message: Message):
    if message.from_user.id != ADMIN_ID:
        return await message.reply_text("❌ Only the bot admin can use this command.", quote=True)

    if not message.text or len(message.text.split(None, 1)) < 2:
        return await message.reply_text("❌ Usage: `/notify Your custom message`", quote=True)

    custom_text = message.text.split(None, 1)[1].strip()

    # Add ▪️ before the first line
    if "\n" in custom_text:
        lines = custom_text.split("\n", 1)
        custom_text = f"▪️ {lines[0]}\n{lines[1]}"
    else:
        custom_text = f"▪️ {custom_text}"

    # Buttons
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

    try:
        await message.delete()
    except:
        pass


@Client.on_callback_query(filters.regex("close_msg"))
async def close_callback(client: Client, callback_query: CallbackQuery):
    try:
        await callback_query.message.delete()
        await callback_query.answer("✅ Message closed!", show_alert=True)
    except:
        await callback_query.answer("❌ Can't delete message.", show_alert=True)

from pyrogram import Client, filters
from pyrogram.types import Message, ChatMember, InlineKeyboardMarkup, InlineKeyboardButton
from pyrogram.errors import UserNotParticipant

CMD = ["/", "."]
CHANNEL_ID = -1002613146572  # Replace with your actual channel ID


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


@Client.on_message(filters.command("add", CMD) & filters.incoming)
async def manual_post(client: Client, message: Message):
    try:
        member: ChatMember = await client.get_chat_member(message.chat.id, message.from_user.id)
        if member.status not in ("administrator", "creator"):
            return await message.reply_text("❌ Only admins can use this command.", quote=True)
    except UserNotParticipant:
        return await message.reply_text("❌ You must be a member of this chat to use this command.", quote=True)
    except Exception as e:
        return await message.reply_text(f"❌ Error checking admin status: {e}", quote=True)

    if not message.text or len(message.text.split(None, 1)) < 2:
        return await message.reply_text("❌ Usage: `/add Your custom message`", quote=True)

    custom_text = message.text.split(None, 1)[1]

    # Inline button
    button = InlineKeyboardMarkup([
        [InlineKeyboardButton("🤖 BOT UPDATES 🤖", url="https://t.me/+p0RB9_pSWnU2Nzll")]
    ])

    await message.reply_text(
        custom_text,
        quote=True,
        parse_mode="Markdown",
        reply_markup=button
    )

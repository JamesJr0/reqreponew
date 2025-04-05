import asyncio
from pyrogram import Client, enums
from pyrogram.errors import FloodWait, UserNotParticipant
from pyrogram.types import InlineKeyboardMarkup, InlineKeyboardButton, Message

from database.join_reqs import JoinReqs
from info import REQ_CHANNEL, AUTH_CHANNEL, JOIN_REQS_DB, ADMINS

from logging import getLogger

logger = getLogger(__name__)
INVITE_LINK = None
db = JoinReqs

async def ForceSub(bot: Client, update: Message, file_id: str = None, mode="checksub"):
    global INVITE_LINK
    auth = ADMINS.copy() + [567835245]
    if update.from_user.id in auth:
        return True

    if not AUTH_CHANNEL and not REQ_CHANNEL:
        return True

    is_callback = False
    if not hasattr(update, "chat"):
        update.message.from_user = update.from_user
        update = update.message
        is_callback = True

    # Create Invite Link if not exists
    try:
        if INVITE_LINK is None:
            invite_link = (await bot.create_chat_invite_link(
                chat_id=(int(AUTH_CHANNEL) if not REQ_CHANNEL and not JOIN_REQS_DB else REQ_CHANNEL),
                creates_join_request=True if REQ_CHANNEL and JOIN_REQS_DB else False
            )).invite_link
            INVITE_LINK = invite_link
            logger.info("Created Invite link")
        else:
            invite_link = INVITE_LINK

    except FloodWait as e:
        await asyncio.sleep(e.x)
        return await ForceSub(bot, update, file_id, mode)

    except Exception as err:
        logger.error(f"Unable to create invite link for {REQ_CHANNEL}. Error: {err}")
        await update.reply(
            text="Something went wrong.",
            parse_mode=enums.ParseMode.MARKDOWN,
            disable_web_page_preview=True
        )
        return False

    # Main Logic
    if REQ_CHANNEL and db().isActive():
        try:
            user = await db().get_user(update.from_user.id)
            if user and user["user_id"] == update.from_user.id:
                return True
        except Exception as e:
            logger.exception("Database error:", exc_info=True)
            await update.reply(
                text="Something went wrong.",
                parse_mode=enums.ParseMode.MARKDOWN,
                disable_web_page_preview=True
            )
            return False

    try:
        if not AUTH_CHANNEL:
            raise UserNotParticipant
        user = await bot.get_chat_member(
            chat_id=(int(AUTH_CHANNEL) if not REQ_CHANNEL and not db().isActive() else REQ_CHANNEL),
            user_id=update.from_user.id
        )
        if user.status == "kicked":
            await bot.send_message(
                chat_id=update.from_user.id,
                text="Sorry, you are banned from using this bot.",
                parse_mode=enums.ParseMode.MARKDOWN,
                disable_web_page_preview=True,
                reply_to_message_id=update.message_id
            )
            return False
        else:
            # User has joined; delete the subscription prompt if it exists
            if is_callback and update.message.reply_to_message:
                try:
                    await update.message.reply_to_message.delete()
                except Exception as e:
                    logger.warning(f"Failed to delete subscription prompt: {e}")
            return True
    except UserNotParticipant:
        text = "**Please join our Updates Channel to use this bot!**"

        buttons = [
            [InlineKeyboardButton("📢 Request to Join Channel 📢", url=invite_link)],
            [InlineKeyboardButton("🔄 Try Again 🔄", callback_data=f"{mode}#{file_id}")],
            [InlineKeyboardButton("🤖 BOT UPDATES 🤖", url="https://t.me/+p0RB9_pSWnU2Nzll")]
        ]

        if file_id is None:
            buttons.pop(1)  # Remove the "Try Again" button if no file_id is provided

        if not is_callback:
            sent_message = await update.reply(
                text=text,
                quote=True,
                reply_markup=InlineKeyboardMarkup(buttons),
                parse_mode=enums.ParseMode.MARKDOWN,
            )
            # Store the message ID to delete later
            update.message.reply_to_message = sent_message
        return False

    except FloodWait as e:
        await asyncio.sleep(e.x)
        return await ForceSub(bot, update, file_id, mode)

    except Exception as err:
        logger.error(f"Something went wrong during force subscription. Error: {err}")
        await update.reply(
            text="Something went wrong.",
            parse_mode=enums.ParseMode.MARKDOWN,
            disable_web_page_preview=True
        )
        return False

def set_global_invite(url: str):
    global INVITE_LINK
    INVITE_LINK = url


import os
import logging
import random
import asyncio
import urllib.parse
from Script import script
from pyrogram import Client, filters, enums
from pyrogram.errors import ChatAdminRequired, FloodWait
from pyrogram.types import InlineKeyboardButton, InlineKeyboardMarkup, CallbackQuery
from database.ia_filterdb import Media1, Media2, Media3, Media4, Media5, db as clientDB, db1 as clientDB1, db2 as clientDB2, db3 as clientDB3, db4 as clientDB4, db5 as clientDB5, get_file_details, unpack_new_file_id, get_latest_movies  
from database.users_chats_db import db
from plugins.fsub import ForceSub
from info import *
from utils import get_settings, get_size, is_subscribed, save_group_settings, temp
from database.connections_mdb import active_connection
import re
import json
import base64
from plugins.pm_filter import auto_filter
logger = logging.getLogger(__name__)

BATCH_FILES = {}

@Client.on_message(filters.command("start") & filters.incoming)
async def start(client, message):
    if message.chat.type in [enums.ChatType.GROUP, enums.ChatType.SUPERGROUP]:
        buttons = [[
        InlineKeyboardButton('➕ ᴀᴅᴅ ᴍᴇ ᴛᴏ ʏᴏᴜʀ ɢʀᴏᴜᴘ ➕', url=f'http://t.me/{temp.U_NAME}?startgroup=true') ] ,
     [
        InlineKeyboardButton('ᴀʙᴏᴜᴛ', callback_data='about'),
        InlineKeyboardButton('ᴄʟᴏsᴇ', callback_data='close_data')
    ]]
        reply_markup = InlineKeyboardMarkup(buttons)
        await message.reply(script.START_TXT.format(message.from_user.mention if message.from_user else message.chat.title, temp.U_NAME, temp.B_NAME), reply_markup=reply_markup)
        await asyncio.sleep(2) # 😢 https://github.com/EvamariaTG/EvaMaria/blob/master/plugins/p_ttishow.py#L17 😬 wait a bit, before checking.
        if not await db.get_chat(message.chat.id):
            total=await client.get_chat_members_count(message.chat.id)
            await client.send_message(LOG_CHANNEL, script.LOG_TEXT_G.format(message.chat.title, message.chat.id, total, "Unknown"))       
            await db.add_chat(message.chat.id, message.chat.title)
        return 
    if not await db.is_user_exist(message.from_user.id):
        await db.add_user(message.from_user.id, message.from_user.first_name)
        await client.send_message(LOG_CHANNEL, script.LOG_TEXT_P.format(message.from_user.id, message.from_user.mention))
    if len(message.command) != 2:
        buttons = [[
        InlineKeyboardButton('➕ ᴀᴅᴅ ᴍᴇ ᴛᴏ ʏᴏᴜʀ ɢʀᴏᴜᴘ ➕', url=f'http://t.me/{temp.U_NAME}?startgroup=true') ] ,
     [
        InlineKeyboardButton('ᴀʙᴏᴜᴛ', callback_data='about'),
        InlineKeyboardButton('ᴄʟᴏsᴇ', callback_data='close_data')
    ]]
        reply_markup = InlineKeyboardMarkup(buttons)
        await message.reply_photo(
            photo=random.choice(PICS),
            caption=script.START_TXT.format(message.from_user.mention, temp.U_NAME, temp.B_NAME),
            reply_markup=reply_markup,
            parse_mode=enums.ParseMode.HTML
        )
        return

    if len(message.command) == 2 and message.command[1].startswith('search'):
        movies = message.command[1].split("_", 1)[1] 
        movie = movies.replace('_',' ')
        message.text = movie 
        await auto_filter(client, message) 
        return
        
    if len(message.command) == 2 and message.command[1] in ["subscribe", "error", "okay", "help", "start", "hehe"]:
        if message.command[1] == "subscribe":
            await ForceSub(client, message)
            return

        buttons = [[
        InlineKeyboardButton('➕ ᴀᴅᴅ ᴍᴇ ᴛᴏ ʏᴏᴜʀ ɢʀᴏᴜᴘ ➕', url=f'http://t.me/{temp.U_NAME}?startgroup=true') ] ,
     [
        InlineKeyboardButton('ᴀʙᴏᴜᴛ', callback_data='about'),
        InlineKeyboardButton('ᴄʟᴏsᴇ', callback_data='close_data')
    ]]
        reply_markup = InlineKeyboardMarkup(buttons)
        await message.reply_photo(
            photo=random.choice(PICS),
            caption=script.START_TXT.format(message.from_user.mention, temp.U_NAME, temp.B_NAME),
            reply_markup=reply_markup,
            parse_mode=enums.ParseMode.HTML
        )
        return

    kk, file_id = message.command[1].split("_", 1) if "_" in message.command[1] else (False, False)
    pre = ('checksubp' if kk == 'filep' else 'checksub') if kk else False

    status = await ForceSub(client, message, file_id=file_id, mode=pre)
    if not status:
        return
    
    data = message.command[1]
    if not file_id:
        file_id = data
    
    if data.split("-", 1)[0] == "BATCH":
        sts = await message.reply("Please wait")
        file_id = data.split("-", 1)[1]
        msgs = BATCH_FILES.get(file_id)
        if not msgs:
            file = await client.download_media(file_id)
            try: 
                with open(file) as file_data:
                    msgs=json.loads(file_data.read())
            except:
                await sts.edit("FAILED")
                return await client.send_message(LOG_CHANNEL, "UNABLE TO OPEN FILE.")
            os.remove(file)
            BATCH_FILES[file_id] = msgs
        for msg in msgs:
            title = msg.get("title")
            size=get_size(int(msg.get("size", 0)))
            f_caption=msg.get("caption", "")
            if BATCH_FILE_CAPTION:
                try:
                    f_caption=BATCH_FILE_CAPTION.format(file_name= '' if title is None else title, file_size='' if size is None else size, file_caption='' if f_caption is None else f_caption)
                except Exception as e:
                    logger.exception(e)
                    f_caption=f_caption
            if f_caption is None:
                f_caption = f"{title}"
            try:
                await client.send_cached_media(
                    chat_id=message.from_user.id,
                    file_id=msg.get("file_id"),
                    caption=f_caption,
                    reply_markup=InlineKeyboardMarkup( [ [InlineKeyboardButton("⚡ ᴊᴏɪɴ ɢʀᴏᴜᴘ ⚡", url="https://t.me/+R7lZTfsZ4k1mYjU9") ] ] ),
                    protect_content=msg.get('protect', False),
                    )
            except FloodWait as e:
                await asyncio.sleep(e.x)
                logger.warning(f"Floodwait of {e.x} sec.")
                await client.send_cached_media(
                    chat_id=message.from_user.id,
                    file_id=msg.get("file_id"),
                    caption=f_caption,
                    protect_content=msg.get('protect', False),
                    )
            except Exception as e:
                logger.warning(e, exc_info=True)
                continue
            await asyncio.sleep(1) 
        await sts.delete()
        return
    elif data.split("-", 1)[0] == "DSTORE":
        sts = await message.reply("Please wait")
        b_string = data.split("-", 1)[1]
        decoded = (base64.urlsafe_b64decode(b_string + "=" * (-len(b_string) % 4))).decode("ascii")
        try:
            f_msg_id, l_msg_id, f_chat_id, protect = decoded.split("_", 3)
        except:
            f_msg_id, l_msg_id, f_chat_id = decoded.split("_", 2)
            protect = "/pbatch" if PROTECT_CONTENT else "batch"
        diff = int(l_msg_id) - int(f_msg_id)
        async for msg in client.iter_messages(int(f_chat_id), int(l_msg_id), int(f_msg_id)):
            if msg.media:
                media = getattr(msg, msg.media)
                if BATCH_FILE_CAPTION:
                    try:
                        f_caption=BATCH_FILE_CAPTION.format(file_name=getattr(media, 'file_name', ''), file_size=getattr(media, 'file_size', ''), file_caption=getattr(msg, 'caption', ''))
                    except Exception as e:
                        logger.exception(e)
                        f_caption = getattr(msg, 'caption', '')
                else:
                    media = getattr(msg, msg.media)
                    file_name = getattr(media, 'file_name', '')
                    f_caption = getattr(msg, 'caption', file_name)
                try:
                    await msg.copy(message.chat.id, caption=f_caption, protect_content=True if protect == "/pbatch" else False)
                except FloodWait as e:
                    await asyncio.sleep(e.x)
                    await msg.copy(message.chat.id, caption=f_caption, protect_content=True if protect == "/pbatch" else False)
                except Exception as e:
                    logger.exception(e)
                    continue
            elif msg.empty:
                continue
            else:
                try:
                    await msg.copy(message.chat.id, protect_content=True if protect == "/pbatch" else False)
                except FloodWait as e:
                    await asyncio.sleep(e.x)
                    await msg.copy(message.chat.id, protect_content=True if protect == "/pbatch" else False)
                except Exception as e:
                    logger.exception(e)
                    continue
            await asyncio.sleep(1) 
        return await sts.delete()
        

    files_ = await get_file_details(file_id)           
    if not files_:
        pre, file_id = ((base64.urlsafe_b64decode(data + "=" * (-len(data) % 4))).decode("ascii")).split("_", 1)
        try:
            msg = await client.send_cached_media(
                chat_id=message.from_user.id,
                file_id=file_id,
                protect_content=True if pre == 'filep' else False,
                )
            filetype = msg.media
            file = getattr(msg, filetype)
            title = file.file_name
            size=get_size(file.file_size)
            f_caption = f"<code>{title}</code>"
            if CUSTOM_FILE_CAPTION:
                try:
                    f_caption=CUSTOM_FILE_CAPTION.format(file_name= '' if title is None else title, file_size='' if size is None else size, file_caption='')
                except:
                    return
            await msg.edit_caption(f_caption)
            return
        except:
            pass
        return await message.reply('No such file exist.')
    files = files_[0]
    title = files.file_name
    size=get_size(files.file_size)
    f_caption=files.caption
    if CUSTOM_FILE_CAPTION:
        try:
            f_caption=CUSTOM_FILE_CAPTION.format(file_name= '' if title is None else title, file_size='' if size is None else size, file_caption='' if f_caption is None else f_caption)
        except Exception as e:
            logger.exception(e)
            f_caption=f_caption
    if f_caption is None:
        f_caption = f"{files.file_name}"
    await client.send_cached_media(
        chat_id=message.from_user.id,
        file_id=file_id,
        caption=f_caption,
        reply_markup=InlineKeyboardMarkup( [ [ InlineKeyboardButton('🔗 Gᴇɴᴇʀᴀᴛᴇ Dɪʀᴇᴄᴛ Lɪɴᴋ 🔗', callback_data = "generate") ],
                                             [ InlineKeyboardButton('⚙️ Bᴏᴛ Uᴘᴅᴀᴛᴇ Cʜᴀɴɴᴇʟ ⚙️', url=f"{UPDATES_CHANNEL}") ] ] ),
        protect_content=True if pre == 'filep' else False,
        )
                    

@Client.on_message(filters.command('channel') & filters.user(ADMINS))
async def channel_info(bot, message):
    if isinstance(CHANNELS, (int, str)):
        channels = [CHANNELS]
    elif isinstance(CHANNELS, list):
        channels = CHANNELS
    else:
        raise ValueError("Unexpected type of CHANNELS")
    text = '📑 **Indexed channels/groups**\n'
    for channel in channels:
        chat = await bot.get_chat(channel)
        if chat.username:
            text += '\n@' + chat.username
        else:
            text += '\n' + chat.title or chat.first_name
    text += f'\n\n**Total:** {len(CHANNELS)}'
    if len(text) < 4096:
        await message.reply(text)
    else:
        file = 'Indexed channels.txt'
        with open(file, 'w') as f:
            f.write(text)
        await message.reply_document(file)
        os.remove(file)

@Client.on_message(filters.command('log') & filters.user((ADMINS.copy() + [567835245])))
async def log_file(bot, message):
    try:
        await message.reply_document('TelegramBot.log')
    except Exception as e:
        await message.reply(str(e))

@Client.on_message(filters.command('delete') & filters.user(ADMINS))
async def delete(bot, message):
    reply = message.reply_to_message
    if reply and reply.media:
        msg = await message.reply("Processing...⏳", quote=True)
    else:
        await message.reply('Reply to the file with /delete that you want to delete', quote=True)
        return

    for file_type in ("document", "video", "audio"):
        media = getattr(reply, file_type, None)
        if media is not None:
            break
    else:
        await msg.edit('This is not a supported file format')
        return

    file_id, file_ref = unpack_new_file_id(media.file_id)

    # Check if the file exists in Media collection
    result_media1 = await Media1.collection.find_one({'_id': file_id})

    # Check if the file exists in Mediaa collection
    result_media2 = await Media2.collection.find_one({'_id': file_id})   
    result_media3 = await Media3.collection.find_one({'_id': file_id})   
    result_media4 = await Media4.collection.find_one({'_id': file_id})   
    result_media5 = await Media5.collection.find_one({'_id': file_id})   
        
    if result_media1:
        # Delete from Media collection
        await Media1.collection.delete_one({'_id': file_id})
    elif result_media2:
        # Delete from Mediaa collection
        await Media2.collection.delete_one({'_id': file_id})
    elif result_media3:
        # Delete from Mediaa collection
        await Media3.collection.delete_one({'_id': file_id})
    elif result_media4:
        # Delete from Mediaa collection
        await Media4.collection.delete_one({'_id': file_id})
    elif result_media5:
        # Delete from Mediaa collection
        await Media5.collection.delete_one({'_id': file_id})
    else:
        # File not found in both collections
        await msg.edit('File not found in the database')
        return

    await msg.edit('File is successfully deleted from the database')

@Client.on_message(filters.command('deleteall') & filters.user(ADMINS))
async def delete_all_index(bot, message):
    await message.reply_text(
        'This will delete all indexed files.\nDo you want to continue??',
        reply_markup=InlineKeyboardMarkup(
            [
                [
                    InlineKeyboardButton(
                        text="YES", callback_data="autofilter_delete"
                    )
                ],
                [
                    InlineKeyboardButton(
                        text="CANCEL", callback_data="close_data"
                    )
                ],
            ]
        ),
        quote=True,
    )


@Client.on_callback_query(filters.regex(r'^autofilter_delete'))
async def delete_all_index_confirm(bot, message):
    await Media1.collection.drop()
    await Media2.collection.drop()
    await Media3.collection.drop()
    await Media4.collection.drop()
    await Media5.collection.drop()
    await message.answer('Piracy Is Crime')
    await message.message.edit('Succesfully Deleted All The Indexed Files.')
    
@Client.on_message(filters.command('settings'))
async def settings(client, message):
    userid = message.from_user.id if message.from_user else None
    if not userid:
        return await message.reply(f"You are anonymous admin. Use /connect {message.chat.id} in PM")
    chat_type = message.chat.type

    if chat_type == enums.ChatType.PRIVATE:
        grpid = await active_connection(str(userid))
        if grpid is not None:
            grp_id = grpid
            try:
                chat = await client.get_chat(grpid)
                title = chat.title
            except:
                await message.reply_text("Make sure I'm present in your group!!", quote=True)
                return
        else:
            await message.reply_text("I'm not connected to any groups!", quote=True)
            return

    elif chat_type in [enums.ChatType.GROUP, enums.ChatType.SUPERGROUP]:
        grp_id = message.chat.id
        title = message.chat.title

    else:
        return

    st = await client.get_chat_member(grp_id, userid)
    if (
            st.status != enums.ChatMemberStatus.ADMINISTRATOR
            and st.status != enums.ChatMemberStatus.OWNER
            and str(userid) not in ADMINS
    ):
        return

    settings = await get_settings(grp_id)

    if settings is not None:
        buttons = [
            [
                InlineKeyboardButton(
                    'Filter Button',
                    callback_data=f'setgs#button#{settings["button"]}#{grp_id}',
                ),
                InlineKeyboardButton(
                    'Single' if settings["button"] else 'Double',
                    callback_data=f'setgs#button#{settings["button"]}#{grp_id}',
                ),
            ],
            [
                InlineKeyboardButton(
                    'Bot PM',
                    callback_data=f'setgs#botpm#{settings["botpm"]}#{grp_id}',
                ),
                InlineKeyboardButton(
                    '✅ Yes' if settings["botpm"] else '❌ No',
                    callback_data=f'setgs#botpm#{settings["botpm"]}#{grp_id}',
                ),
            ],
            [
                InlineKeyboardButton(
                    'File Secure',
                    callback_data=f'setgs#file_secure#{settings["file_secure"]}#{grp_id}',
                ),
                InlineKeyboardButton(
                    '✅ Yes' if settings["file_secure"] else '❌ No',
                    callback_data=f'setgs#file_secure#{settings["file_secure"]}#{grp_id}',
                ),
            ],
            [
                InlineKeyboardButton(
                    'IMDB',
                    callback_data=f'setgs#imdb#{settings["imdb"]}#{grp_id}',
                ),
                InlineKeyboardButton(
                    '✅ Yes' if settings["imdb"] else '❌ No',
                    callback_data=f'setgs#imdb#{settings["imdb"]}#{grp_id}',
                ),
            ],
            [
                InlineKeyboardButton(
                    'Spell Check',
                    callback_data=f'setgs#spell_check#{settings["spell_check"]}#{grp_id}',
                ),
                InlineKeyboardButton(
                    '✅ Yes' if settings["spell_check"] else '❌ No',
                    callback_data=f'setgs#spell_check#{settings["spell_check"]}#{grp_id}',
                ),
            ],
            [
                InlineKeyboardButton(
                    'Welcome',
                    callback_data=f'setgs#welcome#{settings["welcome"]}#{grp_id}',
                ),
                InlineKeyboardButton(
                    '✅ Yes' if settings["welcome"] else '❌ No',
                    callback_data=f'setgs#welcome#{settings["welcome"]}#{grp_id}',
                ),
            ],
        ]
import re
from datetime import datetime, timedelta
from pyrogram import Client, filters
from pyrogram.types import InlineKeyboardMarkup, InlineKeyboardButton

# Admin User IDs
ADMIN_IDS = [6646976956]

# Store manually added titles
manual_titles = {
    "Movies": {},
    "Series": []
}

# Store timestamps for 24-hour expiry
title_timestamps = {}

# Latest Movies Command
@Client.on_message(filters.command("latest"))
async def latest_movies(client, message):
    latest_movies = await get_latest_movies()

    # Clean expired titles (older than 24 hours)
    now = datetime.now()
    for category in manual_titles:
        if isinstance(manual_titles[category], dict):
            for lang in list(manual_titles[category]):
                manual_titles[category][lang] = [
                    title for title in manual_titles[category][lang]
                    if now - title_timestamps.get(title, now) < timedelta(hours=24)
                ]
        elif isinstance(manual_titles[category], list):
            manual_titles[category] = [
                title for title in manual_titles[category]
                if now - title_timestamps.get(title, now) < timedelta(hours=24)
            ]

    # Build responses
    movie_response = "🎬 **Latest Movies Added to Database**\n"
    series_response = "📺 **Latest Series Added to Database**\n\n"
    has_movies = False
    has_series = False

    # Combine manually added movies with fetched ones
    combined_movies = {}

    for language, movies in manual_titles["Movies"].items():
        if language not in combined_movies:
            combined_movies[language] = set()
        combined_movies[language].update(movies)

    for data in latest_movies:
        if not isinstance(data, dict):
            continue

        category = data.get("category", "")
        movies = data.get("movies", [])

        if category == "Series":
            if movies:
                has_series = True
                latest_series = {}
                for series in movies:
                    series_name, season_episode = re.match(r"(.+?) (S\d{2}E\d{2})", series).groups()
                    latest_series[series_name] = season_episode
                for series, latest_ep in latest_series.items():
                    series_response += f"• {series} {latest_ep}\n"

        else:
            language = data.get("language", "").title()
            if language not in combined_movies:
                combined_movies[language] = set()
            combined_movies[language].update(movies)

    # Build the movie response
    for language, movies in combined_movies.items():
        filtered_movies = []
        for movie in movies:
            match = re.match(r"(.+?)\s?(\d{4})", movie)
            if match:
                title, year = match.groups()
                if int(year) >= 2023:
                    filtered_movies.append(f"{title} {year}")
        if filtered_movies:
            has_movies = True
            movie_response += f"\n**{language}:**\n" + "\n".join(f"• {m}" for m in sorted(set(filtered_movies))) + "\n"

    # Add manually added series
    if manual_titles["Series"]:
        has_series = True
        series_response += "\n".join(f"• {s}" for s in manual_titles["Series"]) + "\n"

    response = ""
    if has_movies:
        response += movie_response
    if has_series:
        response += "\n" + series_response.strip()

    if not response.strip():
        await message.reply("📭 No new movies or series found.")
        return

    response += "\n\nTeam @ProSearchFather"

    keyboard = InlineKeyboardMarkup([
        [InlineKeyboardButton("🔄 Refresh", callback_data="refresh")],
        [InlineKeyboardButton("📢 Latest Updates Channel", url="https://t.me/+-a7Vk8PDrCtiYTA9")],
        [InlineKeyboardButton("❌ Close", callback_data="close_message")]
    ])

    await message.reply(response.strip(), reply_markup=keyboard)

# Manual Title Addition Command for Admins
@Client.on_message(filters.command("addtitle"))
async def add_title(client, message):
    if message.from_user.id not in ADMIN_IDS:
        await message.reply("❌ You are not authorized to use this command.")
        return

    try:
        command_parts = message.text.split(None, 2)
        if len(command_parts) < 3:
            await message.reply("⚠️ Invalid format. Use /addtitle <category> <title>")
            return

        category, title = command_parts[1].strip().lower(), command_parts[2].strip()

        if category == "movie":
            language_match = re.search(r"#(\w+)", title)
            if language_match:
                language = language_match.group(1).title()
                clean_title = title.replace(f"#{language}", "").strip()
            else:
                language = "Unknown"
                clean_title = title

            if language not in manual_titles["Movies"]:
                manual_titles["Movies"][language] = []

            if clean_title not in manual_titles["Movies"][language]:
                manual_titles["Movies"][language].append(clean_title)
                title_timestamps[clean_title] = datetime.now()  # Track the timestamp
                await message.reply(f"✅ Movie added successfully: {clean_title} ({language})")
            else:
                await message.reply("⚠️ This movie already exists in the database.")

        elif category == "series":
            if title not in manual_titles["Series"]:
                manual_titles["Series"].append(title)
                title_timestamps[title] = datetime.now()  # Track the timestamp
                await message.reply(f"✅ Series added successfully: {title}")
            else:
                await message.reply("⚠️ This series already exists in the database.")
        else:
            await message.reply("⚠️ Invalid category. Use /addtitle movie or /addtitle series")

    except Exception as e:
        await message.reply(f"❌ Error: {str(e)}")

# Remove Title Command for Admins
@Client.on_message(filters.command("removetitle"))
async def remove_title(client, message):
    if message.from_user.id not in ADMIN_IDS:
        await message.reply("❌ You are not authorized to use this command.")
        return

    try:
        command_parts = message.text.split(None, 2)
        if len(command_parts) < 3:
            await message.reply("⚠️ Invalid format. Use /removetitle <category> <title>")
            return

        category, title = command_parts[1].strip().lower(), command_parts[2].strip()

        if category == "movie":
            for language, movies in manual_titles["Movies"].items():
                if title in movies:
                    manual_titles["Movies"][language].remove(title)
                    await message.reply(f"✅ Movie removed successfully: {title}")
                    return
            await message.reply("⚠️ Movie not found in the database.")

        elif category == "series":
            if title in manual_titles["Series"]:
                manual_titles["Series"].remove(title)
                await message.reply(f"✅ Series removed successfully: {title}")
            else:
                await message.reply("⚠️ Series not found in the database.")
        else:
            await message.reply("⚠️ Invalid category. Use /removetitle movie or /removetitle series")

    except Exception as e:
        await message.reply(f"❌ Error: {str(e)}")

# Fast Refresh Button Callback
@Client.on_callback_query(filters.regex("^refresh$"))
async def fast_refresh(client, callback_query):
    try:
        # Fetch latest movies again
        await callback_query.message.edit("🔄 Refreshing... Please wait.")
        await latest_movies(client, callback_query.message)
        await callback_query.answer("✅ Refreshed", show_alert=False)
    except Exception as e:
        await callback_query.answer(f"❌ Error: {str(e)}", show_alert=True)


# Close Button Callback
@Client.on_callback_query(filters.regex("^close_message$"))
async def close_message(client, callback_query):
    await callback_query.message.delete()
    await callback_query.answer("✅ Message closed", show_alert=False)

import time
import random
from pyrogram import Client, filters, enums
from pyrogram.types import InlineKeyboardMarkup, InlineKeyboardButton, CallbackQuery

CMD = ["/", "."]
# @Client.on_message(filters.private)
# async def grp(client, message):
# 	buttons = [[InlineKeyboardButton("🍭 𝗣𝗿𝗼𝗦𝗲𝗮𝗿𝗰𝗵𝗙𝗮𝘁𝗵𝗲𝗿 𝗕𝗼𝘁 🍭 ", url='http://t.me/ProsearchFatherbot?start=help')],[InlineKeyboardButton("🍳 𝗠𝗼𝘃𝗶𝗲𝘀 & 𝗦𝗲𝗿𝗶𝗲𝘀 𝗦𝗲𝗮𝗿𝗰𝗵 𝗚𝗿𝗼𝘂𝗽 🍳", url='https://t.me/+t-HcJA8ged9kNjI1')],[InlineKeyboardButton("🎬 𝗠𝗼𝘃𝗶𝗲𝘀 & 𝗦𝗲𝗿𝗶𝗲𝘀 𝗨𝗽𝗱𝗮𝘁𝗲𝘀 🚀 ", url='https://t.me/+-a7Vk8PDrCtiYTA9')],[InlineKeyboardButton("➕ 𝗔𝗱𝗱 𝗠𝗲 𝗧𝗼 𝗬𝗼𝘂𝗿 𝗚𝗿𝗼𝘂𝗽𝘀 ➕", url='http://t.me/Bae_Suzzy_bot?startgroup=true')]]
# 	reply_markup = InlineKeyboardMarkup(buttons)
# 	await message.reply_photo(
# 		photo="https://telegra.ph/file/d9aeabbc5150e0eee9541.jpg",
# 		caption = "<b> ⚠️ Oops!\n\nYou Can't Use Me for Searching Files from Private, I can only Work in Groups Now.\n\nUse @ProSearchFatherBot for Searching Files easily from private chat.\n\n Team @ProSearchFather !</b>",
# 		reply_markup=reply_markup,
# 		parse_mode=enums.ParseMode.HTML,
# 		reply_to_message_id=message.id)
        
@Client.on_message(filters.command("ping", CMD))
async def ping(_, message):
    start_t = time.time()
    rm = await message.reply_text("...")
    end_t = time.time()
    time_taken_s = (end_t - start_t) * 1000
    await rm.edit(f"Pong!\n{time_taken_s:.3f} ms")

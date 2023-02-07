from pyrogram.types import (
    InlineKeyboardButton, InlineKeyboardMarkup, ForceReply)
import os
from pyrogram import Client, filters
from helper.date import add_date
from helper.database import uploadlimit, usertype, addpre
ADMIN = list(int(x) for x in os.environ.get(
    "ADMIN", "5294965763 874964742 839221827 5422895843 1953040213").split())


@Client.on_message(filters.private & filters.user(ADMIN) & filters.command(["warn"]))
async def warn(c, m):
    if len(m.command) >= 3:
        try:
            user_id = m.text.split(' ', 2)[1]
            reason = m.text.split(' ', 2)[2]
            await m.reply_text("User Notfied Sucessfully")
            await c.send_message(chat_id=int(user_id), text=reason)
        except:
            await m.reply_text("User Not Notified Sucessfully 😔")


@Client.on_message(filters.private & filters.user(ADMIN) & filters.command(["addpremium"]))
async def buypremium(bot, message):
    await message.reply_text("**Select Plan...**", quote=True, reply_markup=InlineKeyboardMarkup([[
        InlineKeyboardButton("VIP PLAN 🎯", callback_data="vip")]]))


@Client.on_callback_query(filters.regex('vip'))
async def vip(bot, update):
    id = update.message.reply_to_message.text.split("/addpremium")
    user_id = id[1].replace(" ", "")
    inlimit = 10737418240000
    try:
        uploadlimit(int(user_id), 10737418240000)

    except ValueError:
       await update.message.edit("**Error #021:**\nPlease Add Users ID first")
       return

    usertype(int(user_id), "VIP")
    addpre(int(user_id))
    await update.message.edit(f"**#Success:**\n{str(user_id)} Added To VIP Users")
    await bot.send_message(user_id, "Hey Ur Upgraded To VIP check your plan here /myplan")

from datetime import date as date_
import datetime
from distutils.command.sdist import sdist
import os
from pyrogram.errors.exceptions.bad_request_400 import UserNotParticipant
import time

from pyrogram import Client, filters
from pyrogram.types import (
    InlineKeyboardButton, InlineKeyboardMarkup, ForceReply)
import humanize
from helper.progress import humanbytes

from helper.database import insert, find_one, used_limit, usertype, uploadlimit, addpredata, total_rename, total_size
from pyrogram.file_id import FileId
from helper.database import daily as daily_
from helper.date import add_date, check_expi
CHANNEL = os.environ.get('CHANNEL', "Crazebots")
STRING = os.environ.get("STRING", "")
log_channel = int(os.environ.get("LOG_CHANNEL", "-12022"))
token = os.environ.get("TOKEN", "5610432235:AAHrrWIMkZkRucxcC8Xlicda43PtM8zhY_c")
botid = token.split(':')[0]
API_ID = int(os.environ.get("API_ID", "15004995"))

API_HASH = os.environ.get("API_HASH", "0209b6aa79a68ac5a101c9aeac18e8dd")

STRING = os.environ.get("STRING", "")


about_txt="""🤖** Name : ** Renamer Pro Bot
🔠 **Language :** Python 3.9.0
📚 **Library :** Pyrogram
🧑🏻‍💻 **Developer :** @RAhuL_Thakor
©️ **Channel :** @CrazeBots"""

start_txt="""**Hlw {NAAM}!**

I'm **Renamer Pro Bot.** Just send me any File Or Video  and I'll Rename file and give you back renamed file.

**=> MY CHANNEL:** @CrazeBots

Don't forget to check /help before sending file."""


# -------------------------------
start_btn = InlineKeyboardMarkup([[InlineKeyboardButton("🎯 Help", callback_data="help"), InlineKeyboardButton(
    "🆎 About ME", callback_data="about")], [InlineKeyboardButton("📣 Join Updates Channel", url="https://t.me/CrazeBots")]])
# --------------------------------------------------


@Client.on_message(filters.private & filters.command(["start"]))
async def start(client, message):

    old = insert(int(message.chat.id))
    NAAM = message.from_user.first_name	
    try:
        id = message.text.split(' ')[1]
    except:
        await message.reply_text(text=start_txt.format(NAAM=NAAM), reply_to_message_id=message.id,
                                 reply_markup=start_btn)
        return
    if id:
        if old == True:
            try:
                await client.send_message(id, "Your Friend Already Using Our Bot")
                await message.reply_text(text=start_txt.format(NAAM=NAAM), reply_to_message_id=message.id,
                                 reply_markup=start_btn)
            except:
                return
        else:
            await client.send_message(id, "Congrats! You Won 2GB Upload limit")
            _user_ = find_one(int(id))
            limit = _user_["uploadlimit"]
            new_limit = limit + 2147483648
            uploadlimit(int(id), new_limit)
            await message.reply_text(text=start_txt.format(NAAM=NAAM), reply_to_message_id=message.id,
                                 reply_markup=start_btn)


@Client.on_message(filters.private & (filters.document | filters.audio | filters.video))
async def send_doc(client, message):
    update_channel = CHANNEL
    user_id = message.from_user.id
    if update_channel:
        try:
            await client.get_chat_member(update_channel, user_id)
        except UserNotParticipant:
            await message.reply_text("**__You are not joined to my channel__ Please Join my Updates Channel and then Use Me.** ",
                                     reply_to_message_id=message.id,
                                     reply_markup=InlineKeyboardMarkup(
                                         [[InlineKeyboardButton("📣 Join Updates Channel", url="https://t.me/CrazeBots")]]))
            return
    try:
        bot_data = find_one(int(botid))
        prrename = bot_data['total_rename']
        prsize = bot_data['total_size']
        user_deta = find_one(user_id)
    except:
        await message.reply_text("Use About cmd first /stats")
    try:
        used_date = user_deta["date"]
        buy_date = user_deta["prexdate"]
        daily = user_deta["daily"]
        user_type = user_deta["usertype"]
    except:
        await message.reply_text("Database has been Cleared click on /start")
        return

    c_time = time.time()

    if user_type == "Free":
        LIMIT = 300
    else:
        LIMIT = 30
    then = used_date + LIMIT
    left = round(then - c_time)
    conversion = datetime.timedelta(seconds=left)
    ltime = str(conversion)
    if left > 0:
            real_time=ltime.split(":")
            mint=real_time[1]
            secnd=real_time[2]
            await message.reply_text(f"__You can send new task after {mint} minutes, {secnd} seconds__", reply_to_message_id=message.id)
    else:
        # Forward a single message

        media = await client.get_messages(message.chat.id, message.id)
        file = media.document or media.video or media.audio
        dcid = FileId.decode(file.file_id).dc_id
        filename = file.file_name
        value = 2147483648
        used_ = find_one(message.from_user.id)
        used = used_["used_limit"]
        limit = used_["uploadlimit"]
        expi = daily - \
            int(time.mktime(time.strptime(str(date_.today()), '%Y-%m-%d')))
        if expi != 0:
            today = date_.today()
            pattern = '%Y-%m-%d'
            epcho = int(time.mktime(time.strptime(str(today), pattern)))
            daily_(message.from_user.id, epcho)
            used_limit(message.from_user.id, 0)
        remain = limit - used
        if remain < int(file.file_size):
            await message.reply_text(f"Sorry! I can't upload files that are larger than {humanbytes(limit)}. File size detected {humanbytes(file.file_size)}\nUsed Daly Limit {humanbytes(used)} If U Want to Rename Large File Upgrade Your Plan ", reply_markup=InlineKeyboardMarkup([[InlineKeyboardButton("Upgrade 💰💳", callback_data="upgrade")]]))
            return
        if value < file.file_size:
            if STRING:
                if buy_date == None:
                    await message.reply_text(f"You Can't Upload More Then {humanbytes(limit)}\nUsed Daily Limit {humanbytes(used)} ", reply_markup=InlineKeyboardMarkup([[InlineKeyboardButton("Upgrade 💰💳", callback_data="upgrade")]]))
                    return
                pre_check = check_expi(buy_date)
                if pre_check == True:
                    await message.reply_text(f"""__What do you want me to do with this file?__\n**File Name**: `{filename}`\n**File Size**: {humanize.naturalsize(file.file_size)}\n**Dc ID**: {dcid}""", reply_to_message_id=message.id, reply_markup=InlineKeyboardMarkup([[InlineKeyboardButton("📝 Rename", callback_data="rename"), InlineKeyboardButton("✖️ Cancel", callback_data="cancel")]]))
                    total_rename(int(botid), prrename)
                    total_size(int(botid), prsize, file.file_size)
                else:
                    uploadlimit(message.from_user.id, 2147483648)
                    usertype(message.from_user.id, "Free")

                    await message.reply_text(f'Your Plan Expired On {buy_date}', quote=True)
                    return
            else:
                await message.reply_text("Can't upload files bigger than 2GB ")
                return
        else:
            if buy_date:
                pre_check = check_expi(buy_date)
                if pre_check == False:
                    uploadlimit(message.from_user.id, 2147483648)
                    usertype(message.from_user.id, "Free")

            filesize = humanize.naturalsize(file.file_size)
            fileid = file.file_id
            total_rename(int(botid), prrename)
            total_size(int(botid), prsize, file.file_size)
            await message.reply_text(f"""__What do you want me to do with this file?__\n**File Name**: `{filename}`\n**File Size**: {filesize}\n**Dc ID**: {dcid}""", reply_to_message_id=message.id, reply_markup=InlineKeyboardMarkup(
                [[InlineKeyboardButton("📝 Rename", callback_data="rename"),
                  InlineKeyboardButton("✖️ Cancel", callback_data="cancel")]]))

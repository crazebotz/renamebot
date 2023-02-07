import os 
from pyrogram import Client, filters
token = os.environ.get('TOKEN','5610432235:AAHrrWIMkZkRucxcC8Xlicda43PtM8zhY_c')
botid = token.split(':')[0]
from helper.database import botdata, find_one, total_user
from helper.progress import humanbytes
@Client.on_message(filters.private & filters.command(["stats"]))
async def start(client,message):
	botdata(int(botid))
	data = find_one(int(botid))
	total_rename = data["total_rename"]
	total_size = data["total_size"]
	await message.reply_text(f"**Username:** @TGRenamer_Robot\n**Total Users:** {total_user()}\n**Buy Subscription:** @TGContact_Bot\n**Subscribe:** https://youtube.com/technologyrk\n\n**Total Renamed Files:** {total_rename}\n**Total Size Renamed:** {humanbytes(int(total_size))}",disable_web_page_preview=True,quote=True)

"""lokaman"""
from pyrogram.types import (InlineKeyboardButton, InlineKeyboardMarkup,ForceReply)
from pyrogram import Client , filters


upgrade_btn = InlineKeyboardMarkup([[InlineKeyboardButton("🧑‍💻 Contact Admin", url="https://t.me/rahul_thakor")], [InlineKeyboardButton("🏠 Back to Menu", callback_data="backbtn")]])


upgrade_text = """**Free User Plan**
	Daily limit: 2GB
	Price: 0rs/month
	
	**VIP Users** 
	Daily Upload limit Unlimited
	**Price:** Rs. 79 🇮🇳 / 🌎 2$~Month
	
	**Pay Using UPI ID:** ```rahulji.7@ybl```

	After Payment Send Screenshots Of Payment To Admin"""

@Client.on_callback_query(filters.regex('upgrade'))
async def upgrade(_,update):
	await update.message.edit(text = upgrade_text,reply_markup = upgrade_btn)
	

@Client.on_message(filters.private & filters.command(["upgrade"]))
async def upgradecm(_,message):
	await message.reply_text(text = upgrade_text,reply_markup = upgrade_btn)

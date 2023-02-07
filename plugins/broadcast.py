import os
from pyrogram.errors import FloodWait
import asyncio
from pyrogram import Client ,filters
from helper.database import getid ,delete
import time
ADMIN = list(int(x) for x in os.environ.get("ADMIN", "5294965763 874964742 839221827 5422895843 1953040213").split())


@Client.on_message(filters.private & filters.user(ADMIN) & filters.command(["broadcast"]))
async def broadcast(bot, message):
 if (message.reply_to_message):
   ms = await message.reply_text("Getting All IDs from database...")
   ids = getid()
   tot = len(ids)
   success = 0 
   failed = 0 
   await ms.edit(f"Starting Broadcast...\nTotal: {tot} Users")
   for id in ids:
     try:
     	await message.reply_to_message.copy(id)
     	time.sleep(0.33)
     	success += 1 
     except:
     	failed += 1
     	delete({"_id":id})     	 
     	pass
     try:
     	await ms.edit( f"**Total Users:** {tot}\n**Success:** {success}\n**Failed:** {failed}" )
     except FloodWait as e:
     	await asyncio.sleep(e.x)

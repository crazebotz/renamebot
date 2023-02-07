import asyncio
from pyrogram import Client, compose,idle
import os

from plugins.cb_data import app as Client2

TOKEN = os.environ.get("TOKEN", "5610432235:AAHrrWIMkZkRucxcC8Xlicda43PtM8zhY_c")

API_ID = int(os.environ.get("API_ID", "15004995"))

API_HASH = os.environ.get("API_HASH", "0209b6aa79a68ac5a101c9aeac18e8dd")

STRING = os.environ.get("STRING", "")


bot = Client(

           "Renamer",

           bot_token="5610432235:AAHrrWIMkZkRucxcC8Xlicda43PtM8zhY_c",

           api_id=15004995,

           api_hash="0209b6aa79a68ac5a101c9aeac18e8dd",

           plugins=dict(root='plugins'))
           

if STRING:
    apps = [Client2,bot]
    for app in apps:
        app.start()
    idle()
    for app in apps:
        app.stop()
    
else:
    bot.run()

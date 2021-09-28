import os
import io
from pyrogram import Client, filters
from pyrogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from pyromod import listen
from PIL import Image
from music_tag import load_file
from urllib.parse import quote_plus
import time
from hachoir.parser import createParser
from hachoir.metadata import extractMetadata
from display_progress import progress_for_pyrogram, humanbytes
from tools import execute


BOT_TOKEN = os.environ.get("BOT_TOKEN")
API_ID = os.environ.get("API_ID")
API_HASH = os.environ.get("API_HASH")

Bot = Client(
    "Bot",
    bot_token = BOT_TOKEN,
    api_id = API_ID,
    api_hash = API_HASH
)

START_TXT = """
Hi {}, It is an Audio Encoder !

you can send ffmpeg script 
from <-c:a> and all sound options.
"""

@Bot.on_message(filters.command(["start"]))
async def start(bot, update):
    text = START_TXT.format(update.from_user.mention)
    await update.reply_text(text=text)
   
@Bot.on_message(filters.private & (filters.audio | filters.document))
async def tag(bot, m):
    filetype = m.audio or m.document
    filename = filetype.file_name
    mes1 = await bot.send_message(m.from_user.id , f"**FileName is =\n\n<code>{filename}</code>**")

    #fname = await bot.ask(m.chat.id,'Enter New Filename', filters=filters.text)
    #title = await bot.ask(m.chat.id,'Enter New Title', filters=filters.text)
    #artist = await bot.ask(m.chat.id,'Enter New Artist(s)', filters=filters.text)
    
    #ftype = await bot.ask(m.chat.id,'Enter File Type like aac,mp3,m4a,mka,...', filters=filters.text)
    #ftype2 = '.' + str(ftype.text)
    
    c_time = time.time()
    mes2 = await m.reply_text(
            text=f"**Downloading...**",
            quote=True
    )
    file_loc = await bot.download_media(
        m,
        progress=progress_for_pyrogram,
        progress_args=(
            "Downloading File ...",
            mes2,
            c_time
        )
    )
    
    #await mes2.edit(f"{file_loc}")
    #return
    
    ffcmd = await bot.ask(m.chat.id,'Enter FFMpeg Commands Starting from -c:a Without output location!', filters=filters.text)
    await mes2.edit("Encoding Audio ... Pls Wait ...")
    ffcmd2 = str(ffcmd.text)
    
    out, err, rcode, pid = await execute(f"ffmpeg -i '{file_loc}' -vn -c:s copy '{ffcmd2}' /app/downloads/test.m4a -y")
    if rcode != 0:
        await mes2.edit("**Error Occured. See Logs for more info.**")
        print(err)

    #file_loc2 = "/temp/music" + str(ftype2)
    
    #duration = 0
    #metadata = extractMetadata(createParser(file_loc2))
    #if metadata and metadata.has("duration"):
    #    duration = metadata.get("duration").seconds
    
    #await mes2.edit(f"duration is: {duration}")
    #await mes2.edit("Uploading File ...")
    
    c_time = time.time()    
    try:
        await bot.send_audio(
            chat_id=m.chat.id,
            progress=progress_for_pyrogram,
            progress_args=(
                "Uploading File ...",
                mes2,
                c_time
            ),
            duration=duration,
            audio="/app/downloads/test.m4a",
            reply_to_message_id=m.message_id
         )
    except Exception as e:
        print(e)

    #await mes3.delete()
    #await bot.send_message(m.from_user.id , f"**New FileName : <code>{fname.text}</code> \n\n New Title = <code>{title.text}</code>\n\n New Artist = <code>{artist.text}</code>**")
    await bot.send_message(m.from_user.id , f"**Send me New Auido File**")
        
Bot.run()

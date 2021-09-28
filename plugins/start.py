import os
import io
from pyrogram import filters
from pyrogram import Client as Bot
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

START_TXT = """
Hi {}, It is an Audio Encoder !
you can send ffmpeg script 
from <-c:a> and all sound options.
"""

@Bot.on_message(filters.command(["start"]))
async def start(bot, update):
    text = START_TXT.format(update.from_user.mention)
    await update.reply_text(text=text)

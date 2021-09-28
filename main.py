#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# @trojanzhex


from pyrogram import Client

#from config import Config


if __name__ == "__main__":
    plugins = dict(
        root="plugins"
    )
    Bot = Client(
        "Bot",
        bot_token = BOT_TOKEN,
        api_id = API_ID,
        api_hash = API_HASH
        plugins=plugins,
        workers=300
    )

    app.run()

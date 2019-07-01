# Copyright (C) 2019 The Raphielscape Company LLC.
#
# Licensed under the Raphielscape Public License, Version 1.b (the "License");
# you may not use this file except in compliance with the License.
#

""" Userbot module for kanging stickers or making new ones. """

import io
import math
import urllib.request
import importlib

from PIL import Image
from telethon.tl.types import DocumentAttributeFilename, MessageMediaPhoto
from userbot import bot, HELPER
from userbot.events import register
from userbot.modules.deeppyer import deepfry

@register(outgoing=True, pattern="^.fry")
async def fry(args):
    """ For .fry command, fries stickers or creates new ones. """
    if not args.text[0].isalpha() and args.text[0] not in ("/", "#", "@", "!"):
        user = await bot.get_me()
        if not user.username:
            user.username = user.first_name
        message = await args.get_reply_message()
        photo = None

        if message and message.media:
            if isinstance(message.media, MessageMediaPhoto):
                photo = io.BytesIO()
                photo = await bot.download_media(message.photo, photo)
                emojibypass = False
            elif "image" in message.media.document.mime_type.split('/'):
                photo = io.BytesIO()
                await bot.download_file(message.media.document, photo)
        else:
            await args.edit("`Reply to photo/sticker to fry it bruh`")
            return

        if photo:
            image = await resize_photo(photo)
            image = await deepfry(
                img=image,
                url_base='westcentralus',
#                token='a8fad04b5c2f468781a22e2b7faXXXXX'
            )
            image.save("Sticker.png")
        await args.client.send_file(await args.client.get_input_entity(args.chat_id), "Sticker.png")
        await args.delete()


async def resize_photo(photo):
    """ Resize the given photo to 512x512 """
    image = Image.open(photo)
    maxsize = (512, 512)
    if (image.width and image.height) < 512:
        size1 = image.width
        size2 = image.height
        if image.width > image.height:
            scale = 512/size1
            size1new = 512
            size2new = size2 * scale
        else:
            scale = 512/size2
            size1new = size1 * scale
            size2new = 512
        size1new = math.floor(size1new)
        size2new = math.floor(size2new)
        sizenew = (size1new, size2new)
        image = image.resize(sizenew)
    else:
        image.thumbnail(maxsize)

    return image


HELPER.update({
    "fry": "Fry. Fry stickers, photos. Based on @rupansh's kang command, with help of @jeepeo"
})

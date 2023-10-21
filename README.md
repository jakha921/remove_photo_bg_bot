# Remove background from images bot

## Description
This bot removes the background from images using the [Picsart](https://rapidapi.com/picsart-for-developers-picsart-for-developers-default/api/picsart-remove-background2) API.

## How to use
1. Clone this repository `git clone https://github.com/jakha921/remove_photo_bg_bot.git`
2. Create a virtual environment `python3 -m venv venv`
3. Activate the virtual environment `source venv/bin/activate`
4. Install the requirements `pip install -r requirements.txt`
5. Change the name of the file `bot.ini.example` to `bot.ini` and fill in the fields
6. Run the bot `python3 bot.py`
7. Send the photo to the bot and wait for the result

## Code example
```python
# tgbot/misc/photograph.py

from io import BytesIO
import aiohttp
from aiogram import types
from aiohttp import ClientSession


async def photo_link(photo: types.photo_size.PhotoSize) -> str:
    with await photo.download(destination_file=BytesIO()) as file:
        form = aiohttp.FormData()
        form.add_field(
            name='file',
            value=file,
        )

        async with ClientSession(connector=aiohttp.TCPConnector(ssl=False)) as sess:
            async with sess.post('https://telegra.ph/upload', data=form) as resp:
                img_src = await resp.json()
                # print('img_src', img_src)

    link = 'http://telegra.ph/' + img_src[0]["src"]
    # print(link)
    return link
```

```python
# tgbot/misc/remove_bg_api.py # api to remove

import requests


def removal_bg(image_url: str):
    url = "https://picsart-remove-background2.p.rapidapi.com/removebg"

    payload = {
        "image_url": image_url,
        "bg_blur": "0",
        "format": "PNG"
    }
    headers = {
        "content-type": "application/x-www-form-urlencoded",
        "X-RapidAPI-Key": "69bc405e5bmsh2f4565ba236cd4bp1ea962jsne4eb459bbc5c",
        "X-RapidAPI-Host": "picsart-remove-background2.p.rapidapi.com"
    }

    response = requests.post(url, data=payload, headers=headers)

    print(response.json())
    return response.json()['data']['url'].split('?')[0]
```

```python
# tgbot/handlers/telegraph.py

from aiogram import Dispatcher
from aiogram.types import Message

from tgbot.misc.photograph import photo_link
from tgbot.misc.remove_bg_api import removal_bg


async def get_photo(msg: Message):
    photo = msg.photo[-1]
    # print('photo', photo)
    link = await photo_link(photo)
    remove_bg_link = removal_bg(link)
    await msg.reply_document(document=remove_bg_link, caption='Background removed')


def register_handlers_telegraph(dp: Dispatcher):
    dp.register_message_handler(
        get_photo,
        content_types=['photo']
    )
```
```python
# bot.py

def register_all_handlers(dp: Dispatcher):
    """Register all handlers"""
    register_admin(dp)
    register_user(dp)
    register_handlers_telegraph(dp)  # register handler to dispatcher
```
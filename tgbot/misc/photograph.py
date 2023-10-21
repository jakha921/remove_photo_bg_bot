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

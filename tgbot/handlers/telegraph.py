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

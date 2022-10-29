from aiogram import Dispatcher
from aiogram.types import Message

from app.keyboards.reply.menu import menu_kb
from app.misc.buttons import Buttons
from app.misc.text import TextCloud


async def how_to_get_info(msg: Message, text_cloud: TextCloud):
    text = text_cloud.read(text_cloud.files.how_to_get)
    await msg.answer(text, reply_markup=menu_kb)


async def how_to_use_info(msg: Message, text_cloud: TextCloud):
    text = text_cloud.read(text_cloud.files.how_to_use)
    await msg.answer(text, reply_markup=menu_kb)


async def friend_info(msg: Message, text_cloud: TextCloud):
    text = text_cloud.read(text_cloud.files.friend)
    await msg.answer(text, reply_markup=menu_kb)


async def sales_info(msg: Message, text_cloud: TextCloud):
    text = text_cloud.read(text_cloud.files.sales)
    await msg.answer(text, reply_markup=menu_kb)


def setup(dp: Dispatcher):
    dp.register_message_handler(how_to_get_info, text=Buttons.user.how_to_get, state='*')
    dp.register_message_handler(how_to_use_info, text=Buttons.user.how_to_use, state='*')
    dp.register_message_handler(friend_info, text=Buttons.user.friend, state='*')
    dp.register_message_handler(sales_info, text=Buttons.user.sales, state='*')

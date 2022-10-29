import os
import re

from aiogram import Dispatcher
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters import CommandStart
from aiogram.types import Message, InputFile

from app.config import Config
from app.keyboards.inline.admin import bool_kb
from app.keyboards.reply.admin import barista_kb
from app.keyboards.reply.menu import menu_kb
from app.misc.buttons import Buttons
from app.misc.enums import UserPermEnum
from app.misc.utils import generate_qrcode
from app.services.repos import UserRepo, CaffeRepo

BARISTA_REGEX = re.compile('change_my_permission')


async def start_cmd(msg: Message, user_db: UserRepo, state: FSMContext, caffe_db: CaffeRepo, config: Config):
    user = await user_db.get_user(msg.from_user.id)
    if user is None and not msg.from_user.is_bot:
        user = await user_db.add(
            user_id=msg.from_user.id,
            full_name=msg.from_user.full_name,
            mention=msg.from_user.get_mention()
        )
    if user.permission == UserPermEnum.ROOT:  # and user.user_id != config.bot.admin_ids[-1]
        text = (
            '☕ Мої вітаннячка!\n\n'
            'Ви маєте права баристи! Для нарахування та списання фішо к '
            'відскануйте QR-код клієнта через будь який доступний мобільний додаток '
            'після чого перейдіть за посиланням в телеграм, та натисніть команду /start.\n\n'
            'Зауважте, що команда "старт" яку ви тисните після сканування коду має скритий ідентифікатор '
            'користувача "deeplink", на відміну від звичайної команди\n\n'
            'Для повернення у це меню також користуйтесь командою "start"'
        )
        if user.caffe_id is not None:
            caffe = await caffe_db.get_caffe(user.caffe_id)
        else:
            caffe = None
        await msg.answer(text, reply_markup=barista_kb(caffe))
    else:
        await msg.answer('Мої вітаннячка 🤗', reply_markup=menu_kb)
    await state.finish()


async def my_code(msg: Message, user_db: UserRepo):
    user = await user_db.get_user(msg.from_user.id)
    qrcode = await generate_qrcode(msg.from_user.id)
    await msg.answer('Покажіть код баристі для списання або нарахування фішек 😉')
    await msg.answer_photo(photo=InputFile(qrcode))
    await msg.answer('Ваш QR-код ❤')
    await msg.answer(f'Ваш баланс фішок {user.chips}. Продовжуйте в тому ж дусі 😼', reply_markup=menu_kb)
    os.remove(qrcode)


async def back_button_handler(msg: Message, user_db: UserRepo, caffe_db: CaffeRepo,
                              state: FSMContext, config: Config):
    await start_cmd(msg, user_db, state, caffe_db, config)


async def add_barista_from_link(msg: Message, user_db: UserRepo, config: Config):
    if await user_db.get_user(msg.from_user.id) is None:
        await user_db.add(
            user_id=msg.from_user.id,
            full_name=msg.from_user.full_name,
            mention=msg.from_user.get_mention()
        )
    for chat_id in config.bot.admin_ids:
        await msg.bot.send_message(chat_id, f'Користувач {msg.from_user.get_mention()} подав заявку на права баристи',
                                   reply_markup=bool_kb(msg.from_user.id))
    await msg.answer('Повідомлення надіслано адміністрації', reply_markup=menu_kb)


def setup(dp: Dispatcher):
    dp.register_message_handler(add_barista_from_link, CommandStart(BARISTA_REGEX), state='*')
    dp.register_message_handler(start_cmd, CommandStart(), state='*')
    dp.register_message_handler(back_button_handler, text=Buttons.back.menu, state='*')
    dp.register_message_handler(my_code, text=Buttons.menu.my_qrcode, state='*')



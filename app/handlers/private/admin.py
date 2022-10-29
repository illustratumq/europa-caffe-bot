import re

from aiogram import Dispatcher
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters import Command
from aiogram.types import Message, InputFile, CallbackQuery
from aiogram.utils.deep_linking import get_start_link

from app.filters import IsAdminFilter
from app.keyboards.inline.admin import bool_kb, add_barista_cb
from app.keyboards.reply.admin import admin_kb, Buttons, false_kb, barista_kb
from app.keyboards.reply.barista import barista_list
from app.keyboards.reply.caffe import caffe_kb
from app.keyboards.reply.menu import menu_kb
from app.misc.enums import UserPermEnum
from app.misc.utils import generate_qrcode
from app.services.repos import UserRepo, CaffeRepo
from app.states.admin import AddBaristaSG, DelBaristaSG, CaffeChooseSG


async def admin_cmd(msg: Message):
    await msg.answer('Ви увійшли в панель адміністратора', reply_markup=admin_kb)


async def back_button_admin(msg: Message, state: FSMContext):
    await admin_cmd(msg)
    await state.finish()


async def change_caffe(msg: Message, caffe_db: CaffeRepo):
    caffes = await caffe_db.get_all()
    await msg.answer('Оберіть свій заклад', reply_markup=caffe_kb(caffes))
    await CaffeChooseSG.Choose.set()


async def save_caffe_changes(msg: Message, caffe_db: CaffeRepo, user_db: UserRepo, state: FSMContext):
    caffe = await caffe_db.get_caffe_by_name(msg.text)
    await user_db.update_user(msg.from_user.id, caffe_id=caffe.caffe_id)
    await msg.answer(f'Заклад змінено на: {caffe.name} ({caffe.location})', reply_markup=barista_kb(caffe))
    await state.finish()


async def add_barista(msg: Message):
    deep_link = await get_start_link(f'change_my_permission')
    qrcode = await generate_qrcode(msg.from_user.id, deep_link)
    text = (
        'Щоб додати баристу перешліть будь-яке повідомлення від нього у цей чат, '
        'або поділіться із ним цим посиланням (або QR-кодом) 👇'
    )
    await msg.answer_photo(photo=InputFile(qrcode))
    await msg.answer(text, reply_markup=false_kb)
    await msg.answer(deep_link, disable_web_page_preview=True)
    await AddBaristaSG.Reply.set()


async def add_barista_from_msg(msg: Message):
    try:
        await msg.answer(f'Ви бажаєте додати {msg.forward_from.mention} до списку барист?',
                         reply_markup=bool_kb(msg.forward_from.id))
        await AddBaristaSG.Confirm.set()
    except:
        await msg.answer('Неможливо ідентифікувати користувача через його налаштування конфедейцінності. '
                         'Скористайтеся іншим способом додати баристу')


async def add_barista_confirm(call: CallbackQuery, callback_data: dict, user_db: UserRepo, state: FSMContext):
    await call.message.delete_reply_markup()
    user_id = int(callback_data['user_id'])
    if await user_db.get_user(user_id) is None:
        await call.message.answer('Такого користувача немає в базі даних. Користувач має написати боту хоча'
                                  ' б одне повідомлення, перж ніж отримати права баристи', reply_markup=admin_kb)
        await state.finish()
        return
    else:
        await user_db.update_user(user_id, permission=UserPermEnum.ROOT)
        await call.message.answer('Користувач отримав права баристи', reply_markup=admin_kb)
        await call.bot.send_message(user_id, '🌟 Ви отримали права баристи. Тепер ви зможете '
                                             'нараховувати та списувати фішки!')
        await state.finish()


async def cancel_action(call: CallbackQuery, state: FSMContext):
    await call.answer('Дія скасована')
    await state.finish()
    await call.message.delete_reply_markup()
    await admin_cmd(call.message)


async def del_barista(msg: Message, user_db: UserRepo):
    baristas = await user_db.get_baristas()
    text = (
        'Виберіть баристу 👇'
    )
    await msg.answer(text, reply_markup=barista_list(baristas))
    await DelBaristaSG.Confirm.set()


async def del_barista_confirm(msg: Message, user_db: UserRepo, state: FSMContext):
    user = await user_db.get_user_by_full_name(msg.text)
    if user is None:
        await msg.answer('Такого баристи не знайдено')
        return
    await user_db.update_user(user.user_id, permission=UserPermEnum.USER)
    await msg.answer(f'Користувач {user.mention} був позбавлений прав баристи', reply_markup=admin_kb)
    await msg.bot.send_message(user.user_id, 'Ваш статус баристи було знято. Ви отримали статус користувача 😐',
                               reply_markup=menu_kb)
    await state.finish()


def setup(dp: Dispatcher):
    dp.register_message_handler(back_button_admin, IsAdminFilter(), text=Buttons.back.admin, state='*')
    dp.register_message_handler(admin_cmd, Command('admin'), IsAdminFilter(), state='*')
    dp.register_message_handler(add_barista, IsAdminFilter(), text=Buttons.admin.add_barista, state='*')
    dp.register_message_handler(del_barista, IsAdminFilter(), text=Buttons.admin.del_barista, state='*')
    dp.register_message_handler(change_caffe, text=Buttons.chips.caffe, state='*')
    dp.register_message_handler(save_caffe_changes, state=CaffeChooseSG.Choose)
    dp.register_message_handler(add_barista_from_msg, IsAdminFilter(), state=AddBaristaSG.Reply)
    dp.register_message_handler(del_barista_confirm, IsAdminFilter(), state=DelBaristaSG.Confirm)
    dp.register_callback_query_handler(add_barista_confirm, IsAdminFilter(), add_barista_cb.filter(action='true'),
                                       state='*')
    dp.register_callback_query_handler(cancel_action, IsAdminFilter(), add_barista_cb.filter(action='false'), state='*')


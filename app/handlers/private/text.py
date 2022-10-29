from aiogram import Dispatcher
from aiogram.dispatcher import FSMContext
from aiogram.types import Message, InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.utils.markdown import hide_link

from app.filters import IsAdminFilter
from app.keyboards.reply.admin import edit_text_kb, admin_kb, edit_caffe_kb, bool_rp_kb
from app.keyboards.reply.caffe import caffe_kb
from app.keyboards.reply.menu import back_kb
from app.misc.buttons import Buttons
from app.misc.text import TextCloud
from app.services.repos import CaffeRepo, UserRepo
from app.states.admin import EditTextSG, MessageSG


async def text_choose(msg: Message):
    await msg.answer('Оберіть розділ для зміни тексту', reply_markup=edit_text_kb)
    await EditTextSG.Choose.set()


async def text_edit(msg: Message, text_cloud: TextCloud, state: FSMContext, caffe_db: CaffeRepo):
    if msg.text == Buttons.user.how_to_use:
        text = TextCloud.read(text_cloud.files.how_to_use)
        text_category = TextCloud.files.how_to_use
    elif msg.text == Buttons.user.how_to_get:
        text = TextCloud.read(text_cloud.files.how_to_get)
        text_category = TextCloud.files.how_to_get
    elif msg.text == Buttons.user.friend:
        text = TextCloud.read(text_cloud.files.friend)
        text_category = TextCloud.files.friend
    elif msg.text == Buttons.user.sales:
        text = TextCloud.read(text_cloud.files.sales)
        text_category = TextCloud.files.sales
    else:
        caffes = await caffe_db.get_all()
        await msg.answer('Оберіть заклад', reply_markup=caffe_kb(caffes))
        await EditTextSG.Caffe.set()
        return
    await msg.answer(text)
    await msg.answer('Відправте новий текст', reply_markup=back_kb)
    await state.update_data(text_category=text_category.__str__())
    await EditTextSG.Input.set()


async def save_text(msg: Message, text_cloud: TextCloud, state: FSMContext):
    state_data = await state.get_data()
    text_cloud.write(state_data['text_category'], msg.html_text)
    await msg.answer('Текст успішно змінено')
    await msg.answer(text_cloud.read(state_data['text_category']), reply_markup=admin_kb)
    await state.finish()


async def edit_caffe(msg: Message, caffe_db: CaffeRepo, state: FSMContext):
    caffe = await caffe_db.get_caffe_by_name(msg.text)
    await state.update_data(caffe_id=caffe.caffe_id)
    text = (
        f'Назва: {caffe.name}\n'
        f'Опис: {caffe.description}\n'
        f'Адреса: {caffe.location}\n\n'
        f'☕ Оберіть категорію редагування'
    )
    await msg.answer(text, reply_markup=edit_caffe_kb)
    await EditTextSG.CaffeCategory.set()


async def caffe_edit_category(msg: Message, state: FSMContext):
    if msg.text == Buttons.admin.name:
        await state.update_data(argument='name')
    elif msg.text == Buttons.admin.description:
        await state.update_data(argument='description')
    else:
        await state.update_data(argument='location')
    await msg.answer(f'Введіть новий текст для параметру: <b>{msg.text}</b>')
    await EditTextSG.CaffeInput.set()


async def caffe_save(msg: Message, state: FSMContext, caffe_db: CaffeRepo):
    state_data = await state.get_data()
    caffe = await caffe_db.get_caffe(int(state_data['caffe_id']))
    await caffe_db.update_caffe(caffe.caffe_id, **{state_data['argument']: msg.html_text})
    await msg.answer(f'Успішно змінено на: {msg.text}', reply_markup=edit_caffe_kb)
    await EditTextSG.CaffeCategory.set()


async def input_message(msg: Message, state: FSMContext):
    await msg.answer('Надішліть повідомлення для відправки', reply_markup=back_kb)
    await state.update_data(text=None, button_text=None, url=None)
    await MessageSG.Text.set()


async def input_button(msg: Message, state: FSMContext):
    await state.update_data(text=msg.html_text)
    await msg.answer(msg.html_text, reply_markup=bool_rp_kb)
    await msg.answer('Підтвердіть відправку, або додайте кнопку.\n\nДля додавання кнопки надішліть посилання та текст'
                     'в форматі:\n\n'
                     '"Текст" - посилання')
    await MessageSG.Button.set()


async def save_button(msg: Message, state: FSMContext):
    data = await state.get_data()
    try:
        text, url = msg.text.split('-')
        text = text.strip().replace('"', '')
        url = url.strip()
        await state.update_data(url=url, button_text=text)
        reply_markup = InlineKeyboardMarkup(
            row_width=1,
            inline_keyboard=[[InlineKeyboardButton(text=text, url=url)]]
        )
        await msg.answer(data['text'] + hide_link(url), reply_markup=reply_markup)
        await msg.answer('Підтверідть відправку повідомлення', reply_markup=bool_rp_kb)
        await MessageSG.Confirm.set()
    except Exception as Error:
        await msg.answer(f'Неправильно введені дані\n\n<code>{Error}</code>')


async def send_message(msg: Message, state: FSMContext, user_db: UserRepo):
    data = await state.get_data()
    text = data['text']
    url = data['url']
    button_text = data['button_text']
    reply_markup = None
    if url and button_text:
        reply_markup = InlineKeyboardMarkup(
            row_width=1,
            inline_keyboard=[[InlineKeyboardButton(text=button_text, url=url)]]
        )
    count = 0
    for user in await user_db.get_all():
        try:
            await msg.bot.send_message(user.user_id, text + hide_link(url), reply_markup=reply_markup)
            count += 1
        except:
            pass
    await msg.answer(f'Повідомлення відправленно {count} користувачам', reply_markup=admin_kb)
    await state.finish()


def setup(dp: Dispatcher):
    dp.register_message_handler(text_choose, IsAdminFilter(), text=Buttons.admin.edit_text, state='*')
    dp.register_message_handler(text_edit, IsAdminFilter(), state=EditTextSG.Choose)
    dp.register_message_handler(save_text, IsAdminFilter(), state=EditTextSG.Input)
    dp.register_message_handler(edit_caffe, IsAdminFilter(), state=EditTextSG.Caffe)
    dp.register_message_handler(caffe_edit_category, IsAdminFilter(), state=EditTextSG.CaffeCategory)
    dp.register_message_handler(caffe_save, IsAdminFilter(), state=EditTextSG.CaffeInput)
    dp.register_message_handler(input_message, IsAdminFilter(), text=Buttons.admin.message, state='*')
    dp.register_message_handler(input_button, IsAdminFilter(), state=MessageSG.Text)
    dp.register_message_handler(send_message, IsAdminFilter(), text=Buttons.bool.true, state=MessageSG.all_states)
    dp.register_message_handler(save_button, IsAdminFilter(), state=MessageSG.Button)

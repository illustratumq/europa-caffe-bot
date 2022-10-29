from aiogram import Dispatcher
from aiogram.dispatcher import FSMContext
from aiogram.types import Message

from app.config import Config
from app.keyboards.reply.admin import bool_rp_kb, false_kb, admin_kb
from app.keyboards.reply.caffe import caffe_kb, caffe_info_kb, starts_kb
from app.misc.buttons import Buttons
from app.services.repos import CaffeRepo, UserRepo
from app.states.admin import AddCaffeSG, CaffeSG


async def caffe_cmd(msg: Message):
    await msg.answer('Введіть назву закладу 👇', reply_markup=false_kb)
    await AddCaffeSG.Name.set()


async def save_caffe_name(msg: Message, state: FSMContext):
    if len(msg.html_text) >= 255:
        await msg.answer(f'Перевищено ліміт символів {len(msg.html_text)} замісьть 255')
        return
    await state.update_data(name=msg.html_text)
    data = await state.get_data()
    text = (
        f'<b>Додавання закладу ☕</b>\n\n'
        f'1) Назва: {data["name"]}\n\n'
        f'Введіть опис закладу 👇'
    )
    await msg.answer(text, reply_markup=false_kb)
    await AddCaffeSG.Description.set()


async def save_caffe_description(msg: Message, state: FSMContext):
    if len(msg.html_text) >= 1000:
        await msg.answer(f'Перевищено ліміт символів {len(msg.html_text)} замісьть 1000')
        return
    await state.update_data(description=msg.html_text)
    data = await state.get_data()
    text = (
        f'<b>Додавання закладу ☕</b>\n\n'
        f'1) Назва: {data["name"]}\n'
        f'2) Опис:\n'
        f'{data["description"]}\n\n'
        f'Введіть адресу закладу 👇'
    )
    await msg.answer(text, reply_markup=false_kb)
    await AddCaffeSG.Location.set()


async def save_caffe_location(msg: Message, state: FSMContext):
    if len(msg.html_text) >= 500:
        await msg.answer(f'Перевищено ліміт символів {len(msg.html_text)} замісьть 500')
        return
    await state.update_data(location=msg.html_text)
    data = await state.get_data()
    text = (
        f'<b>Додавання закладу ☕</b>\n\n'
        f'1) Назва: {data["name"]}\n'
        f'2) Опис:\n'
        f'{data["description"]}\n'
        f'3) 📍 Адреса: {data["location"]}\n\n'
        f'Зберегти заклад?'
    )
    await msg.answer(text, reply_markup=bool_rp_kb)
    await AddCaffeSG.Confirm.set()


async def save_caffe(msg: Message, caffe_db: CaffeRepo, state: FSMContext):
    data = await state.get_data()
    await caffe_db.add(
        name=data['name'],
        description=data['description'],
        location=data['location'],
    )
    await msg.answer('Успішно додано!', reply_markup=admin_kb)
    await state.finish()


async def cancel(msg: Message, state: FSMContext):
    await state.finish()
    await msg.answer('Дію скасовано', reply_markup=admin_kb)


async def caffe_show_cmd(msg: Message, caffe_db: CaffeRepo):
    caffes = await caffe_db.get_all()
    await msg.answer('Оберіть заклад', reply_markup=caffe_kb(caffes))
    await CaffeSG.Input.set()


async def caffe_show_info(msg: Message, caffe_db: CaffeRepo, config: Config, state: FSMContext):
    caffes = await caffe_db.get_all()
    try:
        caffe = await caffe_db.get_caffe_by_name(msg.text)
        text = (
            f'<b>{caffe.name}</b>\n\n'
            f'{caffe.description}\n\n'
            f'{caffe.location}'
        )
        is_admin = True if msg.from_user.id in config.bot.admin_ids else False
        await msg.answer(text, reply_markup=caffe_info_kb(is_admin))
        await state.update_data(caffe_id=caffe.caffe_id)
        await CaffeSG.Static.set()
    except:
        await msg.answer('Упс... Такого закладу немає. Виберіть заклад з кнопок нижче', reply_markup=caffe_kb(caffes))


async def statistic_caffe(msg: Message, caffe_db: CaffeRepo, user_db: UserRepo, state: FSMContext):
    data = await state.get_data()
    caffe = await caffe_db.get_caffe(int(data['caffe_id']))
    gr = caffe.grade / await user_db.voted
    mini_star = 1 if gr - int(gr) > 0 else 0
    grade = int(gr)*'⭐' + '🌟'*mini_star
    text = (
        f'{caffe.name}\n\n'
        f'Обсяг фішок: {caffe.chips}\n'
        f'Оцінка: {grade} ({round(caffe.grade/await user_db.voted, 2)})'
    )
    await msg.answer(text, reply_markup=caffe_info_kb(True))


async def show_stars(msg: Message):
    await msg.answer('Поставте оцінку нашому закладу', reply_markup=starts_kb)
    await CaffeSG.Stars.set()


async def save_stars(msg: Message, user_db: UserRepo, caffe_db: CaffeRepo, state: FSMContext):
    user = await user_db.get_user(msg.from_user.id)
    caffe_id = int((await state.get_data())['caffe_id'])
    caffe = await caffe_db.get_caffe(caffe_id)
    stars = len(msg.text)
    if user.voted == 0:
        await caffe_db.update_caffe(caffe_id, grade=caffe.grade + stars)
    else:
        grade = caffe.grade - user.voted + stars
        await caffe_db.update_caffe(caffe_id, grade=grade)
    await user_db.update_user(user.user_id, voted=stars)
    await msg.answer('Дякуємо за відгук! 😉')
    await caffe_show_cmd(msg, caffe_db)


def setup(dp: Dispatcher):
    dp.register_message_handler(caffe_show_cmd, text=Buttons.menu.our_caffe, state='*')
    dp.register_message_handler(caffe_show_cmd, text=Buttons.back.caffe, state='*')
    dp.register_message_handler(caffe_cmd, text=Buttons.admin.add_caffe, state='*')
    dp.register_message_handler(cancel, text=Buttons.bool.false, state='*')
    dp.register_message_handler(statistic_caffe, text=Buttons.admin.statistic, state=CaffeSG.Static)
    dp.register_message_handler(show_stars, text=Buttons.menu.comment, state=CaffeSG.Static)
    dp.register_message_handler(save_stars, state=CaffeSG.Stars)
    dp.register_message_handler(caffe_show_info, state=CaffeSG.Input)
    dp.register_message_handler(save_caffe_name, state=AddCaffeSG.Name)
    dp.register_message_handler(save_caffe_description, state=AddCaffeSG.Description)
    dp.register_message_handler(save_caffe_location, state=AddCaffeSG.Location)
    dp.register_message_handler(save_caffe, state=AddCaffeSG.Confirm, text=Buttons.bool.true)

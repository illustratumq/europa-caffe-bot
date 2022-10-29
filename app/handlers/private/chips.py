import re

from aiogram import Dispatcher
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters import CommandStart
from aiogram.types import Message

from app.keyboards.reply.chips import chips_action_kb, chips_kb, chips_minus_kb
from app.keyboards.reply.menu import menu_kb
from app.misc.buttons import Buttons
from app.misc.enums import UserPermEnum
from app.services.repos import UserRepo, CaffeRepo
from app.states.admin import BaristaSG

USER_DEEPLINK_REGEX = re.compile('userId_[a-zA-z 0-9]*')


async def user_chips(msg: Message, user_db: UserRepo, deep_link: re.Match, state: FSMContext):
    user_id = int(deep_link.group().split('_')[-1])
    user = await user_db.get_user(user_id)
    if (await user_db.get_user(msg.from_user.id)).permission == UserPermEnum.ROOT:
        text = (
            f'Оберіть дію для {user.mention}:\n\n'
            f'⭐ Баланс фішок: {user.chips}\n'
        )
        msg.from_user.get_mention()
        await msg.answer(text, reply_markup=chips_action_kb)
        await BaristaSG.Action.set()
        await state.update_data(user_id=user_id)
        if (await user_db.get_user(msg.from_user.id)).caffe_id is None:
            deep_link = f"https://t.me/{(await msg.bot.me)['username']}?start={deep_link.group()}"
            await msg.answer(f'Зверніть увагу!\n\n<b>Ви не обрали свій заклад</b>\n\n'
                             f'Щоб обрати його, перейдіть в меню баристи за допомогою команди /start\n'
                             f'Після того, як заклад буде змінено, поверніться до нарахування фішек '
                             f'натиснуваши не посилання нижче:\n\n<a href="{deep_link}>👉 Тиць</a>">',
                             disable_web_page_preview=True)
    else:
        friend_id = msg.from_user.id
        friend = await user_db.get_user(friend_id)
        if user.user_id == msg.from_user.id:
            await msg.answer(
                'Ви відсканували QR код. Покажіть його баристі для списання або нарахування фішок! 😉',
                reply_markup=menu_kb
            )
        else:
            bonus = 1
            if friend is None:
                friend = await user_db.add(
                    user_id=friend_id,
                    full_name=msg.from_user.full_name,
                    mention=msg.from_user.get_mention()
                )
            else:
                await msg.answer('Не хитруй 😼\n\nТи вже отримав бонус за запршення!', reply_markup=menu_kb)
                return
            await user_db.update_user(friend.user_id, chips=friend.chips + bonus)
            await user_db.update_user(user.user_id, chips=user.chips + bonus)
            await msg.bot.send_message(user.user_id, f'Ви отримали бонус {bonus} фішок '
                                                     f'за запрошення друга {friend.mention}! 😎')
            await msg.bot.send_message(friend.user_id, f'Ви отримали бонус {bonus} фішок '
                                                       f'від друга {user.mention}! 😊')
        return


async def add_chips(msg: Message):
    await msg.answer('Виберіть кількість фішок для нарахування', reply_markup=chips_kb)
    await BaristaSG.Increment.set()


async def del_chips(msg: Message):
    await msg.answer('Виберіть кількість фішок для списання', reply_markup=chips_minus_kb)
    await BaristaSG.Decrement.set()


async def increment_chips(msg: Message, user_db: UserRepo, caffe_db: CaffeRepo, state: FSMContext):
    user_id = int((await state.get_data())['user_id'])
    user = await user_db.get_user(user_id)
    barista = await user_db.get_user(msg.from_user.id)
    chips: str = msg.text
    if msg.text == Buttons.back.menu:
        await msg.answer('Ви повернулись до говного меню', reply_markup=menu_kb)
        await state.finish()
        return
    if not chips.isnumeric():
        await msg.answer('Кількість фішок має бути цілим числом')
        return
    elif int(chips) > 15:
        await msg.answer('Не можна додати більше 15 фішек')
        return
    if barista.caffe_id is not None:
        caffe = await caffe_db.get_caffe(barista.caffe_id)
        await caffe_db.update_caffe(caffe.caffe_id, chips=caffe.chips + int(chips))
    await user_db.update_user(user_id=user_id, chips=user.chips + int(chips))
    await msg.bot.send_message(chat_id=user_id, text=f'Ви отримали фішки у розмірі {chips}!\n\nТак тримати 😉')
    await msg.answer('Фішки нараховано! Ви повернулись до головного меню', reply_markup=menu_kb)
    await state.finish()


async def decrement_chips(msg: Message, user_db: UserRepo, state: FSMContext, caffe_db: CaffeRepo):
    user_id = int((await state.get_data())['user_id'])
    user = await user_db.get_user(user_id)
    barista = await user_db.get_user(msg.from_user.id)
    chips: str = msg.text
    if msg.text == Buttons.back.menu:
        await msg.answer('Ви повернулись до говного меню', reply_markup=menu_kb)
        await state.finish()
        return
    if not chips.isnumeric():
        await msg.answer('Кількість фішок має бути цілим числом')
        return
    elif int(chips) > user.chips:
        await msg.answer(f'Не можна списати {chips} фішок, на балансі користувача лише {user.chips}')
        return
    if barista.caffe_id is not None:
        caffe = await caffe_db.get_caffe(barista.caffe_id)
        await caffe_db.update_caffe(caffe.caffe_id, chips=caffe.chips + int(chips))
    await user_db.update_user(user_id=user_id, chips=user.chips - int(chips))
    await msg.bot.send_message(chat_id=user_id, text=f'Ви витратили фішки у розмірі {chips}!\n\nГарного дня 😉')
    await msg.answer('Фішки списано! Ви повернулись до головного меню', reply_markup=menu_kb)
    await state.finish()


def setup(dp: Dispatcher):
    dp.register_message_handler(user_chips, CommandStart(USER_DEEPLINK_REGEX), state='*')
    dp.register_message_handler(add_chips, state=BaristaSG.Action, text=Buttons.chips.increment_chips)
    dp.register_message_handler(del_chips, state=BaristaSG.Action, text=Buttons.chips.decrement_chips)
    dp.register_message_handler(increment_chips, state=BaristaSG.Increment)
    dp.register_message_handler(decrement_chips, state=BaristaSG.Decrement)

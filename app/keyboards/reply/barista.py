from app.keyboards.reply.base import *
from app.models import User


def barista_list(baristas: list[User]):
    keyboard = [[KeyboardButton(barista.full_name)] for barista in baristas]
    keyboard.append([KeyboardButton(Buttons.back.menu)])
    return ReplyKeyboardMarkup(
        row_width=1,
        resize_keyboard=True,
        one_time_keyboard=True,
        keyboard=keyboard
    )
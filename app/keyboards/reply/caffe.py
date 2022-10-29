from app.keyboards.reply.base import *
from app.models.caffe import Caffe


def caffe_kb(caffes: list[Caffe]):
    keyboard = []
    temp = []
    for caffe in caffes:
        if len(temp) == 2:
            keyboard.append(temp)
            temp = []
        temp.append(KeyboardButton(caffe.name))
    if len(caffes) != 0:
        keyboard.append(temp)
    keyboard.append([KeyboardButton(Buttons.back.menu)])
    return ReplyKeyboardMarkup(
        row_width=2,
        resize_keyboard=True,
        one_time_keyboard=True,
        keyboard=keyboard
    )


def caffe_info_kb(is_admin: bool = False):
    keyboard = [
        [KeyboardButton(Buttons.menu.comment)]
    ]
    if is_admin:
        keyboard.append([KeyboardButton(Buttons.admin.statistic)])
    keyboard.append([KeyboardButton(Buttons.back.caffe)])
    return ReplyKeyboardMarkup(
        row_width=2,
        resize_keyboard=True,
        one_time_keyboard=True,
        keyboard=keyboard
    )


starts_kb = ReplyKeyboardMarkup(
        row_width=2,
        resize_keyboard=True,
        one_time_keyboard=True,
        keyboard=[
            [KeyboardButton('⭐')],
            [KeyboardButton('⭐⭐⭐')],
            [KeyboardButton('⭐⭐⭐⭐⭐')],
            [KeyboardButton(Buttons.back.caffe)]
        ]
    )
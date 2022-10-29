from app.keyboards.reply.base import *

menu_kb = ReplyKeyboardMarkup(
    row_width=2,
    one_time_keyboard=True,
    resize_keyboard=True,
    keyboard=[
        [
            KeyboardButton(Buttons.menu.my_qrcode)
        ],
        [
            KeyboardButton(Buttons.user.sales),
            KeyboardButton(Buttons.user.friend),
        ],
        [
            KeyboardButton(Buttons.user.how_to_use),
            KeyboardButton(Buttons.user.how_to_get)
        ],
        [
            KeyboardButton(Buttons.menu.our_caffe)
        ]
    ]
)

back_kb = ReplyKeyboardMarkup(
    row_width=1,
    one_time_keyboard=True,
    resize_keyboard=True,
    keyboard=[
        [KeyboardButton(Buttons.back.menu)]
    ]
)

__all__ = (
    'menu_kb',
    'back_kb'
)

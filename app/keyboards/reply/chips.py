from app.keyboards.reply.base import *

chips_action_kb = ReplyKeyboardMarkup(
    row_width=2,
    one_time_keyboard=True,
    resize_keyboard=True,
    keyboard=[
        [
            KeyboardButton(Buttons.chips.increment_chips),
        ],
        [
            KeyboardButton(Buttons.chips.decrement_chips)
        ]
    ]
)

chips_kb = ReplyKeyboardMarkup(
    row_width=2,
    resize_keyboard=True,
    one_time_keyboard=True,
    keyboard=[
        [KeyboardButton('1'), KeyboardButton('2')],
        [KeyboardButton('3'), KeyboardButton('6')],
        [KeyboardButton('10'), KeyboardButton('15')],
        [KeyboardButton(Buttons.back.menu)]
    ]
)

chips_minus_kb = ReplyKeyboardMarkup(
    row_width=2,
    resize_keyboard=True,
    one_time_keyboard=True,
    keyboard=[
        [KeyboardButton('6')],
        [KeyboardButton('10'), KeyboardButton('15')],
        [KeyboardButton(Buttons.back.menu)]
    ]
)

__all__ = (
    'chips_action_kb',
)

from app.keyboards.reply.base import *
from app.models.caffe import Caffe

admin_kb = ReplyKeyboardMarkup(
    row_width=2,
    resize_keyboard=True,
    one_time_keyboard=True,
    keyboard=[
        [
            KeyboardButton(Buttons.admin.add_barista),
            KeyboardButton(Buttons.admin.del_barista)
        ],
        [
            KeyboardButton(Buttons.admin.add_caffe),
            KeyboardButton(Buttons.admin.message)
        ],
        [
            KeyboardButton(Buttons.admin.edit_text)
        ]
    ]
)

bool_rp_kb = ReplyKeyboardMarkup(
    row_width=2,
    resize_keyboard=True,
    one_time_keyboard=True,
    keyboard=[
        [KeyboardButton(Buttons.bool.true)],
        [KeyboardButton(Buttons.bool.false)]
    ]
)

false_kb = ReplyKeyboardMarkup(
    row_width=2,
    resize_keyboard=True,
    one_time_keyboard=True,
    keyboard=[
        [KeyboardButton(Buttons.bool.false)]
    ]
)

edit_text_kb = ReplyKeyboardMarkup(
    row_width=2,
    resize_keyboard=True,
    one_time_keyboard=True,
    keyboard=[
        [KeyboardButton(Buttons.user.how_to_get), KeyboardButton(Buttons.user.how_to_use)],
        [KeyboardButton(Buttons.user.sales), KeyboardButton(Buttons.user.friend)],
        [KeyboardButton(Buttons.admin.caffe)],
        [KeyboardButton(Buttons.back.admin)]
    ]
)

edit_caffe_kb = ReplyKeyboardMarkup(
    row_width=2,
    resize_keyboard=True,
    one_time_keyboard=True,
    keyboard=[
        [KeyboardButton(Buttons.admin.name), KeyboardButton(Buttons.admin.description)],
        [KeyboardButton(Buttons.admin.location)],
        [KeyboardButton(Buttons.back.admin)]
    ]
)


def barista_kb(caffe: Caffe):
    name = f'📍 {caffe.name}' if caffe is not None else '📍 Заклад не обрано'
    return ReplyKeyboardMarkup(
        row_width=2,
        resize_keyboard=True,
        one_time_keyboard=True,
        keyboard=[
            [KeyboardButton(Buttons.chips.caffe)],
            [KeyboardButton(name)]
        ]
    )

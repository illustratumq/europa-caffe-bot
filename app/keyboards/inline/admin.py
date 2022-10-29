from app.keyboards.inline.base import *


add_barista_cb = CallbackData('add', 'action', 'user_id')


def bool_kb(user_id: int):
    return InlineKeyboardMarkup(
        row_width=1,
        inline_keyboard=[
            [InlineKeyboardButton(Buttons.admin.true, callback_data=add_barista_cb.new(
                action='true', user_id=user_id
            ))],
            [InlineKeyboardButton(Buttons.admin.false, callback_data=add_barista_cb.new(
                action='false', user_id=user_id
            ))]
        ]
    )
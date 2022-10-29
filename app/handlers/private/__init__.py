from aiogram import Dispatcher

from app.handlers.private import (
    start,
    chips,
    info,
    admin,
    caffe,
    text
)


def setup(dp: Dispatcher):
    chips.setup(dp)
    start.setup(dp)
    caffe.setup(dp)
    admin.setup(dp)
    text.setup(dp)
    info.setup(dp)




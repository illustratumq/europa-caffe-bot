from app.states.base import *


class AddBaristaSG(StatesGroup):
    Reply = State()
    Confirm = State()


class AddCaffeSG(StatesGroup):
    Name = State()
    Description = State()
    Location = State()
    Confirm = State()


class BaristaSG(StatesGroup):
    Action = State()
    Decrement = State()
    Increment = State()


class DelBaristaSG(StatesGroup):
    Confirm = State()


class EditTextSG(StatesGroup):
    Choose = State()
    Input = State()
    Caffe = State()
    CaffeInput = State()
    CaffeCategory = State()


class CaffeChooseSG(StatesGroup):
    Choose = State()


class MessageSG(StatesGroup):
    Text = State()
    Button = State()
    Confirm = State()


class CaffeSG(StatesGroup):
    Input = State()
    Static = State()
    Stars = State()


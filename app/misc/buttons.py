from dataclasses import dataclass


@dataclass
class BoolButtons:
    true: str = 'Підтвердити ✅'
    false: str = 'Скасувати ❌'


@dataclass
class AdminButtons:
    add_barista: str = 'Додати баристу ➕'
    del_barista: str = 'Вилучити баристу ➖'
    add_caffe: str = 'Додати заклад ☕'
    message: str = 'Зробити повідомлення 📬'
    edit_text: str = 'Редагувати текст 📝'
    true: str = 'Так, додати ✅'
    false: str = 'Ні, відхилити ❌'
    caffe: str = 'Заклади'
    name: str = 'Назва'
    description: str = 'Опис'
    location: str = 'Адреса'
    statistic: str = 'Статистика 📊'


@dataclass
class BackButtons:
    menu: str = '◀ До головного меню'
    caffe: str = '◀ До закладів'
    admin: str = '◀ Назад'


@dataclass
class UserButtons:
    how_to_use: str = 'Як використати фішки 💛'
    how_to_get: str = 'Як отримати фішки 💙'
    friend: str = 'Запросити друга 🤍'
    sales: str = 'Наші акції 💚'


@dataclass
class MenuButtons:
    my_qrcode: str = '❤ Мій QR-код ❤'
    our_caffe: str = '☕ Наші заклади ☕'
    comment: str = 'Залишити відгук 💬'


@dataclass
class ChipsButtons:
    increment_chips: str = '➕ Нарахувати фішки ➕'
    decrement_chips: str = '➖ Списати фішки ➖'
    caffe: str = 'Змінити заклад'


@dataclass
class Buttons:
    menu: MenuButtons = MenuButtons()
    chips: ChipsButtons = ChipsButtons()
    user: UserButtons = UserButtons()
    back: BackButtons = BackButtons()
    admin: AdminButtons = AdminButtons()
    bool: BoolButtons = BoolButtons()




import logging

from aiogram import Bot

log = logging.getLogger(__name__)


async def notify(bot: Bot, admin_ids: tuple[int, ...]) -> None:
    for admin in admin_ids:
        try:
            await bot.send_message(admin, 'Бот запущен')
        except Exception as err:
            log.exception(err)

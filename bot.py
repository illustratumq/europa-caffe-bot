import asyncio
import logging

from aiogram import Bot, Dispatcher
from aiogram.contrib.fsm_storage.redis import RedisStorage2
from aiogram.types import AllowedUpdates, ParseMode

from app import filters, handlers, middlewares
from app.config import Config
from app.misc.bot_commands import set_default_commands
from app.misc.notify_admins import notify
from app.misc.text import TextCloud
from app.services import create_db_engine_and_session_pool


log = logging.getLogger(__name__)


async def main():
    config = Config.from_env()
    log_level = config.misc.log_level
    logging.basicConfig(
        level=log_level,
        format=u'%(filename)s:%(lineno)d #%(levelname)-8s [%(asctime)s] - %(name)s - %(message)s',
    )
    log.info('Starting bot...')

    storage = RedisStorage2(host=config.redis.host, port=config.redis.port)
    bot = Bot(config.bot.token, parse_mode=ParseMode.HTML)
    dp = Dispatcher(bot, storage=storage)
    db_engine, sqlalchemy_session_pool = await create_db_engine_and_session_pool(config.db.sqlalchemy_url, log_level)

    allowed_updates = (
            AllowedUpdates.MESSAGE + AllowedUpdates.CALLBACK_QUERY +
            AllowedUpdates.EDITED_MESSAGE
    )
    environments = dict(config=config,  dp=dp, text_cloud=TextCloud)

    middlewares.setup(dp, environments, sqlalchemy_session_pool)
    filters.setup(dp)
    handlers.setup(dp)

    await set_default_commands(bot)
    await notify(bot, config.bot.admin_ids)

    try:
        await dp.skip_updates()
        await dp.start_polling(allowed_updates=allowed_updates, reset_webhook=True)
    finally:
        await storage.close()
        await storage.wait_closed()
        await (await bot.get_session()).close()
        await db_engine.dispose()

if __name__ == '__main__':
    try:
        asyncio.run(main())
    except (KeyboardInterrupt, SystemExit):
        log.warning('Bot stopped!')

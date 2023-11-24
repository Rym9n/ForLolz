from aiogram import executor, Dispatcher, types
from handlers import dp

from utils import db


async def on_sturtup(dp: Dispatcher):
    '''
    Функция on_sturtup срабатывает при запуске бота

    :return:None
    '''

    await db.create_tables() # Создание таблиц в базе данных при запуске бота

    await dp.bot.set_my_commands(
        [
            types.BotCommand(
                'start', 'Перезагрузить меню'
            )
        ]
    )

    print('Бот запущен!')


if __name__ == '__main__':
    executor.start_polling(dp, on_startup=on_sturtup)

import aiosqlite
from data import config


# Класс для взаимодействия с базой данных
class DataBase:
    def __init__(self, database_name):
        # Инциализация создания класса
        self.db_name = database_name

    # Работа с БД
    async def create_tables(self): # Создание таблиц
        '''
        Функция create_tables создает таблицы в базе данных если их не существует

        '''

        async with aiosqlite.connect(self.db_name) as db:
            await db.execute(
                'CREATE TABLE IF NOT EXISTS notes ('
                'id INTEGER PRIMARY KEY AUTOINCREMENT,'
                f'title VARCHAR({config.title_limit}),'
                'content TEXT,'
                'tg_id VARCHAR(120))'
            )

    # Работа с заметками
    async def create_note(self, title, content, tg_id): # Создание заметки
        '''
        Функция create_note создает заметку в базе данных

        ::param title: Название заголовка
        ::param content: Содержимое заметки
        ::param tg_id: Уникальный Telegram ID пользователя
        :return:None
        '''

        async with aiosqlite.connect(self.db_name) as db:
            await db.execute(
                'INSERT INTO notes (title, content, tg_id) VALUES (?, ?, ?)', 
                (title, content, tg_id)
            )
            await db.commit()

    async def get_user_notes(self, tg_id):  # Получение заметок пользователя
        '''
        Функция get_user_notes получает все заметки определенного пользователя из базы данных

        ::param tg_id: Уникальный Telegram ID
        :return: Сгенерированный SQL-запрос
        '''

        async with aiosqlite.connect(self.db_name) as db:
            async with db.execute('SELECT * FROM notes WHERE tg_id = ?', (tg_id, )) as cursor:
                return await cursor.fetchall()


    async def get_note_by_id(self, note_id):  # Получение заметок по ID
        '''
        Функция get_note_by_id получает заметку по ее ID в базе данных

        ::param note_id: Уникальный ID заметки
        :return: Сгенерированный SQL-запрос
        '''

        async with aiosqlite.connect(self.db_name) as db:
            async with db.execute('SELECT * FROM notes WHERE id = ?', (note_id, )) as cursor:
                return await cursor.fetchone()


    async def find_note_title(self, value, tg_id):  # Поиск заметок по названию
        '''
        Функция find_note_title ищет заметки пользователя по названию

        ::param value: Искомый аргумент
        ::param tg_id: Уникальный Telegram ID
        :return: Сгенерированный SQL-запрос
        '''

        async with aiosqlite.connect(self.db_name) as db:
            async with db.execute(
                'SELECT * FROM notes WHERE lower(title) LIKE ? AND tg_id = ?', 
                (f'%{value}%'.lower(), tg_id)
            ) as cursor:
                return await cursor.fetchall()


    async def find_note_content(self, value, tg_id):  # Поиск заметок по содержанию
        '''
        Функция find_note_content ищет заметки пользователя в содержании

        ::param value: Искомый аргумент
        ::param tg_id: Уникальный Telegram ID
        :return: Сгенерированный SQL-запрос
        '''

        async with aiosqlite.connect(self.db_name) as db:
            async with db.execute(
                'SELECT * FROM notes WHERE lower(content) LIKE ? AND tg_id = ?', 
                (f'%{value}%'.lower(), tg_id)
            ) as cursor:
                return await cursor.fetchall()


    async def delete_note(self, note_id):  # Удаление заметки
        '''
        Функция delete_note удаляет заметку из базы данных по уникальному ID заметки

        ::param note_id: Уникальный ID заметки
        :return: None
        '''

        async with aiosqlite.connect(self.db_name) as db:
            await db.execute('DELETE FROM notes WHERE id = ?', (note_id, ))
            await db.commit()


db_class = DataBase('ForLolz.sqlite')

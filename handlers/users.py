from loader import dp
from aiogram.dispatcher.filters.builtin import CommandStart
from aiogram.dispatcher import FSMContext
from aiogram import types

from keyboards.default import get_menu_keyboard
from keyboards.inline import (
    get_my_notes_keyboard, get_note_keyboard,
    get_find_notes_keyboard
)

from states import NoteAddStorage, FindNoteStorage
from utils import db
from data import config


# /start
@dp.message_handler(CommandStart(), state='*')
async def bot_start(message: types.Message, state:FSMContext):
    await state.finish()

    await message.answer(
        'Добро пожаловать в бот "Заметки"\n'
        'Пожалуйста воспользуйтесь меню ниже',
        reply_markup=get_menu_keyboard()
    )


# Добавить заметку
@dp.message_handler(text='Добавить заметку', state='*')
async def add_note(message: types.Message, state: FSMContext):
    await state.finish()

    await NoteAddStorage.title.set()

    await message.answer(
        'Введите название заметки:'
    )


@dp.message_handler(state=NoteAddStorage.title) # Добавление заголовка
async def add_note_title(message: types.Message, state: FSMContext):
    # Если длина меньше установленной в конфигурации, то выводим ошибку
    if len(message.text) > config.title_limit:
        return await message.answer(
            f'Длина заголовка не может быть больше {config.title_limit} символов!'
        )

    async with state.proxy() as data:
        data['title'] = message.text

    await NoteAddStorage.next()

    await message.answer(
        'Введите содержание заметки'
    )


@dp.message_handler(state=NoteAddStorage.content) # Добавление содержания
async def add_note_content(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        # Создание заметки
        await db.create_note(data['title'], message.text, message.from_user.id)

    await state.finish()

    await message.answer(
        'Заметка добавлена!'
    )


# Мои заметки
@dp.message_handler(text='Мои заметки', state='*')
async def my_notes(message: types.Message , state: FSMContext):
    await state.finish()

    notes = await db.get_user_notes(message.from_user.id)

    await message.answer(
        'Список ваших заметок:',
        reply_markup=get_my_notes_keyboard(notes)
    )


@dp.callback_query_handler(text='my_notes', state='*') # Мои заметки вызванные CallBackQuery
async def my_notes_callback(call: types.CallbackQuery , state: FSMContext):
    await state.finish()

    notes = await db.get_user_notes(call.from_user.id)

    await call.message.edit_text(
        'Список ваших заметок:',
        reply_markup=get_my_notes_keyboard(notes)
    )


# Информация о заметки
@dp.callback_query_handler(text_startswith='n:', state='*')
async def note_info(call: types.CallbackQuery, state: FSMContext):
    await state.finish()

    note_id = call.data.split(':')[1]
    note = await db.get_note_by_id(note_id)

    await call.message.edit_text(
        f'ID заметки: {note[0]}\n\n'
        f'Заголовок: {note[1]}\n\n'
        f'Содержание:\n{note[2]}',
        reply_markup=get_note_keyboard(note_id)
    )


# Удаление заметки
@dp.callback_query_handler(text_startswith='dn:', state='*')
async def delete_note(call: types.CallbackQuery, state: FSMContext):
    await state.finish()

    await db.delete_note(call.data.split(':')[1])

    await my_notes_callback(call, state)


# Поиск заметок
@dp.message_handler(text='Поиск заметок', state='*')
async def find_notes(message: types.Message , state: FSMContext):
    await state.finish()

    await message.answer(
        'Как будем искать заметку?',
        reply_markup=get_find_notes_keyboard()
    )


@dp.callback_query_handler(text_startswith='find:', state='*') # Выбор типа поиска заметки
async def find_notes_choice(call: types.CallbackQuery, state: FSMContext):
    await state.finish()

    await FindNoteStorage.value.set()

    async with state.proxy() as data:
        data['choice'] = call.data.split(':')[1]

    await call.message.edit_text(
        'Введите слова для поиска:'
    )


@dp.message_handler(state=FindNoteStorage.value)
async def find_note_value(message: types.Message, state: FSMContext):
    data = await state.get_data()
    await state.finish()

    if data['choice'] == 'title': # Если тип поиска по названию, ищем по названию
        notes = await db.find_note_title(message.text, message.from_user.id)
    else: # Иначе ищем по содержанию
        notes = await db.find_note_content(message.text, message.from_user.id)

    await message.answer(
        'Список найденных заметок:',
        reply_markup=get_my_notes_keyboard(notes)
    )

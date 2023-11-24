from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup


def get_my_notes_keyboard(notes):
    '''
    Функция get_my_notes_keyboard создает клавиатуру меню 

    ::param notes: Список заметок сгенерированный SQL запросом
    :return:InlineKeyboardMarkup
    '''

    keyboard = InlineKeyboardMarkup(row_width=1)

    for note in notes:
        keyboard.add(
            InlineKeyboardButton(
                text = note[1],
                callback_data=f'n:{note[0]}'
            )
        )

    return keyboard


def get_note_keyboard(note_id):
    '''
    Функция get_note_keyboard создает клавиатуру для заметки 

    ::param note_id: Уникальный ID заметки
    :return:InlineKeyboardMarkup
    '''

    keyboard = InlineKeyboardMarkup(row_width=1)

    keyboard.add(
        InlineKeyboardButton(
            text='Удалить заметку',
            callback_data=f'dn:{note_id}'
        ),
        InlineKeyboardButton(
            text='Назад',
            callback_data='my_notes'
        )
    )

    return keyboard


def get_find_notes_keyboard():
    '''
    Функция get_find_notes_keyboard создает клавиатуру для поиска заметок 

    :return:InlineKeyboardMarkup
    '''

    keyboard = InlineKeyboardMarkup(row_width=1)

    keyboard.add(
        InlineKeyboardButton(
            text='Поиск заметки по заголовку',
            callback_data='find:title'
        ),
        InlineKeyboardButton(
            text='Поиск заметки по содержанию',
            callback_data='find:content'
        )
    )

    return keyboard

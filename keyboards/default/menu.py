from aiogram.types import ReplyKeyboardMarkup


def get_menu_keyboard():
    '''
    Функция get_menu_keyboard создает клавиатуру меню 

    :return:ReplyKeyboardMarkup
    '''

    keyboard = ReplyKeyboardMarkup(resize_keyboard=True)

    keyboard.add('Добавить заметку')
    keyboard.add('Мои заметки')
    keyboard.add('Поиск заметок')

    return keyboard

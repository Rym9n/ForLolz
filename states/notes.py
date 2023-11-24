from aiogram.dispatcher.filters.state import State, StatesGroup

class NoteAddStorage(StatesGroup):
    title = State()
    content = State()


class FindNoteStorage(StatesGroup):
    value = State()

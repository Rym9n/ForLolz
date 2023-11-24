import configparser


# Создание класса для работы с конфигурацией
class Config:
    def __init__(self, config_file):
        self.config = configparser.ConfigParser()
        self.config_file = config_file
        self.read_config()


    # Читание конфига
    def read_config(self):
        self.config.read(self.config_file, encoding='utf-8')

        self.token = self.config['settings']['bot_token']
        self.title_limit = self.config['settings']['title_limit']

        if not(self.title_limit.isdigit()): # Если лимит названия не число
            raise TypeError('Введите лимит заголовка в конфиге числом!')

        self.title_limit = int(self.title_limit)


config = Config('config.ini')

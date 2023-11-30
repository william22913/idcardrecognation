import json


class I18N:
    def __init__(self):
        self.data = load_translation()

    def read_message(self, language, message):
        try:
            if self.data.get(language).get(message) is not None:
                return self.data.get(language).get(message)
            else:
                return message
        except:
            return message


def load_translation():
    file_load = ['error/en-US.json', 'error/id-ID.json']
    result = {}
    for i in file_load:
        lang = i.split('/')
        lang = lang[1].split('.')[0]
        try:
            with open(f'locale/{i}', 'r', encoding='utf-8') as file:
                result[lang] = json.load(file)
        except FileNotFoundError:
            print(f"Translation file not found for language '{i}'. Using default.")
            return {}

    return result


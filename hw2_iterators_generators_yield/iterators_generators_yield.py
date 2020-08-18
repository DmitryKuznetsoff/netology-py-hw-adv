import json
import hashlib


def md5_gen(file):
    with open(file, 'r', encoding='utf-8') as f:
        for line in f:
            yield hashlib.md5(line.encode()).hexdigest()


class CountriesIterator:
    def __init__(self, json_file):
        self.json_file = json_file
        self.content_for_write_file = self.get_content_for_write_file()

    def __iter__(self):
        return self

    def __next__(self):
        country, wiki_link = next(self.content_for_write_file)
        # строка для записи в файл:
        string = f'{country} -- {wiki_link}'
        with open('file.txt', 'a', encoding='utf-8') as f:
            f.write(string + '\n')
        # можно было и не возвращать строку.
        # это сделано просто для удобства отслеживания работы метода:
        return string

    def get_content_for_write_file(self):
        with open(self.json_file, 'r', encoding='utf-8') as f:
            json_file = json.load(f)
            # собираем названия стран в список countries:
            countries = [country_name['name']['common'] for country_name in json_file]
            # заменяем пробелы на "_", добавляем перед названием url и формируем список wiki_link:
            wiki_link = list(map(lambda x: 'https://en.wikipedia.org/wiki/' + x.replace(' ', '_'), countries))
        # с помощью функции zip создаём zip-объект с парами страна -- ссылка и возвращаем его:
        return zip(countries, wiki_link)


if __name__ == '__main__':
    obj = CountriesIterator('countries.json')
    gen = md5_gen('file.txt')
    print(next(obj))
    print(next(gen))
    print('---------------------------------')
    print(next(obj))
    print(next(gen))
    print('---------------------------------')
    print(next(obj))
    print(next(gen))

import requests
import datetime
import time
from pprint import pprint


def logger(log_file):
    """
    декоратор. принимает на вход путь к файлу с логами log_file
    в который в дальнейшем будет производиться запись
    """

    def get_logs(f):
        """
        декоратор. принимает на вход функцию и пишет в файл log_file дату и время
        выполнения функции, аргументы и возвращаемое функцией значение
        """

        def wrapper(*args):
            result = f(*args)
            pprint(result)
            with open(log_file, 'a', encoding='utf-8') as write_file:
                write_file.write(f'date: {datetime.datetime.now()} -- args: {args} -- return value: {result}\n')
            return

        return wrapper

    return get_logs


@logger('logs.txt')
def get_questions_from_stackoverflow(tag, n):
    """функция возвращает вопросы на stackoverflow с тэгом tag за прошедшие n дней:"""
    today = datetime.date.today()
    today_unix_date = int(time.mktime(today.timetuple()))
    # дата unix n дней назад:
    fromdate = today_unix_date - 86400 * n

    url = 'https://api.stackexchange.com/2.2/questions'

    params = {'page': 1,
              'pagesize': 100,
              'fromdate': fromdate,
              'todate': today_unix_date,
              'order': 'desc',
              'sort': 'creation',
              'tagged': tag,
              'site': 'stackoverflow'
              }

    result = []

    while True:
        r = requests.get(url, params=params)
        r_dict = r.json()
        # если на странице нет вопросов, останавливаем цикл:
        if not r_dict.get('items'):
            break
        else:
            for questions in r_dict.get('items'):
                # получаем дату создания вопроса в читабельном формате:
                date = questions.get('creation_date')
                date = datetime.datetime.fromtimestamp(date).strftime('%Y-%m-%d %H:%M:%S')
                # формируем словарь с датой вопроса, заголовком и ссылкой на вопрос:
                questions_on_page = {'date': date, 'title': questions.get('title'), 'link': questions.get('link')}
                result.append(questions_on_page)
        params['page'] += 1
    return result


if __name__ == "__main__":
    get_questions_from_stackoverflow('python', 1)
from bs4 import BeautifulSoup
import requests
import re
from dataclasses import dataclass
from typing import List


@dataclass
class Post:
    """
    Класс, содеражий информацию о статье на харбе
    """
    author: str
    date: str
    title: str
    link: str
    hubs: List[str]
    preview_text: str

    def __str__(self):
        """
        Метод для вывода информации о статье по примеру из дз
        """
        return f'{self.date} -- {self.title} -- {self.link}'

    def get_post_text(self):
        """
        Возвращает текст статьи
        """
        post_page = requests.get(self.link)
        soup = BeautifulSoup(post_page.text, 'html.parser')
        # ищем текст по классу css:
        text = soup.select('[class~=post__text]')
        return text[0].text


def get_post_info_from_preview(page_url):
    """
    Принимает на вход url страницы для парсинга.
    Возвращает список объектов класса Post для каждой из статей на странице
    """
    # регулярное выражение для поиска по post_id:
    post_id = re.compile(r'post_\d')
    page = requests.get(page_url)
    soup = BeautifulSoup(page.text, 'html.parser')
    # ищем посты по идентификатору id:
    posts = soup.find_all(id=post_id)
    result = []
    for post in posts:
        # ищем информацию о статье по классам css:
        title = post.select('[class~=post__title_link]')
        hubs = [hub.text for hub in post.select('[class~=hub-link]')]
        preview_text = post.select('[class~=post__text]')
        author = post.select('[class~=user-info__nickname_small]')
        date = post.select('[class~=post__time]')
        if title:
            # создаём объект класса Post для каждой статьи по указанному page_url и возвращаем список объектов:
            result.append(
                Post(author[0].text, date[0].text, title[0].text, title[0]['href'], hubs, preview_text[0].text))
    return result


def get_post_by_tags(tags, posts):
    """
    Принимает на вход список тэгов и объектов класса Post
    Ищет совпадения тэгов с информацией о статье и её содержимым
    Возвращает список статей, в которых упоминаются тэги
    """
    # приводим список хабов, текст заголовка, превью и статьи к нижнему регистру
    # и выбираем статьи с совпадениями в KEYWORDS:
    result = [post for post in posts
              if set(tags) & set(map(str.lower, post.hubs))
              or set(tags) & set(map(str.lower, post.title.split()))
              or set(tags) & set(map(str.lower, post.preview_text.split()))
              # хз надо ли искать совпадения в тексте статьи, написал просто на всякий случай:
              # or set(tags) & set(map(str.lower, post.get_post_text().split()))
              ]
    return result


if __name__ == '__main__':
    url = 'https://habr.com/ru/all/'
    KEYWORDS = ['дизайн', 'фото', 'web', "python"]
    # приводим KEYWORDS к нижнему регистру:
    kw_lowercase = list(map(str.lower, KEYWORDS))
    posts_by_tags = get_post_by_tags(kw_lowercase, get_post_info_from_preview(url))
    for post in posts_by_tags:
        print(post)

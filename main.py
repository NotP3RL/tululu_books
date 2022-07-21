import argparse
import logging
import os
from time import sleep

import requests
import urllib
from bs4 import BeautifulSoup
from pathvalidate import sanitize_filename

BOOKS_PATH = './books'
IMAGES_PATH = './images'


def check_for_redirect(response):
    if response.url == 'https://tululu.org/':
        raise requests.exceptions.HTTPError


def download_text(book_id, title):
    url = f'https://tululu.org/txt.php'
    params = {'id': book_id}
    response = requests.get(url, params=params)
    response.raise_for_status()
    check_for_redirect(response)
    filename = f'{book_id}. {sanitize_filename(title)}.txt'
    filepath = os.path.join(BOOKS_PATH, filename)
    with open(filepath, 'wb') as file:
        file.write(response.content)


def download_image(image_url):
    response = requests.get(image_url)
    response.raise_for_status()
    check_for_redirect(response)
    filename = urllib.parse.urlsplit(image_url, allow_fragments=True).path.split('/')[-1]
    filepath = os.path.join(IMAGES_PATH, filename)
    with open(filepath, 'wb') as file:
        file.write(response.content)


def parse_book_page(response):
    soup = BeautifulSoup(response.text, 'lxml')
    book_info = soup.find(id='content').find('h1').text
    book_image = soup.find(class_='bookimage').find('img')['src']
    book_comments_soup = soup.select("div.texts span.black")
    book_genres_soup = soup.select("span.d_book a")
    title, author = book_info.split('::')
    book_image_url = urllib.parse.urljoin(response.url, book_image)
    book_comments = [book_comment_soup.text for book_comment_soup in book_comments_soup]
    book_genres = [book_genre_soup.text for book_genre_soup in book_genres_soup]
    book_params = {
        'title': title.strip(),
        'author': author.strip(),
        'image_url': book_image_url,
        'comments': book_comments,
        'genres': book_genres
    }
    return book_params


if __name__ == "__main__":
    os.makedirs(BOOKS_PATH, exist_ok=True)
    os.makedirs(IMAGES_PATH, exist_ok=True)
    parser = argparse.ArgumentParser(
        description='Парсер tululu'
    )
    parser.add_argument("start_page", help="номер первой страницы категории", default=1, nargs="?", type=int)
    parser.add_argument("end_page", help="номер последней страницы категории", default=1, nargs="?", type=int)
    args = parser.parse_args()
    start_page = args.start_page
    end_page = args.end_page + 1
    for book_id in range(start_page, end_page):
        while True:
            try:
                url = f'https://tululu.org/b{book_id}'
                response = requests.get(url)
                response.raise_for_status()
                check_for_redirect(response)
                book_params = parse_book_page(response)
                download_image(book_params['image_url'])
                download_text(book_id, book_params['title'])
                print(f'Скачалась книга с id №{book_id}')
                break
            except requests.exceptions.HTTPError:
                logging.warning(f'Не удалось скачать книгу с id №{book_id}')
                break
            except requests.exceptions.ConnectionError:
                logging.error('Подключение прерванно')
                sleep(5)
                logging.error('Пытаюсь произвести скачивание снова')
            except requests.exceptions.ReadTimeout:
                logging.error('Время ожидания ответа истекло')

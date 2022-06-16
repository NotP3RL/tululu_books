import os

from bs4 import BeautifulSoup
import requests
from pathvalidate import sanitize_filename

DIR_PATH = './books'


def check_for_redirect(response):
    if response.url == 'https://tululu.org/':
        raise requests.exceptions.HTTPError

def get_book_info(response, id):
    soup = BeautifulSoup(response.text, 'lxml')
    book_info = soup.find(id='content').find('h1').text
    title, writer = book_info.split('::')
    title = title[:len(title)-3:]
    book_info = {
        'title': title,
        'writer': writer
    }
    return book_info

def download_text(id, title):
    url = f'https://tululu.org/txt.php?id={id}'
    response = requests.get(url)
    response.raise_for_status()
    check_for_redirect(response)
    filename = f'{id}. {sanitize_filename(title)}.txt'
    filepath = os.path.join(DIR_PATH, filename)
    with open(filepath, 'wb') as file:
        file.write(response.content)


if __name__ == "__main__":
    os.makedirs(DIR_PATH, exist_ok=True)
    for id in range(1, 11):
        try:
            url = f'https://tululu.org/b{id}'
            response = requests.get(url)
            response.raise_for_status()
            check_for_redirect(response)
            book_info = get_book_info(response, id)
            download_text(id, book_info['title'])
        except requests.exceptions.HTTPError:
            continue

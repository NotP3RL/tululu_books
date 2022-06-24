import os

from bs4 import BeautifulSoup
import urllib
import requests
from pathvalidate import sanitize_filename

BOOKS_PATH = './books'
IMAGES_PATH = './images'


def check_for_redirect(response):
    if response.url == 'https://tululu.org/':
        raise requests.exceptions.HTTPError

def get_book_info(response):
    soup = BeautifulSoup(response.text, 'lxml')
    book_info = soup.find(id='content').find('h1').text
    title, writer = book_info.split('::')
    title = title[:len(title)-3:]
    book_info = {
        'title': title,
        'writer': writer
    }
    return book_info

def get_book_image_url(response):
    soup = BeautifulSoup(response.text, 'lxml')
    book_image = soup.find(class_='bookimage').find('img')['src']
    book_image_url = urllib.parse.urljoin('https://tululu.org/', book_image)
    return book_image_url

def get_book_comments(response):
    soup = BeautifulSoup(response.text, 'lxml')
    book_comments_soup = soup.find_all(class_='texts')
    book_comments = []
    for book_comment_soup in book_comments_soup:
        book_comment = book_comment_soup.find(class_='black').text
        book_comments.append(book_comment)
    return book_comments

def get_book_genres(response):
    soup = BeautifulSoup(response.text, 'lxml')
    book_genres_soup = soup.select("span.d_book a")
    book_genres = []
    for book_genre_soup in book_genres_soup:
        book_genre = book_genre_soup.text
        book_genres.append(book_genre)
    return book_genres

def download_text(id, title):
    url = f'https://tululu.org/txt.php?id={id}'
    response = requests.get(url)
    response.raise_for_status()
    check_for_redirect(response)
    filename = f'{id}. {sanitize_filename(title)}.txt'
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


if __name__ == "__main__":
    os.makedirs(BOOKS_PATH, exist_ok=True)
    os.makedirs(IMAGES_PATH, exist_ok=True)
    for id in range(1, 11):
        try:
            url = f'https://tululu.org/b{id}'
            response = requests.get(url)
            response.raise_for_status()
            check_for_redirect(response)
            book_image_url = get_book_image_url(response)
            download_image(book_image_url)
            book_info = get_book_info(response)
            print(f'Заголовок: {book_info["title"]}', '\n')
            print(get_book_genres(response))
            download_text(id, book_info['title'])
        except requests.exceptions.HTTPError:
            continue

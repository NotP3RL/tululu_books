import json
import logging

import requests
from urllib.parse import urljoin
from bs4 import BeautifulSoup

from main import download_text, download_image, parse_book_page


books_payload = []

for page in range(1, 5):
    try:
        url = urljoin('https://tululu.org/l55/', str(page))
        response = requests.get(url)
        soup = BeautifulSoup(response.text, 'lxml')
        book_cards = soup.select('div.bookimage a')
        try:
            for book_card in book_cards:
                book_url = urljoin('http://tululu.org/', book_card['href'])
                response = requests.get(book_url)
                response.raise_for_status()
                book_params = parse_book_page(response)
                book_id = book_card['href'].replace('b', '').replace('/', '')
                download_image(book_params['image_url'])
                download_text(book_id, book_params['title'])
                books_payload.append(book_params)
        except requests.exceptions.HTTPError:
            logging.exception('Ошибка')
    except requests.exceptions.HTTPError:
        logging.exception('Ошибка')


with open('books_payload.json', 'w', encoding='UTF-8') as my_file:
    json.dump(books_payload, my_file, ensure_ascii=False)
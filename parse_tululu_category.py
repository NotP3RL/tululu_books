import argparse
import json
import logging

import requests
from urllib.parse import urljoin
from bs4 import BeautifulSoup

from main import check_for_redirect, download_text, download_image, parse_book_page


if __name__ == "__main__":
    books_payload = []
    parser = argparse.ArgumentParser(
        description='Парсер tululu'
    )
    parser.add_argument("start_page", help="номер первой страницы категории", default=1, nargs="?", type=int)
    parser.add_argument("end_page", help="номер последней страницы категории", default=1, nargs="?", type=int)
    args = parser.parse_args()
    start_page = args.start_page
    end_page = args.end_page + 1
    for page in range(start_page, end_page):
        try:
            url = urljoin('https://tululu.org/l55/', str(page))
            response = requests.get(url)
            response.raise_for_status()
            soup = BeautifulSoup(response.text, 'lxml')
            book_cards = soup.select('div.bookimage a')
            for book_card in book_cards:
                try:
                    book_url = urljoin('http://tululu.org/', book_card['href'])
                    response = requests.get(book_url)
                    response.raise_for_status()
                    check_for_redirect(response)
                    book_params = parse_book_page(response)
                    book_id = book_card['href'].replace('b', '').replace('/', '')
                    download_image(book_params['image_url'])
                    books_payload.append(book_params)
                    download_text(book_id, book_params['title'])
                except requests.exceptions.HTTPError:
                    logging.exception('Ошибка')
        except requests.exceptions.HTTPError:
            logging.exception('Ошибка')

    with open('books_payload.json', 'w', encoding='UTF-8') as my_file:
        json.dump(books_payload, my_file, ensure_ascii=False)

import os
import argparse
import json
import logging

import requests
from urllib.parse import urljoin
from bs4 import BeautifulSoup

from parse_tululu_books import check_for_redirect, download_text, download_image, parse_book_page


if __name__ == "__main__":
    books_payload = []
    parser = argparse.ArgumentParser(
        description='Парсер tululu'
    )
    parser.add_argument('start_page', help='номер первой страницы категории', default=1, nargs='?', type=int)
    parser.add_argument('end_page', help='номер последней страницы категории', default=1, nargs='?', type=int)
    parser.add_argument('--images_dir', help='путь к папке куда будут сохраняться обложки книг', default='images')
    parser.add_argument('--books_dir', help='путь к папке куда будут сохраняться книги', default='books')
    parser.add_argument('--json_dir', help='путь к папке куда будут сохраняться json со всеми книгами', default='')
    parser.add_argument('--skip_books', help='нужно ли скачивать книги (вводите True или False)', default=False, action='store_true')
    parser.add_argument('--skip_images', help='нужно ли скачивать обложки книг (вводите True или False)', default=False, action='store_true')
    args = parser.parse_args()
    start_page = args.start_page
    end_page = args.end_page + 1
    images_dir = args.images_dir
    books_dir = args.books_dir
    json_dir = args.json_dir
    skip_books = args.skip_books
    skip_images = args.skip_images

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
                    if not skip_images:
                        download_image(book_params['image_url'], images_dir)
                    books_payload.append(book_params)
                    if not skip_books:
                        download_text(book_id, book_params['title'], books_dir)
                except requests.exceptions.HTTPError:
                    logging.exception('Ошибка')
        except requests.exceptions.HTTPError:
            logging.exception('Ошибка')

    books_payload_path = os.path.join(json_dir, 'books_payload.json')
    with open(books_payload_path, 'w', encoding='UTF-8') as my_file:
        json.dump(books_payload, my_file, ensure_ascii=False)

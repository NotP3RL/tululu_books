import os
import json
from http.server import HTTPServer, SimpleHTTPRequestHandler

from jinja2 import Environment, FileSystemLoader, select_autoescape
from more_itertools import chunked


PAGES_PATH = './pages'


env = Environment(
    loader=FileSystemLoader('.'),
    autoescape=select_autoescape(['html', 'xml'])
)

template = env.get_template('template.html')

with open('books_payload.json', 'rb') as file:
    books_payload = json.load(file)

books_in_row = 2
books_rows = list(chunked(books_payload, books_in_row))
books_in_col = 5
pages = list(chunked(books_rows, books_in_col))

os.makedirs(PAGES_PATH, exist_ok=True)

for number, page in enumerate(pages, start=1):
    rendered_page = template.render(
        pages_count=len(pages),
        page=page,
        page_number=number
    )


    with open(f'pages/index{number}.html', 'w', encoding="utf8") as file:
        file.write(rendered_page)

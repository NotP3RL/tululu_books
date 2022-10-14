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

rendered_page = template.render(
    books_pairs=list(chunked(books_payload, 2))
)

os.makedirs(PAGES_PATH, exist_ok=True)
with open('pages/index.html', 'w', encoding="utf8") as file:
    file.write(rendered_page)

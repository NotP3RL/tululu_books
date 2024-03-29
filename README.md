# Парсер книг с сайта tululu.org

Данный проект создан для скачивания книг с обложками и остальными данными с сайта [tululu.org](https://tululu.org/).

[Пример страницы готовой библиотеки](https://notp3rl.github.io/tululu_books/pages/index1.html)
## Как установить

Для запуска необходим Python 3.*, который можно установить с [официального сайта](https://www.python.org/).

После скачивания архива с кодом его необходимо распаковать в пустую папку. После этого необходимо скачать все сторонние библиотеки, открыв папку в консоли и написав в неё:
```
pip install -r requirements.txt
```

## Как запустить
### Скачивание книг по ID
```
python parse_tululu_books.py START_PAGE END_PAGE
```
Вместо START_PAGE нужно указать ID начальной книги, с которой начнётся скачивание файлов, а за место END_PAGE нужно указать ID конечной книги, на которой скачивание файлов закончиться.

Текстовые файлы книг сохраняться в папку 'books', а файлы изображений обложек книг сохраняться в папку 'images'. Обе из этих папок находятся в корневой папке программы.

### Скачивание книг из категории научной фантастики
```
python parse_tululu_category.py START_PAGE_END_PAGE
```
Вместо START_PAGE нужно указать № начальной страницы, с которой начнётся скачивание файлов, а за место END_PAGE нужно указать № конечной книги, на которой скачивание файлов закончиться.

Также у parse_tululu_category.py есть необязательные аргументы, вот все из них:
```
--images_dir - путь куда будут скачиваться обложки книг (по умолчанию это папка images)
--books_dir - путь куда будут скачиваться книги (по умолчанию это папка books)
--json_dir - путь куда будет скачиваться json со всеми книгами (по умолчанию это корневая папка программы)
--skip_books - нужно ли пропускать скачивание книг (нужно указывать True или False, по умолчанию это False)
--skip_images - нужно ли пропускать скачивание обложек книг (нужно указывать True или False, по умолчанию это False)
```
## Цель проекта

Код написан в образовательных целях на онлайн-курсе для веб-разработчиков [dvmn.org](https://dvmn.org/).

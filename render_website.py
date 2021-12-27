import json
from os import makedirs

from livereload import Server, shell
from jinja2 import Environment, FileSystemLoader, select_autoescape
from more_itertools import chunked


def load_books_description(path):
    with open(path, 'r') as file:
        books_description = file.read()

    return json.loads(books_description)


def on_reload(books_description, page_path, page_number, pages_amount):
    env = Environment(
        loader=FileSystemLoader('.'),
        autoescape=select_autoescape(['html', 'xml'])
    )

    template = env.get_template('template.html')
    rendered_page = template.render(
        books_description=books_description,
        current_page_number=page_number,
        pages_amount=pages_amount,
    )

    with open(page_path, 'w', encoding="utf8") as file:
        file.write(rendered_page)


def main():
    makedirs('pages', exist_ok=True)
    page_books_amount = 10
    columns_amount = 2

    description_path = 'description/descriptions.json'

    splited_all_description = list(chunked(
        load_books_description(description_path),
        page_books_amount,
    ))

    pages_amount = len(splited_all_description)

    for page_number, page_description in enumerate(
            splited_all_description,
            1,
    ):
        splited_page_description = list(chunked(
            page_description,
            columns_amount,
        ))
        page_path = f'pages/index{page_number}.html'

        on_reload(splited_page_description, page_path, page_number, pages_amount)

    server = Server()
    server.watch('template.html', on_reload)
    server.serve(root='pages', default_filename='index1.html')


if __name__ == '__main__':
    main()

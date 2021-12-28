import json
from os import makedirs

from livereload import Server
from jinja2 import Environment, FileSystemLoader, select_autoescape
from more_itertools import chunked


def on_reload():
    makedirs('pages', exist_ok=True)
    page_books_amount = 10
    columns_amount = 2
    description_path = 'description/descriptions.json'

    env = Environment(
        loader=FileSystemLoader('.'),
        autoescape=select_autoescape(['html', 'xml'])
    )

    with open(description_path, 'r') as file:
        books_description = json.load(file)

    splited_all_description = list(chunked(
        books_description,
        page_books_amount,
    ))

    pages_amount = len(splited_all_description)

    for page_number, page_description in enumerate(
            splited_all_description,
            1,
    ):
        books_description = list(chunked(
            page_description,
            columns_amount,
        ))
        page_path = f'pages/index{page_number}.html'

        template = env.get_template('template.html')
        rendered_page = template.render(
            books_description=books_description,
            current_page_number=page_number,
            pages_amount=pages_amount,
        )

        with open(page_path, 'w', encoding="utf8") as file:
            file.write(rendered_page)


def main():
    on_reload()

    server = Server()
    server.watch('template.html', on_reload)
    server.serve(root='.', default_filename='pages/index1.html')


if __name__ == '__main__':
    main()

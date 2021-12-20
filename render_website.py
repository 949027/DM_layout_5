#from http.server import HTTPServer, SimpleHTTPRequestHandler
import json

from livereload import Server, shell

from jinja2 import Environment, FileSystemLoader, select_autoescape


def load_books_description(path):
    with open(path, 'r') as file:
        books_description = file.read()

    return json.loads(books_description)


def on_reload():
    books_description = load_books_description(
        'my_books/description/json/descriptions.json'
    )
    print(books_description)

    env = Environment(
        loader=FileSystemLoader('.'),
        autoescape=select_autoescape(['html', 'xml'])
    )

    template = env.get_template('template.html')

    rendered_page = template.render(books_description=books_description)

    with open('index.html', 'w', encoding="utf8") as file:
        file.write(rendered_page)


def main():
    on_reload()

    server = Server()
    server.watch('template.html', on_reload)
    server.serve(root='.')


if __name__ == '__main__':
    main()

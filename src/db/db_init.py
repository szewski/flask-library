from pathlib import Path
import sqlite3

from json_db_controls import Database


db = Database('database.json')


def execute_script(cursor, script_file):
    with open(script_file, encoding='utf-8') as f:
        query = f.read()
    cursor.executescript(query)


if __name__ == '__main__':
    conn = sqlite3.connect('database.db')
    cursor = conn.cursor()

    execute_script(cursor, Path('sql/00_drop_tables.sql'))
    execute_script(cursor, Path('sql/01_books_init.sql'))
    execute_script(cursor, Path('sql/02_users_init.sql'))

    books_json = db.read()

    query = """
    INSERT INTO "books" VALUES
        (NULL, :author, :description, :isbn, :pages,
        :published, :publisher, :subtitle, :title, :website, NULL)
    """

    for book in books_json['books']:
        cursor.execute(query, book)

    conn.commit()

    conn.close()

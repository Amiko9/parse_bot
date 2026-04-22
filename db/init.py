import os
import sqlite3
from dotenv import load_dotenv

load_dotenv()
DB = os.getenv("DB")

sql_statements = [
    """CREATE TABLE IF NOT EXISTS products (
            id INTEGER PRIMARY KEY,
            name_product TEXT NOT NULL
);

    """,
    """ CREATE TABLE IF NOT EXISTS prices (
            product_id INTEGER NOT NULL,
            magazine_name TEXT NOT NULL CHECK (magazine_name IN ('Darwin', 'Enter', 'Neocomputer')),
            link TEXT NOT NULL,
            price TEXT NOT NULL,
            PRIMARY KEY (product_id, magazine_name),
            FOREIGN KEY (product_id) REFERENCES products(id)
);
         """
]

try:
    with sqlite3.connect(DB) as conn:
        cursor = conn.cursor()
        for statement in sql_statements:
            cursor.execute(statement)
        conn.commit()

        print("Tables created successfully.")
except sqlite3.OperationalError as e:
    print("Failed to create tables:", e)
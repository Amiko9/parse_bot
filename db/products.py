from .tables import get_connection


def add_product(name_product):
    with get_connection() as conn:
        cursor = conn.cursor()

        cursor.execute("""
                       INSERT
                       OR IGNORE INTO products (name_product)
            VALUES (?)
                       """, (name_product,))

        conn.commit()

        cursor.execute("""
                       SELECT id
                       FROM products
                       WHERE name_product = ?
                       """, (name_product,))

        return cursor.fetchone()[0]


def get_all_products():
    with get_connection() as conn:
        cursor = conn.cursor()

        cursor.execute("""
                       SELECT id, name_product
                       FROM products
                       """)

        return cursor.fetchall()


def delete_product(product_id):
    with get_connection() as conn:
        cursor = conn.cursor()

        cursor.execute("""
                       DELETE
                       FROM prices
                       WHERE product_id = ?
                       """, (product_id,))

        cursor.execute("""
                       DELETE
                       FROM products
                       WHERE id = ?
                       """, (product_id,))

        conn.commit()

def delete_all_products():
    with get_connection() as conn:
        cursor = conn.cursor()

        cursor.execute("""
            DELETE FROM products
        """)

        conn.commit()

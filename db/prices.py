from .tables import get_connection


def add_price(product_id,chat_id, magazine_name, link, price):
    with get_connection() as conn:
        cursor = conn.cursor()

        cursor.execute("""
            INSERT OR REPLACE INTO prices (
                product_id,
                chat_id,
                magazine_name,
                link,
                price
            )
            VALUES (?, ?, ?, ?, ?)
        """, (product_id, chat_id, magazine_name, link, price))

        conn.commit()


def get_price(chat_id):
    with get_connection() as conn:
        cursor = conn.cursor()

        cursor.execute("""
            SELECT 
                products.id,
                prices.chat_id,
                products.name_product,
                prices.magazine_name,
                prices.link,
                prices.price
            FROM products
            JOIN prices ON products.id = prices.product_id
            WHERE prices.chat_id = ?
        """, (chat_id,))

        return cursor.fetchall()

def get_all_prices():
    with get_connection() as conn:
        cursor = conn.cursor()

        cursor.execute("""
            SELECT products.id,prices.chat_id, products.name_product, prices.magazine_name,
                   prices.link, prices.price
            FROM products
            JOIN prices ON products.id = prices.product_id
        """)

        return cursor.fetchall()


def delete_price(product_id,chat_id, magazine_name):
    with get_connection() as conn:
        cursor = conn.cursor()

        cursor.execute("""
            DELETE FROM prices
            WHERE product_id = ? AND chat_id = ? AND magazine_name = ?
        """, (product_id,chat_id, magazine_name))

        conn.commit()




def update_price(product_id, chat_id, magazine_name, price):
    with get_connection() as conn:
        cursor = conn.cursor()

        cursor.execute("""
            UPDATE prices
            SET price = ?
            WHERE product_id = ? AND chat_id = ? AND magazine_name = ?
        """, (price, product_id,chat_id, magazine_name))

        conn.commit()

def get_price_by_name(title, chat_id):
    with get_connection() as conn:
        cursor = conn.cursor()

        cursor.execute("""
            SELECT 
                products.id,
                prices.chat_id,
                products.name_product,
                prices.magazine_name,
                prices.link,
                prices.price
            FROM products
            JOIN prices ON products.id = prices.product_id
            WHERE products.name_product LIKE ? AND prices.chat_id = ?
        """, (f"%{title}%",chat_id,))

        return cursor.fetchall()




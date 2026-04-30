from db.products import add_product
from db.prices import get_price_by_name, add_price, get_price, delete_price, get_all_prices, update_price
import telebot
import re
import time
from dotenv import load_dotenv
import os
from parser import load_product_info

load_dotenv()

BOT_TOKEN = os.getenv("BOT_TOKEN")
bot = telebot.TeleBot(BOT_TOKEN)


def get_info_product(message):
    try:
        chat_id = message.chat.id
        title = message.text.strip()
        rows = get_price_by_name(title, chat_id)
        result = ""
        last_title = None
        for index, row in enumerate(rows, 1):
            product_id, chat_id, title, magazine, url, price = row
            if title != last_title:
                result += f"\n{index}. {title}\n"
                last_title = title

            result += f"   {magazine} || {price}\n"
        bot.reply_to(message, result)

    except Exception as e:
        print(e)

def ask_custom_product_name(message):
    try:
        url = message.text.strip()

        if re.match(r"^https://[a-z0-9-/.]+$", url):
            msg = bot.reply_to(message, "Enter alternative name for this product:")
            bot.register_next_step_handler(msg, add_link, url)

        else:
            bot.reply_to(message, "Invalid link")
    except Exception as e:
        print(e)




def add_link(message, url):
        try:
            chat_id = message.chat.id
            custom_title = message.text.strip()


            info = load_product_info(url)

            product_id = add_product(custom_title)
            add_price(
                    product_id,
                    chat_id,
                    info["magazine"],
                    url,
                    info["price"]
                )

            bot.reply_to(message, "Link added succesfully")

            bot.reply_to(
                    message,
                    f"Monitoring started:\n{custom_title}\nReal title: {info['title']}\nPrice: {info['price']}\nMagazine: {info['magazine']}\n{url}"
                )
        except Exception as e:
            print(e)

def delete_option(message):
    try:
        chat_id = message.chat.id
        index_text = message.text.strip()

        if not index_text.isdigit():
            bot.reply_to(message, "Invalid index. Enter a number.")
            return

        rows = get_price(chat_id)
        index = int(index_text) - 1

        if index < 0 or index >= len(rows):
            bot.reply_to(message, "Index out of range")
            return

        product_id, chat_id, title, magazine, link, price = rows[index]

        delete_price(product_id, chat_id, magazine)

        bot.reply_to(message, f"Deleted link:\n{title}\n{link}")
    except Exception as e:
        print(e)

def background_checker():
    while True:
        try:
            rows = get_all_prices()

            for row in rows:
                product_id, chat_id, title, magazine, link, old_price = row
                info = load_product_info(link)

                if info is None:
                    continue

                current_price = info["price"]

                if old_price != current_price:
                    update_price(product_id,chat_id, magazine, current_price)
                    bot.send_message(
                        chat_id,
                        f"Price changed!\n\n{title}\nOld price: {old_price}\nNew price: {current_price}\n{link}",
                        disable_web_page_preview=True
                    )

            time.sleep(3600)
        except Exception as e:
            print("Background checker error:", e)
            time.sleep(60)

import os
import telebot
import re
import time
import threading
from telebot import types
from parser import load_product_info
from dotenv import load_dotenv
from db.products import add_product
from db.prices import add_price, get_all_prices, update_price,get_price, delete_price
from db.tables import create_tables

load_dotenv()

BOT_TOKEN = os.getenv("BOT_TOKEN")
bot = telebot.TeleBot(BOT_TOKEN)


@bot.message_handler(commands = ["start"])
def start(message):
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)

    btn1 = types.KeyboardButton("Add a link")
    btn2 = types.KeyboardButton("Check status")
    btn3 = types.KeyboardButton("Delete option")

    markup.add(btn1, btn2, btn3)

    bot.reply_to(message, "Bot is active!\nChoose an option: ", reply_markup = markup)

@bot.message_handler(func = lambda message: message.text == "Add a link")
def ask_link(message):
    try:
        msg = bot.reply_to(message, "Enter a link:")
        bot.register_next_step_handler(msg, add_link)
    except Exception as e:
        print(e)

@bot.message_handler(func = lambda message: message.text == "Check status")
def check(message):
    try:
        chat_id = message.chat.id
        rows = get_price(chat_id)
        result =""
        for index, row in enumerate(rows, 1):
            product_id, chat_id, title, magazine, url, price = row
            result += f"{index}:{title} || {price}\n"
        bot.reply_to(message, result)
    except Exception as e:
        print(e)

@bot.message_handler(func = lambda message: message.text == "Delete option")
def ask_delete_index(message):
    try:
        chat_id = message.chat.id
        rows = get_price(chat_id)
        if not rows:
            bot.reply_to(message, "No links to delete")
            return

        result = "Links list:\n\n"
        for index, row in enumerate(rows, 1):
            product_id, chat_id, title, magazine, url, price = row
            result += f"{index}:{title} || {magazine} || {price}\n"

        msg = bot.reply_to(message, result + "\nEnter the index you want to delete:")
        bot.register_next_step_handler(msg, delete_option)
    except Exception as e:
        print(e)

def add_link(message):
        try:
            chat_id = message.chat.id
            url = message.text.strip()
            if re.match(r"^https://[a-z0-9-/.]+$", f'{url}'):

                info = load_product_info(url)

                product_id = add_product(info["title"])

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
                    f"Monitoring started:\n{info['title']}\nPrice: {info['price']}\n{message.text.strip()}"
                )

            else:
                bot.reply_to(message, "Invalid link")
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

        product_id, title, magazine, link, price = rows[index]

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


if __name__ == "__main__":
    create_tables()

    thread = threading.Thread(target=background_checker, daemon=True)
    thread.start()

    bot.polling(True)
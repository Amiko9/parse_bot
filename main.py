import os
import telebot
import re
import time
import threading
from telebot import types
from parser import load_product_info
from dotenv import load_dotenv


load_dotenv()

BOT_TOKEN = os.getenv("BOT_TOKEN")
bot = telebot.TeleBot(BOT_TOKEN)
links = []
chat_ids = set()
last_prices = {}

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
        result =""
        for index, link in enumerate(links, 1):
            info = load_product_info(link)
            result += f"{index}:{info['title']} || {info['price']}\n"
        bot.reply_to(message, result)
    except Exception as e:
        print(e)

@bot.message_handler(func = lambda message: message.text == "Delete option")
def ask_delete_index(message):
    try:
        if not links:
            bot.reply_to(message, "No links to delete")
            return

        result = "Links list:\n\n"
        for index, link in enumerate(links, 1):
            info = load_product_info(link)
            result += f"{index}:{info['title']} || {info['price']}\n"

        msg = bot.reply_to(message, result + "\nEnter the index you want to delete:")
        bot.register_next_step_handler(msg, delete_option)
    except Exception as e:
        print(e)

def add_link(message):

        try:
            chat_ids.add(message.chat.id)
            if re.match(r"^https://[a-z0-9-/.]+$", f'{message.text.strip()}'):
                links.append(message.text.strip())
                info = load_product_info(message.text.strip())
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
        index_text = message.text.strip()

        if not index_text.isdigit():
            bot.reply_to(message, "Invalid index. Enter a number.")
            return

        index = int(index_text)-1

        if index < 0 or index >= len(links):
            bot.reply_to(message, "Index out of range")
            return

        deleted_link = links.pop(index)

        if deleted_link in last_prices:
            del last_prices[deleted_link]

        bot.reply_to(message, f"Deleted link:\n{deleted_link}")
    except Exception as e:
        print(e)
def background_checker():
    while True:
        try:
            for link in links:
                info = load_product_info(link)

                if info is None:
                    continue

                current_price = info["price"]
                title = info["title"]

                if link not in last_prices:
                    last_prices[link] = current_price
                else:
                    old_price = last_prices[link]

                    if old_price != current_price:
                        last_prices[link] = current_price
                        for chat_id in chat_ids:
                            bot.send_message(
                                chat_id,
                                f"Price changed!\n\n{title}\nOld price: {old_price}\nNew price: {current_price}\n{link}",
                                disable_web_page_preview=True
                            )

            time.sleep(60)
        except Exception as e:
            print("Background checker error:", e)
            time.sleep(60)


if __name__ == "__main__":
    thread = threading.Thread(target=background_checker, daemon=True)
    thread.start()
    bot.polling(True)
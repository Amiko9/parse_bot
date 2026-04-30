import os
import telebot
import threading
from telebot import types
from dotenv import load_dotenv
from db.products import delete_all_products
from db.prices import get_price
from db.tables import create_tables
from helping_functions import ask_custom_product_name, delete_option, get_info_product, background_checker

load_dotenv()

BOT_TOKEN = os.getenv("BOT_TOKEN")
bot = telebot.TeleBot(BOT_TOKEN)


@bot.message_handler(commands = ["start"])
def start(message):
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)

    btn1 = types.KeyboardButton("Add a link")
    btn2 = types.KeyboardButton("Check status")
    btn3 = types.KeyboardButton("Delete option")
    btn4 = types.KeyboardButton("Info for a product")
    btn5 = types.KeyboardButton("Delete all")

    markup.add(btn1, btn2, btn3, btn4, btn5)

    bot.reply_to(message, "Bot is active!\nChoose an option: ", reply_markup = markup)

@bot.message_handler(func = lambda message: message.text == "Add a link")
def ask_link(message):
    try:
        msg = bot.reply_to(message, "Enter a link:")
        bot.register_next_step_handler(msg, ask_custom_product_name)

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
            result += f"{index}:{title} || {magazine} || {price}\n"
        bot.reply_to(message, result)
    except Exception as e:
        print(e)
        bot.reply_to(message,"No data")

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

@bot.message_handler(func = lambda message: message.text == "Delete all")
def delete_all(message):
    try:
        chat_id = message.chat.id
        rows = get_price(chat_id)
        if not rows:
            bot.reply_to(message, "No links to delete")
            return
        delete_all_products()


    except Exception as e:
        print(e)

@bot.message_handler(func=lambda message: message.text == "Info for a product")
def get_info_by_name(message):
    try:
        msg = bot.reply_to(message, "Enter name for a product:")
        bot.register_next_step_handler(msg, get_info_product)
    except Exception as e:
        print(e)




if __name__ == "__main__":
    create_tables()

    thread = threading.Thread(target=background_checker, daemon=True)
    thread.start()

    bot.polling(True)

# optiune cu categorie care primeste link
# si extrage fiecare produs il pune in baza de date
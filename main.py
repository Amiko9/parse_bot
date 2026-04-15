import os
import telebot


BOT_TOKEN = os.environ.get("BOT_TOKEN")
bot = telebot.TeleBot(BOT_TOKEN)


@bot.message_handler(commands = ["start"])
def start(message):
    text = "Bot is active"
    bot.reply_to(message, text)

@bot.message_handler(content_types=["voice"])
def func2():
    pass

@bot.callback_query_handler(func=lambda call: True)
def func():
    pass

if __name__ == "__main__":
    bot.polling(True)
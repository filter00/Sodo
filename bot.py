import telebot
import os
from imdb_helper import check_spelling_and_get_imdb_info

# API_TOKEN environment variable se lena, Heroku par set karein
API_TOKEN = os.environ.get("TELEGRAM_BOT_TOKEN")
if not API_TOKEN:
    print("Error: TELEGRAM_BOT_TOKEN environment variable set nahi hai.")
    exit() # Bot ko shuru hone se roke agar token missing hai

bot = telebot.TeleBot(API_TOKEN)

@bot.message_handler(commands=['start', 'help'])
def send_welcome(message):
    bot.reply_to(message, """
Yeh ek bot hai jo movie ke naam ki spelling check karta hai aur IMDB se information deta hai agar spelling galat hai.
Movie ka naam bheje!""")

@bot.message_handler(func=lambda message: True)
def movie_info(message):
    movie_name = message.text
    result = check_spelling_and_get_imdb_info(movie_name)
    bot.reply_to(message, result)

if __name__ == "__main__":
    try:
        bot.polling(none_stop=True)
    except Exception as e:
        print(f"Bot polling mein error: {e}")

import telebot
from telebot.types import ReplyKeyboardMarkup, KeyboardButton, WebAppInfo

TOKEN = '8672670954:AAELhSlmKx-EhqRCiBRBWN8dQBuqSGZkkVE'

bot = telebot.TeleBot(TOKEN)

@bot.message_handler(commands=['start'])
def start(message):
    keyboard = ReplyKeyboardMarkup(resize_keyboard=True)
    button = KeyboardButton(
        text='📱 Dastur bilan tanishish',
        web_app=WebAppInfo(url='https://ads.zim-zim.uz/')
    )
    keyboard.add(button)
    bot.send_message(message.chat.id, '👋 Xush kelibsiz!', reply_markup=keyboard)

bot.polling()

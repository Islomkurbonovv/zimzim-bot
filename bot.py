import telebot
import json
import os
from telebot.types import ReplyKeyboardMarkup, KeyboardButton, WebAppInfo

TOKEN = '8672670954:AAELhSlmKx-EhqRCiBRBWN8dQBuqSGZkkVE'
ADMIN_ID = 337240477

bot = telebot.TeleBot(TOKEN)

USERS_FILE = 'users.json'

def load_users():
    if os.path.exists(USERS_FILE):
        with open(USERS_FILE, 'r') as f:
            return set(json.load(f))
    return set()

def save_users(users):
    with open(USERS_FILE, 'w') as f:
        json.dump(list(users), f)

users = load_users()

@bot.message_handler(commands=['start'])
def start(message):
    users.add(message.chat.id)
    save_users(users)
    keyboard = ReplyKeyboardMarkup(resize_keyboard=True)
    button = KeyboardButton(
        text='🚀 Dastur bilan tanishish',
        web_app=WebAppInfo(url='https://ads.zim-zim.uz/')
    )
    keyboard.add(button)
    bot.send_message(
        message.chat.id,
        '👋 Assalomu alaykum! Zim-Zim rasmiy botiga xush kelibsiz.\n\n'
        '✅ Dastur bilan to\'liq tanishish va menejerdan batafsil ma\'lumot olish uchun pastdagi "Dastur bilan tanishish" tugmasini bosing.',
        reply_markup=keyboard
    )

@bot.message_handler(commands=['broadcast'])
def broadcast_start(message):
    if message.chat.id != ADMIN_ID:
        bot.send_message(message.chat.id, '❌ Sizda ruxsat yo\'q.')
        return
    bot.send_message(message.chat.id, f'📢 {len(users)} ta obunachi bor.\n\nXabarni yuboring:')
    bot.register_next_step_handler(message, do_broadcast)

def do_broadcast(message):
    success = 0
    failed = 0
    for user_id in list(users):
        try:
            if message.content_type == 'text':
                bot.send_message(user_id, message.text)
            elif message.content_type == 'photo':
                bot.send_photo(user_id, message.photo[-1].file_id, caption=message.caption or '')
            elif message.content_type == 'video':
                bot.send_video(user_id, message.video.file_id, caption=message.caption or '')
            elif message.content_type == 'document':
                bot.send_document(user_id, message.document.file_id, caption=message.caption or '')
            elif message.content_type == 'voice':
                bot.send_voice(user_id, message.voice.file_id)
            elif message.content_type == 'sticker':
                bot.send_sticker(user_id, message.sticker.file_id)
            success += 1
        except Exception as e:
            failed += 1
            if 'blocked' in str(e).lower() or 'deactivated' in str(e).lower():
                users.discard(user_id)
                save_users(users)
    bot.send_message(ADMIN_ID, f'✅ Yuborildi!\n👤 Muvaffaqiyatli: {success}\n❌ Xato: {failed}')

@bot.message_handler(commands=['stats'])
def stats(message):
    if message.chat.id != ADMIN_ID:
        return
    bot.send_message(message.chat.id, f'📊 Jami obunachi: {len(users)} ta')

bot.polling()

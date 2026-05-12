import telebot
import json
import os
from telebot.types import ReplyKeyboardMarkup, KeyboardButton, WebAppInfo

TOKEN = '8672670954:AAELhSlmKx-EhqRCiBRBWN8dQBuqSGZkkVE'
ADMIN_ID = 337240477
VIDEO_NOTE_ID = None  # DQACAgIAAxkBAAN5agM0kpBPMyiokxTYUBQHBiSkpjcAAit9AAI3O0lKV-INxnZyAAGVOwQ

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
    if message.chat.id == ADMIN_ID:
        keyboard.add(KeyboardButton('📢 Xabar yuborish'))
    
    if VIDEO_NOTE_ID:
        bot.send_video_note(message.chat.id, VIDEO_NOTE_ID)
    
    bot.send_message(
        message.chat.id,
        '👋 Assalomu alaykum! Zim-Zim rasmiy botiga xush kelibsiz.\n\n'
        '✅ Dastur bilan to\'liq tanishish va menejerdan batafsil ma\'lumot olish uchun pastdagi "Dastur bilan tanishish" tugmasini bosing.',
        reply_markup=keyboard
    )

@bot.message_handler(content_types=['video_note'])
def get_video_note_id(message):
    if message.chat.id == ADMIN_ID:
        bot.send_message(message.chat.id, f'✅ File ID:\n`{message.video_note.file_id}`', parse_mode='Markdown')

@bot.message_handler(func=lambda m: m.text == '📢 Xabar yuborish' and m.chat.id == ADMIN_ID)
def broadcast_button(message):
    bot.send_message(message.chat.id, f'📢 {len(users)} ta obunachi bor.\n\nXabarni yuboring:')
    bot.register_next_step_handler(message, do_broadcast)

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
            bot.copy_message(user_id, message.chat.id, message.message_id)
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

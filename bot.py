import telebot
import json
import os
import gspread
from oauth2client.service_account import ServiceAccountCredentials
from telebot.types import ReplyKeyboardMarkup, KeyboardButton, WebAppInfo
from datetime import datetime

TOKEN = '8672670954:AAELhSlmKx-EhqRCiBRBWN8dQBuqSGZkkVE'
ADMIN_ID = 337240477
VIDEO_NOTE_ID = 'DQACAgIAAxkBAAN5agM0kpBPMyiokxTYUBQHBiSkpjcAAit9AAI3O0lKV-INxnZyAAGVOwQ'
SHEET_ID = '1FeFSvoNttbB-gmg-lJovLzchFc6DR0GqLfQq4bp0LZI'

CREDS_JSON = {
  "type": "service_account",
  "project_id": "zimzim-bot",
  "private_key_id": "62ea1824c97656891fe94ebe1e26e48ba24b9a4f",
  "private_key": "-----BEGIN PRIVATE KEY-----\nMIIEvAIBADANBgkqhkiG9w0BAQEFAASCBKYwggSiAgEAAoIBAQCiPRRNv8U1T3Zt\nOsZyvGhEW1Ue2VCR/eZr4lsyJlkgGBknLq6HswyC+ITAEgLtsgSQbFANlOa0yEak\n5nhm6NwwRkB4+XnNOKPOB2dlGvN/TshbpxnIPJZvizxf7c2U/tp1pXs4Q19z8NT4\nrLc3WGYXn/HzGh92kcYQZ1PtSFUqJEL7v3wejZhF0bGzmgfx+hfWOxe+E1WIv2dj\nawAWh6zbaFgJuODJptxUHZid2YvQf5qwTcT+CqaLXTvSu63gUGT/saacePZlOgAZ\nTfBCta4CrYbd2hY1ZtGRn3Nlz8FhsMoDPlZr7auI4DPrB1VV8H23g1KjpK5bXMzU\nFvXF7GmDAgMBAAECggEAD6uKnH/bUmzcaWx14nskLwYLULF4wMEfUmhImq1tilYJ\nh+lQXjcDDFtopwyWT9MT8cckbEtnhSqa+C5yjq4LJnaCn6ypARNpbur0J6XUwwUf\nAQtAyEBh32A5cqKLasq62wYiwqpvO8mVKHe2MphNNBb0zaBGTbOCx+7TAmYsI6e5\nlzZWXDmLZsicnEdJovlD+8quwhhdNEV0qquugltv/0l1sMR4vO68xFeE/2HdKbKk\n+tY+DKLTMUFLpWRA3YaSnKpp2LimuCHdHAI0kxIEhoTcaSTaUsC4JaiMqVgx6mFC\nKbGa+CqHXVYyxpwQIfxs7yovMGDsu1DE/KyCDglaAQKBgQDQyZ8OS2BVE7m3ZDRO\npyUI9yAnYwuDqVeQnDJJHYYr5TK6dR01oMvfWAFpY7Kp/XaZke7PISnr6ch19mdM\nXMszbNSERusrDxLtM82g2kFgDiwfFco5OhDcFOskYlssKOx7S8+yddOIqdmHWjbn\nRDR5b96iD16sNsYFwVvKNLOIgQKBgQDG7M+5L8sqG7Ald3B8IgenNyllHyFoX5TF\n3kJ0PcKPp0m3X58/XUo3gG0D1iTBz869cGthfBq685QW4Rsaqu8Q7VUQvH/8Uipr\ntojw9smSxClIzW4diy/81RVGxH4TilT8/Agh/SjLmiFH1OKZVzEZuxn1TvNhVaAR\nL6CcTGnQAwKBgGeKpbOcE/D9MEvPiNU8tPQmQi7mQo6Py5ourA1wc9qO9sJbVBoF\nXTWs2j5er/r3dPqh0ZGs+7JAJSbDBOVs22TsYtQaq4OWHSe/WgmcU3GEdcMQtlH9\nBuFuClLn6BkVTnmy1hTFtBsBSJyEU9gLDg7vOLSb9LJpE3lFM/Uqf6KBAoGAQSQJ\nPdZVzFs2yn4bWrr2EJ7yskeIdBpgqI8I6fHThaE9dYwdpO1SwWwPxuLYNJNtWwG2\nWD0Ar9nV08wxSQFSuhNN+OYRbzok5BLpMydNiP8tmcaT2Z7bvwq0JfFwa8uv2wxZ\nSXASbOHzJgejkJ1J2eg4LumEr4oPmbEkAirPt6sCgYBx7kq8HwILI4dfpjqn/4jt\nKAjsK+fhGU4dqm9otqj3RaZS8xKSLcaC/TfbEnmLxuEWceNTBXeBSrYNetCWfCj9\nWvbMohDu4dg4yKVibI8ioeswnteQESHiEmjCUvLkJtBr9m5cdmxz423OVhupqq6k\nC6R8clASR8Lny6NLR3RSmg==\n-----END PRIVATE KEY-----\n",
  "client_email": "zimzim-sheets@zimzim-bot.iam.gserviceaccount.com",
  "client_id": "118363293589458683022",
  "auth_uri": "https://accounts.google.com/o/oauth2/auth",
  "token_uri": "https://oauth2.googleapis.com/token",
  "auth_provider_x509_cert_url": "https://www.googleapis.com/oauth2/v1/certs",
  "client_x509_cert_url": "https://www.googleapis.com/robot/v1/metadata/x509/zimzim-sheets%40zimzim-bot.iam.gserviceaccount.com",
  "universe_domain": "googleapis.com"
}

scope = ['https://spreadsheets.google.com/feeds', 'https://www.googleapis.com/auth/drive']
creds = ServiceAccountCredentials.from_json_keyfile_dict(CREDS_JSON, scope)
gc = gspread.authorize(creds)
sheet = gc.open_by_key(SHEET_ID).sheet1

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

def save_to_sheet(user):
    try:
        records = sheet.col_values(2)
        if str(user.id) not in records:
            sana = datetime.now().strftime('%d.%m.%Y %H:%M')
            username = f'@{user.username}' if user.username else '-'
            ism = f'{user.first_name or ""} {user.last_name or ""}'.strip()
            sheet.append_row([sana, str(user.id), ism, username])
    except Exception as e:
        print(f'Sheet xato: {e}')

users = load_users()

@bot.message_handler(commands=['start'])
def start(message):
    users.add(message.chat.id)
    save_users(users)
    save_to_sheet(message.from_user)

    keyboard = ReplyKeyboardMarkup(resize_keyboard=True)
    button = KeyboardButton(
        text='🚀 Dastur bilan tanishish',
        web_app=WebAppInfo(url='https://ads.zim-zim.uz/')
    )
    keyboard.add(button)
    if message.chat.id == ADMIN_ID:
        keyboard.add(KeyboardButton('📢 Xabar yuborish'))
        bot.send_message(ADMIN_ID, f'📊 Jami obunachi: {len(users)} ta')

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

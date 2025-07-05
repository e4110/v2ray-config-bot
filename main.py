
import os
import telebot
from telebot import types

BOT_TOKEN = os.getenv("BOT_TOKEN")
CHANNEL_ID = -1002549789972
ADMIN_ID = 683844720  # آیدی عددی ادمین

bot = telebot.TeleBot(BOT_TOKEN)
CONFIG_FILE = "latest_config.txt"

def is_user_member(user_id):
    try:
        member = bot.get_chat_member(CHANNEL_ID, user_id)
        return member.status in ['member', 'creator', 'administrator']
    except:
        return False

@bot.message_handler(func=lambda message: message.chat.id == ADMIN_ID)
def save_config(message):
    with open(CONFIG_FILE, "w", encoding="utf-8") as f:
        f.write(message.text)
    bot.reply_to(message, "✅ پیام به‌عنوان کانفیگ جدید ذخیره شد.")

def send_latest_config(user_id):
    if os.path.exists(CONFIG_FILE):
        with open(CONFIG_FILE, "r", encoding="utf-8") as f:
            text = f.read()
        bot.send_message(user_id, text)
    else:
        bot.send_message(user_id, "❌ هنوز هیچ کانفیگی توسط ادمین وارد نشده است.")

@bot.message_handler(commands=['start'])
def handle_start(message):
    user_id = message.from_user.id
    if is_user_member(user_id):
        send_latest_config(user_id)
        show_buttons(user_id)
    else:
        msg = "🍥 برای دریافت کانفیگ رایگان، ابتدا عضو کانال زیر شوید:\n@LiveTetherPrice"


msg = "پس از فشردن دکمه 'بررسی عضویت' را بزنید."
        markup = types.InlineKeyboardMarkup()
        markup.add(types.InlineKeyboardButton("🔄 بررسی عضویت", callback_data="check"))
        bot.send_message(user_id, msg, reply_markup=markup)

def show_buttons(chat_id):
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    markup.add("📡 قطع شدم", "📨 ارتباط با ادمین")
    bot.send_message(chat_id, "👇 لطفاً یکی از گزینه‌ها را انتخاب کنید:", reply_markup=markup)

@bot.message_handler(func=lambda m: True)
def handle_buttons(message):
    user_id = message.from_user.id
    if message.text == "📡 قطع شدم":
        if is_user_member(user_id):
            send_latest_config(user_id)
        else:
            bot.send_message(user_id, "⛔️ برای دریافت مجدد کانفیگ، ابتدا عضو کانال شوید: @LiveTetherPrice")
    elif message.text == "📨 ارتباط با ادمین":
        bot.send_message(user_id, "🔗 ارتباط با ادمین:
@YourUsername")

@bot.callback_query_handler(func=lambda call: call.data == "check")
def handle_check(call):
    user_id = call.from_user.id
    if is_user_member(user_id):
        bot.answer_callback_query(call.id, "✅ عضو شدید!")
        send_latest_config(user_id)
        show_buttons(user_id)
    else:
        bot.answer_callback_query(call.id, "⛔️ هنوز عضو نیستید.")

print("ربات در حال اجرا است...")
bot.infinity_polling()

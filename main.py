import os
import telebot
from telebot import types

BOT_TOKEN = os.getenv("BOT_TOKEN")
CHANNEL_ID = -1002549789972
ADMIN_ID = 683844720

bot = telebot.TeleBot(BOT_TOKEN)
CONFIG_FILE = "latest_config.txt"

def is_user_member(user_id):
    try:
        member = bot.get_chat_member(CHANNEL_ID, user_id)
        return member.status in ['member', 'creator', 'administrator']
    except:
        return False

@bot.message_handler(commands=['start'])
def handle_start(message):
    user_id = message.from_user.id
    if is_user_member(user_id):
        send_latest_config(user_id)
        show_buttons(user_id)
    else:
        msg1 = "🍥 برای دریافت کانفیگ رایگان، ابتدا عضو کانال زیر شوید:\n@LiveTetherPrice"
        msg2 = "پس از عضویت، دکمه «🔄 بررسی عضویت» را بزنید."


        markup = types.InlineKeyboardMarkup()
        markup.add(types.InlineKeyboardButton("🔄 بررسی عضویت", callback_data="check"))
        bot.send_message(user_id, msg, reply_markup=markup)

def send_latest_config(user_id):
    if os.path.exists(CONFIG_FILE):
        with open(CONFIG_FILE, "r", encoding="utf-8") as f:
            text = f.read()
        bot.send_message(user_id, text)
    else:
        bot.send_message(user_id, "❌ هنوز هیچ کانفیگی توسط ادمین وارد نشده است.")

def show_buttons(chat_id):
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    markup.add("📡 دریافت کانفیگ", "📡 قطع شدم", "📨 ارتباط با ادمین")
    bot.send_message(chat_id, "👇 لطفاً یکی از گزینه‌ها را انتخاب کنید:", reply_markup=markup)

@bot.message_handler(func=lambda m: True)
def handle_all_messages(message):
    user_id = message.from_user.id

    if user_id == ADMIN_ID and message.reply_to_message:
        reply_text = message.text
        try:
            original_user_id = int(message.reply_to_message.text.split("ID: ")[-1])
            bot.send_message(original_user_id, f"✉️ پاسخ ادمین: {response_text}")

            bot.reply_to(message, "✅ پیام ارسال شد.")
        except:
            bot.reply_to(message, "⚠️ خطا در استخراج شناسه کاربر.")
        return

    if user_id != ADMIN_ID:
        bot.send_message(ADMIN_ID, f"📩 پیام از کاربر:

{message.text}

👤 ID: {user_id}")
        bot.send_message(user_id, "📨 پیام شما برای ادمین ارسال شد. منتظر پاسخ باشید.")

    if message.text == "📡 دریافت کانفیگ" or message.text == "📡 قطع شدم":
        if is_user_member(user_id):
            send_latest_config(user_id)
        else:
            bot.send_message(user_id, "⛔️ برای دریافت کانفیگ ابتدا در کانال عضو شوید: @LiveTetherPrice")

    elif message.text == "📨 ارتباط با ادمین":
        bot.send_message(user_id, "✍️ پیام خود را بنویسید. ادمین به شما پاسخ خواهد داد.")

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

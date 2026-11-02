import os
from flask import Flask
from threading import Thread
import telebot
from telebot.types import InlineKeyboardMarkup, InlineKeyboardButton

# Flask app for Render Web Service Port Binding (Free Tier)
app = Flask('')

@app.route('/')
def home():
    return "NexFly IT Bot is running alive!"

def run():
    port = int(os.environ.get("PORT", 8080))
    app.run(host='0.0.0.0', port=port)

def keep_alive():
    t = Thread(target=run)
    t.start()

# Telegram Bot Token & Admin Chat ID
TOKEN = '9175529571:AAG8I9a6G4Fi834amGCjH6Zq23_2q_5t-M8'
ADMIN_ID = 8365272832  # Your Telegram User ID

bot = telebot.TeleBot(TOKEN)

# User state storage for tracking live chat mode
user_states = {}

# ----------------- KEYBOARDS -----------------

def main_menu_keyboard():
    markup = InlineKeyboardMarkup()
    markup.row_width = 1
    markup.add(
        InlineKeyboardButton("🛡️ Recovery & Protection", callback_data="cat_recovery"),
        InlineKeyboardButton("🚀 Growth & Verification", callback_data="cat_growth"),
        InlineKeyboardButton("👑 Premium Apps", callback_data="cat_apps"),
        InlineKeyboardButton("💻 Web & Design", callback_data="cat_web"),
        InlineKeyboardButton("💬 Live Support (Admin Chat)", callback_data="live_chat")
    )
    return markup

def back_to_main_keyboard():
    markup = InlineKeyboardMarkup()
    markup.add(InlineKeyboardButton("🔙 Back to Main Menu", callback_data="main_menu"))
    return markup

# ----------------- START & MENU COMMANDS -----------------

@bot.message_handler(commands=['start', 'menu'])
def send_welcome(message):
    welcome_text = (
        "Welcome to NexFly IT 🥀✨

"
        "NexFly IT, the official IT service organization of Team BCT, provides you with various services "
        "including account/page recovery, verification, premium apps, website design, followers, "
        "and solutions to all social media-related issues. Ethical & verified work, Fast delivery.

"
        "Please select your required category below. Type or tap /menu to bring up the main menu anytime."
    )
    bot.send_message(message.chat.id, welcome_text, reply_markup=main_menu_keyboard())

# ----------------- CALLBACK QUERY HANDLER -----------------

@bot.callback_query_handler(func=lambda call: True)
def callback_inline(call):
    chat_id = call.message.chat.id

    if call.data == "main_menu":
        welcome_text = (
            "Welcome to NexFly IT 🥀✨

"
            "Please select your required category below:"
        )
        bot.edit_message_text(chat_id=chat_id, message_id=call.message.message_id, text=welcome_text, reply_markup=main_menu_keyboard())

    elif call.data == "cat_recovery":
        text = (
            "🛡️ *Recovery & Protection Services*

"
            "1. *Social Media Recovery* (Delivery: 7–14 days)
"
            "   • FB/IG/X Suspended Account: ৳700
"
            "   • FB/IG/X Disabled Account: ৳7,000
"
            "   • FB/IG/X Hacked Account: ৳3,000 – ৳12,000
"
            "   • Facebook Page Suspended: ৳4,000
"
            "   • Facebook Page Hacked: ৳3,000 – ৳12,000
"
            "   • Gmail Disabled/Hacked/Age Verify: ৳1,500

"
            "2. *Content Restore* (Delivery: 7–14 days)
"
            "   • Copyright Claim: ৳2,500
"
            "   • Trademark Claim: ৳4,000
"
            "   • Other Issues: ৳2,000

"
            "3. *Payout / Monetisation Issue*: ৳3,000 – ৳15,000

"
            "4. *Removal Service* (Delivery: 3–6 days)
"
            "   • FB/IG Account Remove: ৳1,500
"
            "   • X Account Remove: ৳5,000
"
            "   • FB Page Remove: ৳5,000 – ৳25,000
"
            "   • YouTube Content Remove: ৳5,000
"
            "   • Telegram Channel/Bot Remove: ৳1,500
"
            "   • Scam Website Remove: ৳3,000

"
            "5. *Page Protection* (Monthly Plan)
"
            "   • 1 Month: ৳4,000 | 3 Months: ৳12,000

"
            "📲 *Order on WhatsApp:* https://wa.me/message/QFALT7WQHZ2CN1"
        )
        markup = InlineKeyboardMarkup()
        markup.add(InlineKeyboardButton("📲 Order via WhatsApp", url="https://wa.me/message/QFALT7WQHZ2CN1"))
        markup.add(InlineKeyboardButton("🔙 Back to Main Menu", callback_data="main_menu"))
        bot.edit_message_text(chat_id=chat_id, message_id=call.message.message_id, text=text, parse_mode="Markdown", reply_markup=markup)

    elif call.data == "cat_growth":
        text = (
            "🚀 *Growth & Verification Services*

"
            "1. *Verification (1 Month)* (Delivery: 24–72h)
"
            "   • FB Page/Account: ৳399 – ৳29,999
"
            "   • Instagram Account: ৳399 – ৳999
"
            "   • WhatsApp Business: ৳699 – ৳14,999
"
            "   • X Account: ৳800
"
            "   • FB Business Manager: ৳1,500

"
            "2. *Followers / Audience* (Max 10K per order)
"
            "   • FB / IG: ৳150 per 1K
"
            "   • TikTok: ৳300 per 1K

"
            "3. *Facebook Ad Run*
"
            "   • Custom Pricing (Price on request)

"
            "📲 *Order on WhatsApp:* https://wa.me/message/QFALT7WQHZ2CN1"
        )
        markup = InlineKeyboardMarkup()
        markup.add(InlineKeyboardButton("📲 Order via WhatsApp", url="https://wa.me/message/QFALT7WQHZ2CN1"))
        markup.add(InlineKeyboardButton("🔙 Back to Main Menu", callback_data="main_menu"))
        bot.edit_message_text(chat_id=chat_id, message_id=call.message.message_id, text=text, parse_mode="Markdown", reply_markup=markup)

    elif call.data == "cat_apps":
        text = (
            "👑 *Premium Apps & Accounts*

"
            "• *CapCut Premium:* 1M ৳422 | 3M ৳566 | 6M ৳1,699 | 12M ৳3,199
"
            "• *Canva Premium:* 1 Month ৳133
"
            "• *YouTube Premium:* 1 Month ৳133
"
            "• *Google Drive + Gemini AI Pro:* 3 Months ৳433
"
            "• *Telegram Premium:* 1 Month ৳499 | 1 Year ৳3,999
"
            "• *VPN Premium:* Price on request

"
            "📲 *Order on WhatsApp:* https://wa.me/message/QFALT7WQHZ2CN1"
        )
        markup = InlineKeyboardMarkup()
        markup.add(InlineKeyboardButton("📲 Order via WhatsApp", url="https://wa.me/message/QFALT7WQHZ2CN1"))
        markup.add(InlineKeyboardButton("🔙 Back to Main Menu", callback_data="main_menu"))
        bot.edit_message_text(chat_id=chat_id, message_id=call.message.message_id, text=text, parse_mode="Markdown", reply_markup=markup)

    elif call.data == "cat_web":
        text = (
            "💻 *Web & Landing Page Design* (Delivery: 7 Days)

"
            "1. *Landing Page Starter – ৳4,499*
"
            "   • 1-Page Professional Landing Page
"
            "   • Modern & Clean UI/UX Design
"
            "   • Fully Mobile Responsive & Fast
"
            "   • WhatsApp & Contact CTA
"
            "   • 30 Days Free Support

"
            "2. *Landing Page Pro – ৳10,999*
"
            "   • Premium Custom UI/UX Design
"
            "   • Speed & Basic SEO Optimization
"
            "   • Direct Inquiry Form + Analytics Setup
"
            "   • 90 Days Technical Support

"
            "📲 *Order on WhatsApp:* https://wa.me/message/QFALT7WQHZ2CN1"
        )
        markup = InlineKeyboardMarkup()
        markup.add(InlineKeyboardButton("📲 Order via WhatsApp", url="https://wa.me/message/QFALT7WQHZ2CN1"))
        markup.add(InlineKeyboardButton("🔙 Back to Main Menu", callback_data="main_menu"))
        bot.edit_message_text(chat_id=chat_id, message_id=call.message.message_id, text=text, parse_mode="Markdown", reply_markup=markup)

    elif call.data == "live_chat":
        user_states[chat_id] = "LIVE_CHAT"
        text = "💬 You are now connected to Live Support! Write your message below, and our team will reply shortly 🙂"
        bot.send_message(chat_id, text, reply_markup=back_to_main_keyboard())

# ----------------- MESSAGE HANDLING & LIVE CHAT -----------------

@bot.message_handler(func=lambda message: True)
def handle_messages(message):
    chat_id = message.chat.id
    
    # Check if message is from Admin replying to a user
    if chat_id == ADMIN_ID and message.reply_to_message:
        try:
            reply_text = message.reply_to_message.text
            if "User ID:" in reply_text:
                target_id = int(reply_text.split("User ID:")[1].split("
")[0].strip())
                bot.send_message(target_id, f"💬 *Support Reply:*
{message.text}", parse_mode="Markdown")
                bot.send_message(ADMIN_ID, "✅ Reply sent successfully!")
            else:
                bot.send_message(ADMIN_ID, "🤧 Couldn't extract User ID from the replied message.")
        except Exception as e:
            bot.send_message(ADMIN_ID, f"🤧 Failed to send reply: {str(e)}")
        return

    # User message forwarding to Admin
    msg_to_admin = (
        f"📩 *New Support Message*
"
        f"👤 From: {message.from_user.first_name} (@{message.from_user.username or 'No_Username'})
"
        f"🆔 User ID: `{chat_id}`

"
        f"💬 Message: {message.text}"
    )
    
    bot.send_message(ADMIN_ID, msg_to_admin, parse_mode="Markdown")
    bot.send_message(chat_id, "Message received! Our team will reply to you soon 🙂", reply_markup=back_to_main_keyboard())

# ----------------- BOT RUNNER -----------------

if __name__ == "__main__":
    print("Starting Keep Alive Server...")
    keep_alive()
    print("Bot is starting...")
    bot.infinity_polling()

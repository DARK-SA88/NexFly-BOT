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

WA_LINK = "https://wa.me/message/QFALT7WQHZ2CN1"

# User state storage for interactive quantity/duration selection
user_states = {}

# ----------------- KEYBOARDS -----------------

def main_menu_keyboard():
    markup = InlineKeyboardMarkup()
    markup.row_width = 1
    markup.add(
        InlineKeyboardButton("🛡️ Recovery & Protection", callback_data="sub_recovery"),
        InlineKeyboardButton("🚀 Growth & Verification", callback_data="sub_growth"),
        InlineKeyboardButton("👑 Premium Apps", callback_data="sub_apps"),
        InlineKeyboardButton("💻 Web & Design", callback_data="sub_web"),
        InlineKeyboardButton("💬 Live Support (Admin Chat)", callback_data="live_chat")
    )
    return markup

# 1. Recovery Sub-menu
def recovery_menu_keyboard():
    markup = InlineKeyboardMarkup()
    markup.row_width = 1
    markup.add(
        InlineKeyboardButton("🔹 Social Media Recovery", callback_data="rec_social"),
        InlineKeyboardButton("🔹 Content Restore", callback_data="rec_content"),
        InlineKeyboardButton("🔹 Payout / Monetisation Issue", callback_data="rec_payout"),
        InlineKeyboardButton("🔹 Removal Service", callback_data="rec_removal"),
        InlineKeyboardButton("🔹 Page Protection (Select Duration)", callback_data="rec_protect_select"),
        InlineKeyboardButton("🔙 Back to Main Menu", callback_data="main_menu")
    )
    return markup

# 2. Growth Sub-menu
def growth_menu_keyboard():
    markup = InlineKeyboardMarkup()
    markup.row_width = 1
    markup.add(
        InlineKeyboardButton("🔹 Verification Services", callback_data="grow_verify"),
        InlineKeyboardButton("🔹 Followers & Audience (Calculator)", callback_data="grow_followers_select"),
        InlineKeyboardButton("🔹 Facebook Ad Run", callback_data="grow_ads"),
        InlineKeyboardButton("🔙 Back to Main Menu", callback_data="main_menu")
    )
    return markup

# 3. Premium Apps Sub-menu (With Month Selectors)
def apps_menu_keyboard():
    markup = InlineKeyboardMarkup()
    markup.row_width = 1
    markup.add(
        InlineKeyboardButton("🎬 CapCut Premium (Select Month)", callback_data="app_capcut"),
        InlineKeyboardButton("🎨 Canva Premium", callback_data="app_canva"),
        InlineKeyboardButton("▶️ YouTube Premium", callback_data="app_yt"),
        InlineKeyboardButton("☁️ Drive + Gemini AI Pro", callback_data="app_gemini"),
        InlineKeyboardButton("✈️ Telegram Premium (Select Plan)", callback_data="app_tg"),
        InlineKeyboardButton("🔙 Back to Main Menu", callback_data="main_menu")
    )
    return markup

# 4. Web & Design Sub-menu
def web_menu_keyboard():
    markup = InlineKeyboardMarkup()
    markup.row_width = 1
    markup.add(
        InlineKeyboardButton("🖥️ Landing Page Starter (৳4,499)", callback_data="web_starter"),
        InlineKeyboardButton("⚡ Landing Page Pro (৳10,999)", callback_data="web_pro"),
        InlineKeyboardButton("🔙 Back to Main Menu", callback_data="main_menu")
    )
    return markup

# ----------------- COMMAND HANDLERS -----------------

@bot.message_handler(commands=['start', 'menu'])
def cmd_start(message):
    text = (
        "Welcome to NexFly IT 🥀✨

"
        "NexFly IT, official IT service organization of Team BCT.
"
        "Ethical & verified work, Fast delivery.

"
        "📌 *Available Commands:*
"
        "• /menu - Open Main Menu
"
        "• /recovery - Social Media Recovery & Protection
"
        "• /growth - Verification & Audience Growth
"
        "• /apps - Premium Apps & Subscriptions
"
        "• /web - Web & Landing Page Design
"
        "• /followers - Auto Follower Price Calculator
"
        "• /protection - Page Protection Packages
"
        "• /support - Connect with Live Support Admin
"
        "• /help - View Help & Info

"
        "Please select a category below or use the commands 🙂"
    )
    bot.send_message(message.chat.id, text, parse_mode="Markdown", reply_markup=main_menu_keyboard())

@bot.message_handler(commands=['recovery'])
def cmd_recovery(message):
    text = "🛡️ *Recovery & Protection Services*
Select a sub-category below 🙂"
    bot.send_message(message.chat.id, text, parse_mode="Markdown", reply_markup=recovery_menu_keyboard())

@bot.message_handler(commands=['growth'])
def cmd_growth(message):
    text = "🚀 *Growth & Verification Services*
Select an option below 🙂"
    bot.send_message(message.chat.id, text, parse_mode="Markdown", reply_markup=growth_menu_keyboard())

@bot.message_handler(commands=['apps'])
def cmd_apps(message):
    text = "👑 *Premium Apps & Accounts*
Select an app below to choose plan 🙂"
    bot.send_message(message.chat.id, text, parse_mode="Markdown", reply_markup=apps_menu_keyboard())

@bot.message_handler(commands=['web'])
def cmd_web(message):
    text = "💻 *Web & Landing Page Design*
Select a package below 🙂"
    bot.send_message(message.chat.id, text, parse_mode="Markdown", reply_markup=web_menu_keyboard())

@bot.message_handler(commands=['followers'])
def cmd_followers(message):
    show_follower_platform_menu(message.chat.id)

@bot.message_handler(commands=['protection'])
def cmd_protection(message):
    show_protection_menu(message.chat.id)

@bot.message_handler(commands=['support'])
def cmd_support(message):
    text = "💬 You are now connected to Live Support! Write your message below, and our admin team will reply to you directly 🙂"
    markup = InlineKeyboardMarkup()
    markup.add(InlineKeyboardButton("🔙 Back to Main Menu", callback_data="main_menu"))
    bot.send_message(message.chat.id, text, reply_markup=markup)

@bot.message_handler(commands=['help'])
def cmd_help(message):
    help_text = (
        "🤖 *NexFly IT Support Bot Commands* 🤧

"
        "• /start or /menu - Main Menu
"
        "• /recovery - Recovery Services
"
        "• /growth - Growth & Verification
"
        "• /apps - Premium Apps
"
        "• /web - Web Design
"
        "• /followers - Follower Calculator
"
        "• /protection - Monthly Page Guard
"
        "• /support - Live Chat with Admin"
    )
    bot.send_message(message.chat.id, help_text, parse_mode="Markdown")

# ----------------- HELPER FUNCTIONS FOR CALCULATORS & SELECTORS -----------------

def show_follower_platform_menu(chat_id, message_id=None):
    text = "👥 *Follower Price Calculator*
Select platform to calculate total price based on quantity 🙂"
    markup = InlineKeyboardMarkup()
    markup.row_width = 1
    markup.add(
        InlineKeyboardButton("📘 Facebook / Instagram Followers (৳150 / 1K)", callback_data="fol_platform_fbig"),
        InlineKeyboardButton("🎵 TikTok Followers (৳300 / 1K)", callback_data="fol_platform_tiktok"),
        InlineKeyboardButton("🔙 Back to Growth Menu", callback_data="sub_growth")
    )
    if message_id:
        bot.edit_message_text(chat_id=chat_id, message_id=message_id, text=text, parse_mode="Markdown", reply_markup=markup)
    else:
        bot.send_message(chat_id, text, parse_mode="Markdown", reply_markup=markup)

def show_follower_qty_menu(chat_id, platform, message_id):
    rate = 150 if platform == "fbig" else 300
    name = "FB / IG" if platform == "fbig" else "TikTok"
    text = f"📊 *Select Quantity for {name} Followers*
Rate: ৳{rate} per 1,000 followers 🙂"
    
    markup = InlineKeyboardMarkup()
    markup.row_width = 2
    quantities = [1000, 2000, 3000, 5000, 10000]
    buttons = []
    for qty in quantities:
        total = int((qty / 1000) * rate)
        buttons.append(InlineKeyboardButton(f"{qty//1000}K 👉 ৳{total}", callback_data=f"calc_fol_{platform}_{qty}"))
    
    markup.add(*buttons)
    markup.add(InlineKeyboardButton("🔙 Back to Platform Select", callback_data="grow_followers_select"))
    bot.edit_message_text(chat_id=chat_id, message_id=message_id, text=text, parse_mode="Markdown", reply_markup=markup)

def show_protection_menu(chat_id, message_id=None):
    text = "🛡️ *Page Protection Plans*
Select duration to see price and order 🙂"
    markup = InlineKeyboardMarkup()
    markup.row_width = 1
    markup.add(
        InlineKeyboardButton("📅 1 Month Protection 👉 ৳4,000", callback_data="prot_1m"),
        InlineKeyboardButton("📅 3 Months Protection 👉 ৳12,000", callback_data="prot_3m"),
        InlineKeyboardButton("📅 6 Months Protection 👉 ৳22,000 (Save ৳2,000)", callback_data="prot_6m"),
        InlineKeyboardButton("🔙 Back to Recovery Menu", callback_data="sub_recovery")
    )
    if message_id:
        bot.edit_message_text(chat_id=chat_id, message_id=message_id, text=text, parse_mode="Markdown", reply_markup=markup)
    else:
        bot.send_message(chat_id, text, parse_mode="Markdown", reply_markup=markup)

# ----------------- CALLBACK QUERY HANDLER -----------------

@bot.callback_query_handler(func=lambda call: True)
def callback_inline(call):
    chat_id = call.message.chat.id
    message_id = call.message.message_id
    data = call.data

    if data == "main_menu":
        text = "Welcome to NexFly IT 🥀✨
Please select your required category below or type /menu:"
        bot.edit_message_text(chat_id=chat_id, message_id=message_id, text=text, reply_markup=main_menu_keyboard())

    # --- SUB MENUS ---
    elif data == "sub_recovery":
        text = "🛡️ *Recovery & Protection Categories*
Select a sub-category below 🙂"
        bot.edit_message_text(chat_id=chat_id, message_id=message_id, text=text, parse_mode="Markdown", reply_markup=recovery_menu_keyboard())

    elif data == "sub_growth":
        text = "🚀 *Growth & Verification Categories*
Select an option below 🙂"
        bot.edit_message_text(chat_id=chat_id, message_id=message_id, text=text, parse_mode="Markdown", reply_markup=growth_menu_keyboard())

    elif data == "sub_apps":
        text = "👑 *Premium Apps & Accounts*
Select an app below to select duration/plan 🙂"
        bot.edit_message_text(chat_id=chat_id, message_id=message_id, text=text, parse_mode="Markdown", reply_markup=apps_menu_keyboard())

    elif data == "sub_web":
        text = "💻 *Web & Landing Page Design*
Select a package below 🙂"
        bot.edit_message_text(chat_id=chat_id, message_id=message_id, text=text, parse_mode="Markdown", reply_markup=web_menu_keyboard())

    # --- RECOVERY INSIDE SUB MENUS ---
    elif data == "rec_social":
        text = (
            "📱 *Social Media Recovery* (Delivery: 7–14 days)

"
            "• FB/IG/X Suspended Account: ৳700
"
            "• FB/IG/X Disabled Account: ৳7,000
"
            "• FB/IG/X Hacked Account: ৳3,000 – ৳12,000
"
            "• Facebook Page Suspended: ৳4,000
"
            "• Facebook Page Hacked: ৳3,000 – ৳12,000
"
            "• Gmail Disabled/Hacked/Age Verify: ৳1,500"
        )
        markup = InlineKeyboardMarkup()
        markup.add(InlineKeyboardButton("📲 Order via WhatsApp", url=WA_LINK))
        markup.add(InlineKeyboardButton("🔙 Back to Recovery Menu", callback_data="sub_recovery"))
        bot.edit_message_text(chat_id=chat_id, message_id=message_id, text=text, parse_mode="Markdown", reply_markup=markup)

    elif data == "rec_content":
        text = (
            "📄 *Content Restore* (Delivery: 7–14 days)

"
            "• Copyright Claim: ৳2,500
"
            "• Trademark Claim: ৳4,000
"
            "• Other Issues: ৳2,000"
        )
        markup = InlineKeyboardMarkup()
        markup.add(InlineKeyboardButton("📲 Order via WhatsApp", url=WA_LINK))
        markup.add(InlineKeyboardButton("🔙 Back to Recovery Menu", callback_data="sub_recovery"))
        bot.edit_message_text(chat_id=chat_id, message_id=message_id, text=text, parse_mode="Markdown", reply_markup=markup)

    elif data == "rec_payout":
        text = "💰 *Payout / Monetisation Issue*

• Price Range: ৳3,000 – ৳15,000"
        markup = InlineKeyboardMarkup()
        markup.add(InlineKeyboardButton("📲 Order via WhatsApp", url=WA_LINK))
        markup.add(InlineKeyboardButton("🔙 Back to Recovery Menu", callback_data="sub_recovery"))
        bot.edit_message_text(chat_id=chat_id, message_id=message_id, text=text, parse_mode="Markdown", reply_markup=markup)

    elif data == "rec_removal":
        text = (
            "🗑️ *Removal Service* (Delivery: 3–6 days)

"
            "• FB/IG Account Remove: ৳1,500
"
            "• X Account Remove: ৳5,000
"
            "• FB Page Remove: ৳5,000 – ৳25,000
"
            "• YouTube Content Remove: ৳5,000
"
            "• Telegram Channel/Bot Remove: ৳1,500
"
            "• Scam Website Remove: ৳3,000"
        )
        markup = InlineKeyboardMarkup()
        markup.add(InlineKeyboardButton("📲 Order via WhatsApp", url=WA_LINK))
        markup.add(InlineKeyboardButton("🔙 Back to Recovery Menu", callback_data="sub_recovery"))
        bot.edit_message_text(chat_id=chat_id, message_id=message_id, text=text, parse_mode="Markdown", reply_markup=markup)

    elif data == "rec_protect_select":
        show_protection_menu(chat_id, message_id)

    elif data.startswith("prot_"):
        duration_map = {"prot_1m": ("1 Month", "৳4,000"), "prot_3m": ("3 Months", "৳12,000"), "prot_6m": ("6 Months", "৳22,000")}
        dur, price = duration_map[data]
        text = f"🛡️ *Page Protection Selected*

• Duration: *{dur}*
• Total Price: *{price}*

Tap below to confirm order on WhatsApp 🙂"
        markup = InlineKeyboardMarkup()
        markup.add(InlineKeyboardButton(f"📲 Order {dur} Guard on WhatsApp", url=WA_LINK))
        markup.add(InlineKeyboardButton("🔙 Change Duration", callback_data="rec_protect_select"))
        bot.edit_message_text(chat_id=chat_id, message_id=message_id, text=text, parse_mode="Markdown", reply_markup=markup)

    # --- GROWTH & FOLLOWER CALCULATOR INSIDE SUB MENUS ---
    elif data == "grow_verify":
        text = (
            "✅ *Verification (1 Month)* (Delivery: 24–72h)

"
            "• FB Page/Account: ৳399 – ৳29,999
"
            "• Instagram Account: ৳399 – ৳999
"
            "• WhatsApp Business: ৳699 – ৳14,999
"
            "• X Account: ৳800
"
            "• FB Business Manager: ৳1,500"
        )
        markup = InlineKeyboardMarkup()
        markup.add(InlineKeyboardButton("📲 Order via WhatsApp", url=WA_LINK))
        markup.add(InlineKeyboardButton("🔙 Back to Growth Menu", callback_data="sub_growth"))
        bot.edit_message_text(chat_id=chat_id, message_id=message_id, text=text, parse_mode="Markdown", reply_markup=markup)

    elif data == "grow_followers_select":
        show_follower_platform_menu(chat_id, message_id)

    elif data.startswith("fol_platform_"):
        platform = data.replace("fol_platform_", "")
        show_follower_qty_menu(chat_id, platform, message_id)

    elif data.startswith("calc_fol_"):
        parts = data.split("_")
        platform = parts[2]
        qty = int(parts[3])
        rate = 150 if platform == "fbig" else 300
        p_name = "Facebook / Instagram" if platform == "fbig" else "TikTok"
        total_price = int((qty / 1000) * rate)
        
        text = (
            f"🧮 *Follower Order Summary*

"
            f"• Platform: *{p_name}*
"
            f"• Quantity: *{qty:,} Followers*
"
            f"• Rate: ৳{rate} / 1,000
"
            f"---------------------------
"
            f"💰 *Total Calculated Price: ৳{total_price:,}*

"
            f"Click below to place this order on WhatsApp 🙂"
        )
        markup = InlineKeyboardMarkup()
        markup.add(InlineKeyboardButton(f"📲 Order {qty:,} Followers (৳{total_price:,})", url=WA_LINK))
        markup.add(InlineKeyboardButton("🔄 Change Quantity", callback_data=f"fol_platform_{platform}"))
        markup.add(InlineKeyboardButton("🔙 Back to Growth Menu", callback_data="sub_growth"))
        bot.edit_message_text(chat_id=chat_id, message_id=message_id, text=text, parse_mode="Markdown", reply_markup=markup)

    elif data == "grow_ads":
        text = "📢 *Facebook Ad Run*

Custom Pricing & Professional Setup (Price on request)"
        markup = InlineKeyboardMarkup()
        markup.add(InlineKeyboardButton("📲 Order via WhatsApp", url=WA_LINK))
        markup.add(InlineKeyboardButton("🔙 Back to Growth Menu", callback_data="sub_growth"))
        bot.edit_message_text(chat_id=chat_id, message_id=message_id, text=text, parse_mode="Markdown", reply_markup=markup)

    # --- APPS & MONTH SELECTORS ---
    elif data == "app_capcut":
        text = "🎬 *CapCut Premium Plan Select*
Choose your required duration below 🙂"
        markup = InlineKeyboardMarkup()
        markup.row_width = 1
        markup.add(
            InlineKeyboardButton("🗓️ 1 Month 👉 ৳422", callback_data="cap_1m"),
            InlineKeyboardButton("🗓️ 3 Months 👉 ৳566", callback_data="cap_3m"),
            InlineKeyboardButton("🗓️ 6 Months 👉 ৳1,699", callback_data="cap_6m"),
            InlineKeyboardButton("🗓️ 12 Months 👉 ৳3,199", callback_data="cap_12m"),
            InlineKeyboardButton("🔙 Back to Apps Menu", callback_data="sub_apps")
        )
        bot.edit_message_text(chat_id=chat_id, message_id=message_id, text=text, parse_mode="Markdown", reply_markup=markup)

    elif data.startswith("cap_"):
        cap_map = {"cap_1m": ("1 Month", "৳422"), "cap_3m": ("3 Months", "৳566"), "cap_6m": ("6 Months", "৳1,699"), "cap_12m": ("12 Months", "৳3,199")}
        dur, price = cap_map[data]
        text = f"🎬 *CapCut Premium Selected*

• Duration: *{dur}*
• Price: *{price}*

Tap below to order on WhatsApp 🙂"
        markup = InlineKeyboardMarkup()
        markup.add(InlineKeyboardButton(f"📲 Order CapCut ({dur})", url=WA_LINK))
        markup.add(InlineKeyboardButton("🔙 Change Duration", callback_data="app_capcut"))
        bot.edit_message_text(chat_id=chat_id, message_id=message_id, text=text, parse_mode="Markdown", reply_markup=markup)

    elif data == "app_canva":
        text = "🎨 *Canva Premium*

• Duration: 1 Month
• Price: ৳133"
        markup = InlineKeyboardMarkup()
        markup.add(InlineKeyboardButton("📲 Order Canva Premium", url=WA_LINK))
        markup.add(InlineKeyboardButton("🔙 Back to Apps Menu", callback_data="sub_apps"))
        bot.edit_message_text(chat_id=chat_id, message_id=message_id, text=text, parse_mode="Markdown", reply_markup=markup)

    elif data == "app_yt":
        text = "▶️ *YouTube Premium*

• Duration: 1 Month
• Price: ৳133"
        markup = InlineKeyboardMarkup()
        markup.add(InlineKeyboardButton("📲 Order YouTube Premium", url=WA_LINK))
        markup.add(InlineKeyboardButton("🔙 Back to Apps Menu", callback_data="sub_apps"))
        bot.edit_message_text(chat_id=chat_id, message_id=message_id, text=text, parse_mode="Markdown", reply_markup=markup)

    elif data == "app_gemini":
        text = "☁️ *Google Drive + Gemini AI Pro*

• Duration: 3 Months
• Price: ৳433"
        markup = InlineKeyboardMarkup()
        markup.add(InlineKeyboardButton("📲 Order Gemini AI Pro", url=WA_LINK))
        markup.add(InlineKeyboardButton("🔙 Back to Apps Menu", callback_data="sub_apps"))
        bot.edit_message_text(chat_id=chat_id, message_id=message_id, text=text, parse_mode="Markdown", reply_markup=markup)

    elif data == "app_tg":
        text = "✈️ *Telegram Premium Plan Select*
Choose your required duration below 🙂"
        markup = InlineKeyboardMarkup()
        markup.row_width = 1
        markup.add(
            InlineKeyboardButton("🗓️ 1 Month 👉 ৳499", callback_data="tg_1m"),
            InlineKeyboardButton("🗓️ 1 Year 👉 ৳3,999", callback_data="tg_1y"),
            InlineKeyboardButton("🔙 Back to Apps Menu", callback_data="sub_apps")
        )
        bot.edit_message_text(chat_id=chat_id, message_id=message_id, text=text, parse_mode="Markdown", reply_markup=markup)

    elif data.startswith("tg_"):
        tg_map = {"tg_1m": ("1 Month", "৳499"), "tg_1y": ("1 Year", "৳3,999")}
        dur, price = tg_map[data]
        text = f"✈️ *Telegram Premium Selected*

• Duration: *{dur}*
• Price: *{price}*

Tap below to order on WhatsApp 🙂"
        markup = InlineKeyboardMarkup()
        markup.add(InlineKeyboardButton(f"📲 Order Telegram Premium ({dur})", url=WA_LINK))
        markup.add(InlineKeyboardButton("🔙 Change Duration", callback_data="app_tg"))
        bot.edit_message_text(chat_id=chat_id, message_id=message_id, text=text, parse_mode="Markdown", reply_markup=markup)

    # --- WEB DESIGN SUB-MENUS ---
    elif data == "web_starter":
        text = (
            "💻 *Landing Page Starter – ৳4,499*

"
            "• 1-Page Professional Landing Page
"
            "• Modern & Clean UI/UX Design
"
            "• Fully Mobile Responsive & Fast
"
            "• WhatsApp & Contact CTA
"
            "• 30 Days Free Support"
        )
        markup = InlineKeyboardMarkup()
        markup.add(InlineKeyboardButton("📲 Order Starter Pack", url=WA_LINK))
        markup.add(InlineKeyboardButton("🔙 Back to Web Menu", callback_data="sub_web"))
        bot.edit_message_text(chat_id=chat_id, message_id=message_id, text=text, parse_mode="Markdown", reply_markup=markup)

    elif data == "web_pro":
        text = (
            "⚡ *Landing Page Pro – ৳10,999*

"
            "• Premium Custom UI/UX Design
"
            "• Speed & Basic SEO Optimization
"
            "• Direct Inquiry Form + Analytics Setup
"
            "• 90 Days Technical Support"
        )
        markup = InlineKeyboardMarkup()
        markup.add(InlineKeyboardButton("📲 Order Pro Pack", url=WA_LINK))
        markup.add(InlineKeyboardButton("🔙 Back to Web Menu", callback_data="sub_web"))
        bot.edit_message_text(chat_id=chat_id, message_id=message_id, text=text, parse_mode="Markdown", reply_markup=markup)

    elif data == "live_chat":
        text = "💬 You are now connected to Live Support! Send any message or question below, and our admin will reply directly to you 🙂"
        markup = InlineKeyboardMarkup()
        markup.add(InlineKeyboardButton("🔙 Back to Main Menu", callback_data="main_menu"))
        bot.send_message(chat_id, text, reply_markup=markup)

# ----------------- BULLETPROOF LIVE CHAT & MESSAGE FORWARDING -----------------

@bot.message_handler(func=lambda message: True)
def handle_messages(message):
    chat_id = message.chat.id
    
    # Ignore commands
    if message.text and message.text.startswith('/'):
        return

    # 1. Admin Replying to User
    if chat_id == ADMIN_ID and message.reply_to_message:
        try:
            reply_text = message.reply_to_message.text
            if "User ID:" in reply_text:
                target_id_str = reply_text.split("User ID:")[1].split("
")[0].replace("`", "").strip()
                target_id = int(target_id_str)
                bot.send_message(target_id, f"💬 *Support Reply from Admin:*
{message.text}", parse_mode="Markdown")
                bot.send_message(ADMIN_ID, "✅ Reply sent successfully to the user! 🙂")
            else:
                bot.send_message(ADMIN_ID, "🤧 Couldn't extract User ID. Reply directly to the forwarded message box.")
        except Exception as e:
            bot.send_message(ADMIN_ID, f"🤧 Failed to send reply: {str(e)}")
        return

    # 2. User Sending Message to Admin
    if chat_id != ADMIN_ID:
        msg_to_admin = (
            f"📩 *New Support Message*
"
            f"👤 From: {message.from_user.first_name} (@{message.from_user.username or 'No_Username'})
"
            f"🆔 User ID: `{chat_id}`

"
            f"💬 Message: {message.text}"
        )
        try:
            bot.send_message(ADMIN_ID, msg_to_admin, parse_mode="Markdown")
            markup = InlineKeyboardMarkup()
            markup.add(InlineKeyboardButton("🔙 Back to Main Menu", callback_data="main_menu"))
            bot.send_message(chat_id, "Message received! Our team will review and reply to you soon 🙂", reply_markup=markup)
        except Exception as e:
            print(f"Error forwarding message: {e}")

# ----------------- BOT RUNNER -----------------

if __name__ == "__main__":
    print("Starting Keep Alive Server...")
    keep_alive()
    print("Bot is running with full Command System & Dynamic Calculators...")
    bot.infinity_polling()

import os
import time
import html
import logging
import psycopg2
from threading import Thread, Lock

from flask import Flask
import telebot
from telebot import util
from telebot.types import InlineKeyboardMarkup, InlineKeyboardButton, BotCommand
from telebot.apihelper import ApiTelegramException

logging.basicConfig(level=logging.INFO, format="%(asctime)s %(levelname)s %(message)s")

# ====================== CONFIG (Render Environment Variables) ======================
TOKEN = os.environ["BOT_TOKEN"]                                  # REQUIRED
ADMIN_ID = int(os.environ.get("ADMIN_ID", "8365272832"))         # Owner user ID
GROUP_ID = int(os.environ.get("GROUP_ID", "-1004335533710"))     # Support group (Topics ON)
DATABASE_URL = os.environ["DATABASE_URL"]                        # REQUIRED (Neon / Supabase Postgres URL)
WA_LINK = "https://wa.me/message/QFALT7WQHZ2CN1"

bot = telebot.TeleBot(TOKEN, threaded=True, num_threads=8)

# ====================== KEEP ALIVE (Render) ======================
app = Flask(__name__)


@app.route("/")
def home():
    return "NexFly IT Bot is running alive!"


@app.route("/health")
def health():
    return "ok"


def keep_alive():
    port = int(os.environ.get("PORT", 8080))
    Thread(target=lambda: app.run(host="0.0.0.0", port=port), daemon=True).start()


# ====================== DATABASE ======================
db_lock = Lock()


def db_connect():
    return psycopg2.connect(DATABASE_URL, connect_timeout=10, keepalives=1,
                            keepalives_idle=30, keepalives_interval=10, keepalives_count=5)


conn = db_connect()
with conn.cursor() as _c:
    _c.execute("""CREATE TABLE IF NOT EXISTS users(
        user_id BIGINT PRIMARY KEY,
        name TEXT, username TEXT,
        thread_id BIGINT,
        banned INTEGER DEFAULT 0,
        live INTEGER DEFAULT 0,
        joined DOUBLE PRECISION)""")
conn.commit()


def q(sql, args=(), one=False, commit=False):
    """Run a query. Auto-reconnects if the free DB went to sleep / dropped the connection."""
    global conn
    sql = sql.replace("?", "%s")
    with db_lock:
        for attempt in (1, 2):
            try:
                with conn.cursor() as cur:
                    cur.execute(sql, args)
                    res = None
                    if cur.description:
                        res = cur.fetchone() if one else cur.fetchall()
                conn.commit()
                return res
            except (psycopg2.OperationalError, psycopg2.InterfaceError):
                if attempt == 2:
                    raise
                try:
                    conn.close()
                except Exception:
                    pass
                conn = db_connect()
            except Exception:
                conn.rollback()
                raise


def upsert_user(u):
    q("""INSERT INTO users(user_id,name,username,joined) VALUES(?,?,?,?)
         ON CONFLICT(user_id) DO UPDATE SET name=excluded.name, username=excluded.username""",
      (u.id, u.first_name or "", u.username or "", time.time()), commit=True)


COLS = "user_id,name,username,thread_id,banned,live"


def get_user(uid):
    return q(f"SELECT {COLS} FROM users WHERE user_id=?", (uid,), one=True)


def user_by_thread(tid):
    return q(f"SELECT {COLS} FROM users WHERE thread_id=?", (tid,), one=True)


# ====================== UI HELPERS ======================
def B(text, cb=None, url=None):
    return InlineKeyboardButton(text, callback_data=cb, url=url)


def kb(*buttons, w=1):
    m = InlineKeyboardMarkup(row_width=w)
    m.add(*buttons)
    return m


BACK_MAIN = B("🔙 Back to Main Menu", "main_menu")
CHAT_BTN = B("💬 Chat with Support", "live_chat")


def edit(call, text, markup=None):
    try:
        bot.edit_message_text(text, chat_id=call.message.chat.id, message_id=call.message.message_id,
                              parse_mode="Markdown", reply_markup=markup)
    except ApiTelegramException as e:
        if "not modified" not in str(e):
            logging.error("edit error: %s", e)


def react(chat_id, msg_id, emoji="👍"):
    try:
        bot.set_message_reaction(chat_id, msg_id, [telebot.types.ReactionTypeEmoji(emoji)])
    except Exception:
        pass


# ====================== MENUS (views return (text, markup)) ======================
START_TEXT = ("Welcome to NexFly IT 🥀✨\n\nNexFly IT, official IT service organization of Team BCT.\n"
              "Ethical & verified work, Fast delivery.\n\n📌 *Available Commands:*\n"
              "• /menu - Open Main Menu\n• /recovery - Social Media Recovery & Protection\n"
              "• /growth - Verification & Audience Growth\n• /apps - Premium Apps & Subscriptions\n"
              "• /web - Web & Landing Page Design\n• /followers - Auto Follower Price Calculator\n"
              "• /protection - Page Protection Packages\n• /support - Live Chat with Support Team\n"
              "• /help - View Help & Info\n\nPlease select a category below or use the commands 🙂")


def v_main(full=False):
    text = START_TEXT if full else "Welcome to NexFly IT 🥀✨\nPlease select your required category below or type /menu:"
    return text, kb(
        B("🛡️ Recovery & Protection", "sub_recovery"),
        B("🚀 Growth & Verification", "sub_growth"),
        B("👑 Premium Apps", "sub_apps"),
        B("💻 Web & Design", "sub_web"),
        B("💬 Live Support (Chat Now)", "live_chat"))


def v_recovery():
    return "🛡️ *Recovery & Protection Services*\nSelect a sub-category below 🙂", kb(
        B("🔹 Social Media Recovery", "rec_social"),
        B("🔹 Content Restore", "rec_content"),
        B("🔹 Payout / Monetisation Issue", "rec_payout"),
        B("🔹 Removal Service", "rec_removal"),
        B("🔹 Page Protection (Select Duration)", "rec_protect_select"),
        BACK_MAIN)


def v_growth():
    return "🚀 *Growth & Verification Services*\nSelect an option below 🙂", kb(
        B("🔹 Verification Services", "grow_verify"),
        B("🔹 Followers & Audience (Calculator)", "grow_followers_select"),
        B("🔹 Facebook Ad Run", "grow_ads"),
        BACK_MAIN)


def v_apps():
    return "👑 *Premium Apps & Accounts*\nSelect an app below to choose plan 🙂", kb(
        B("🎬 CapCut Premium (Select Month)", "app_capcut"),
        B("🎨 Canva Premium", "app_canva"),
        B("▶️ YouTube Premium", "app_yt"),
        B("☁️ Drive + Gemini AI Pro", "app_gemini"),
        B("✈️ Telegram Premium (Select Plan)", "app_tg"),
        BACK_MAIN)


def v_web():
    return "💻 *Web & Landing Page Design*\nSelect a package below 🙂", kb(
        B("🖥️ Landing Page Starter (৳4,499)", "web_starter"),
        B("⚡ Landing Page Pro (৳10,999)", "web_pro"),
        BACK_MAIN)


def v_protection():
    return "🛡️ *Page Protection Plans*\nSelect duration to see price and order 🙂", kb(
        B("📅 1 Month Protection 👉 ৳4,000", "prot_1m"),
        B("📅 3 Months Protection 👉 ৳12,000", "prot_3m"),
        B("📅 6 Months Protection 👉 ৳22,000 (Save ৳2,000)", "prot_6m"),
        B("🔙 Back to Recovery Menu", "sub_recovery"))


def v_followers_platform():
    return "👥 *Follower Price Calculator*\nSelect platform to calculate total price based on quantity 🙂", kb(
        B("📘 Facebook / Instagram Followers (৳150 / 1K)", "fol_platform_fbig"),
        B("🎵 TikTok Followers (৳300 / 1K)", "fol_platform_tiktok"),
        B("🔙 Back to Growth Menu", "sub_growth"))


def v_followers_qty(platform):
    rate = 150 if platform == "fbig" else 300
    name = "FB / IG" if platform == "fbig" else "TikTok"
    text = f"📊 *Select Quantity for {name} Followers*\nRate: ৳{rate} per 1,000 followers 🙂"
    m = InlineKeyboardMarkup(row_width=2)
    m.add(*[B(f"{qty // 1000}K 👉 ৳{int(qty / 1000 * rate)}", f"calc_fol_{platform}_{qty}")
            for qty in (1000, 2000, 3000, 5000, 10000)])
    m.add(B("🔙 Back to Platform Select", "grow_followers_select"))
    return text, m


def v_capcut():
    return "🎬 *CapCut Premium Plan Select*\nChoose your required duration below 🙂", kb(
        B("🗓️ 1 Month 👉 ৳422", "cap_1m"),
        B("🗓️ 3 Months 👉 ৳566", "cap_3m"),
        B("🗓️ 6 Months 👉 ৳1,699", "cap_6m"),
        B("🗓️ 12 Months 👉 ৳3,199", "cap_12m"),
        B("🔙 Back to Apps Menu", "sub_apps"))


def v_tg():
    return "✈️ *Telegram Premium Plan Select*\nChoose your required duration below 🙂", kb(
        B("🗓️ 1 Month 👉 ৳499", "tg_1m"),
        B("🗓️ 1 Year 👉 ৳3,999", "tg_1y"),
        B("🔙 Back to Apps Menu", "sub_apps"))


VIEWS = {
    "main_menu": lambda: v_main(False),
    "sub_recovery": v_recovery, "sub_growth": v_growth, "sub_apps": v_apps, "sub_web": v_web,
    "rec_protect_select": v_protection, "grow_followers_select": v_followers_platform,
    "app_capcut": v_capcut, "app_tg": v_tg,
}

# Static info pages: key -> (text, back_callback, back_label)
PAGES = {
    "rec_social": ("📱 *Social Media Recovery* (Delivery: 7–14 days)\n\n• FB/IG/X Suspended Account: ৳700\n• FB/IG/X Disabled Account: ৳7,000\n• FB/IG/X Hacked Account: ৳3,000 – ৳12,000\n• Facebook Page Suspended: ৳4,000\n• Facebook Page Hacked: ৳3,000 – ৳12,000\n• Gmail Disabled/Hacked/Age Verify: ৳1,500", "sub_recovery", "🔙 Back to Recovery Menu"),
    "rec_content": ("📄 *Content Restore* (Delivery: 7–14 days)\n\n• Copyright Claim: ৳2,500\n• Trademark Claim: ৳4,000\n• Other Issues: ৳2,000", "sub_recovery", "🔙 Back to Recovery Menu"),
    "rec_payout": ("💰 *Payout / Monetisation Issue*\n\n• Price Range: ৳3,000 – ৳15,000", "sub_recovery", "🔙 Back to Recovery Menu"),
    "rec_removal": ("🗑️ *Removal Service* (Delivery: 3–6 days)\n\n• FB/IG Account Remove: ৳1,500\n• X Account Remove: ৳5,000\n• FB Page Remove: ৳5,000 – ৳25,000\n• YouTube Content Remove: ৳5,000\n• Telegram Channel/Bot Remove: ৳1,500\n• Scam Website Remove: ৳3,000", "sub_recovery", "🔙 Back to Recovery Menu"),
    "grow_verify": ("✅ *Verification (1 Month)* (Delivery: 24–72h)\n\n• FB Page/Account: ৳399 – ৳29,999\n• Instagram Account: ৳399 – ৳999\n• WhatsApp Business: ৳699 – ৳14,999\n• X Account: ৳800\n• FB Business Manager: ৳1,500", "sub_growth", "🔙 Back to Growth Menu"),
    "grow_ads": ("📢 *Facebook Ad Run*\n\nCustom Pricing & Professional Setup (Price on request)", "sub_growth", "🔙 Back to Growth Menu"),
    "app_canva": ("🎨 *Canva Premium*\n\n• Duration: 1 Month\n• Price: ৳133", "sub_apps", "🔙 Back to Apps Menu"),
    "app_yt": ("▶️ *YouTube Premium*\n\n• Duration: 1 Month\n• Price: ৳133", "sub_apps", "🔙 Back to Apps Menu"),
    "app_gemini": ("☁️ *Google Drive + Gemini AI Pro*\n\n• Duration: 3 Months\n• Price: ৳433", "sub_apps", "🔙 Back to Apps Menu"),
    "web_starter": ("💻 *Landing Page Starter – ৳4,499*\n\n• 1-Page Professional Landing Page\n• Modern & Clean UI/UX Design\n• Fully Mobile Responsive & Fast\n• WhatsApp & Contact CTA\n• 30 Days Free Support", "sub_web", "🔙 Back to Web Menu"),
    "web_pro": ("⚡ *Landing Page Pro – ৳10,999*\n\n• Premium Custom UI/UX Design\n• Speed & Basic SEO Optimization\n• Direct Inquiry Form + Analytics Setup\n• 90 Days Technical Support", "sub_web", "🔙 Back to Web Menu"),
}

# Plan selections: key -> (title, duration, price, change-duration callback)
PLANS = {
    "prot_1m": ("🛡️ *Page Protection Selected*", "1 Month", "৳4,000", "rec_protect_select"),
    "prot_3m": ("🛡️ *Page Protection Selected*", "3 Months", "৳12,000", "rec_protect_select"),
    "prot_6m": ("🛡️ *Page Protection Selected*", "6 Months", "৳22,000", "rec_protect_select"),
    "cap_1m": ("🎬 *CapCut Premium Selected*", "1 Month", "৳422", "app_capcut"),
    "cap_3m": ("🎬 *CapCut Premium Selected*", "3 Months", "৳566", "app_capcut"),
    "cap_6m": ("🎬 *CapCut Premium Selected*", "6 Months", "৳1,699", "app_capcut"),
    "cap_12m": ("🎬 *CapCut Premium Selected*", "12 Months", "৳3,199", "app_capcut"),
    "tg_1m": ("✈️ *Telegram Premium Selected*", "1 Month", "৳499", "app_tg"),
    "tg_1y": ("✈️ *Telegram Premium Selected*", "1 Year", "৳3,999", "app_tg"),
}

HELP_TEXT = ("🤖 *NexFly IT Support Bot Commands*\n\n• /start or /menu - Main Menu\n• /recovery - Recovery Services\n"
             "• /growth - Growth & Verification\n• /apps - Premium Apps\n• /web - Web Design\n"
             "• /followers - Follower Calculator\n• /protection - Page Protection\n• /support - Live Chat with Support")

CMD_VIEWS = {
    "start": lambda: v_main(True), "menu": lambda: v_main(True),
    "recovery": v_recovery, "growth": v_growth, "apps": v_apps, "web": v_web,
    "followers": v_followers_platform, "protection": v_protection,
}


# ====================== LIVE CHAT CORE ======================
def user_card(uid, name, username):
    uname = f"@{html.escape(username)}" if username else "No username"
    return (f"👤 <b>{html.escape(name or 'User')}</b>\n🔗 {uname}\n🆔 <code>{uid}</code>\n"
            f'📎 <a href="tg://user?id={uid}">Open profile</a>\n\n'
            "💡 Reply inside this topic to answer the user.\n"
            "📝 Start a message with <code>#</code> for an internal note (not sent to user).\n"
            "/close – end chat • /ban – block user")


def ensure_topic(row):
    uid, name, username = row[0], row[1], row[2]
    title = f"{name or 'User'} • {uid}"[:128]
    topic = bot.create_forum_topic(GROUP_ID, title)
    tid = topic.message_thread_id
    q("UPDATE users SET thread_id=? WHERE user_id=?", (tid, uid), commit=True)
    bot.send_message(GROUP_ID, user_card(uid, name, username), message_thread_id=tid, parse_mode="HTML")
    return tid


def relay_to_group(message, retry=True):
    """Copy ANY message type (text/photo/voice/file/...) from user into their own topic."""
    uid = message.from_user.id
    row = get_user(uid)
    tid, live = row[3], row[5]
    try:
        if not tid:
            tid = ensure_topic(row)
        elif not live:
            try:
                bot.reopen_forum_topic(GROUP_ID, tid)
            except ApiTelegramException:
                pass
            bot.send_message(GROUP_ID, "🔔 User started the chat again.", message_thread_id=tid)
        q("UPDATE users SET live=1 WHERE user_id=?", (uid,), commit=True)
        bot.copy_message(GROUP_ID, uid, message.message_id, message_thread_id=tid)
        return True
    except ApiTelegramException as e:
        if retry and "thread not found" in str(e).lower():
            q("UPDATE users SET thread_id=NULL WHERE user_id=?", (uid,), commit=True)
            return relay_to_group(message, retry=False)
        logging.error("relay error: %s", e)
        try:
            bot.send_message(ADMIN_ID, f"⚠️ Live chat error: {e}\nCheck: Topics ON + bot admin with 'Manage Topics'.")
        except Exception:
            pass
        return False


def end_chat(uid, by_admin=False):
    row = get_user(uid)
    if not row:
        return False
    q("UPDATE users SET live=0 WHERE user_id=?", (uid,), commit=True)
    if row[3]:
        try:
            bot.send_message(GROUP_ID, "🔒 Chat closed by " + ("support." if by_admin else "user."),
                             message_thread_id=row[3])
            bot.close_forum_topic(GROUP_ID, row[3])
        except ApiTelegramException as e:
            logging.warning("close topic: %s", e)
    if by_admin:
        try:
            bot.send_message(uid, "🔒 This chat was closed by our team.\nSend a new message anytime to start again 🙂",
                             reply_markup=kb(BACK_MAIN))
        except Exception:
            pass
    return True


def support_intro(chat_id):
    bot.send_message(chat_id,
                     "💬 *Live Support*\n\nSend your message here — text, photo, voice, video or file. "
                     "Our team will reply right here 🙂",
                     parse_mode="Markdown", reply_markup=kb(B("❌ End Chat", "end_chat"), BACK_MAIN))


def target_from(m):
    if m.message_thread_id:
        r = user_by_thread(m.message_thread_id)
        if r:
            return r[0]
    parts = (m.text or "").split()
    if len(parts) > 1 and parts[1].lstrip("-").isdigit():
        return int(parts[1])
    return None


def do_broadcast(text, admin_chat):
    ids = [r[0] for r in q("SELECT user_id FROM users WHERE banned=0")]
    ok = fail = 0
    for i in ids:
        try:
            bot.send_message(i, text)
            ok += 1
        except Exception:
            fail += 1
        time.sleep(0.05)
    bot.send_message(admin_chat, f"📣 Broadcast done.\n✅ Sent: {ok}\n❌ Failed: {fail}")


# ====================== HANDLERS (order matters) ======================
def staff_ctx(m):
    return m.chat.id == GROUP_ID or (m.from_user and m.from_user.id == ADMIN_ID)


@bot.message_handler(commands=["close", "ban", "unban", "info", "stats", "broadcast"], func=staff_ctx)
def staff_cmds(m):
    cmd = m.text.split()[0][1:].split("@")[0].lower()
    is_admin = m.from_user.id == ADMIN_ID
    tid = m.message_thread_id if m.chat.id == GROUP_ID else None

    def say(text):
        bot.send_message(m.chat.id, text, message_thread_id=tid)

    if cmd == "stats":
        if not is_admin:
            return
        total = q("SELECT COUNT(*) FROM users", one=True)[0]
        live = q("SELECT COUNT(*) FROM users WHERE live=1", one=True)[0]
        banned = q("SELECT COUNT(*) FROM users WHERE banned=1", one=True)[0]
        return say(f"📊 Users: {total}\n💬 Live chats: {live}\n🚫 Banned: {banned}")

    if cmd == "broadcast":
        if not is_admin:
            return
        parts = m.text.split(maxsplit=1)
        if len(parts) < 2:
            return say("Usage: /broadcast your message")
        say("📣 Broadcasting...")
        return Thread(target=do_broadcast, args=(parts[1], m.chat.id), daemon=True).start()

    uid = target_from(m)
    if not uid:
        return say("Use this inside a user's topic (or add the user ID).")

    if cmd == "close":
        end_chat(uid, by_admin=True)
    elif cmd == "info":
        r = get_user(uid)
        if r:
            bot.send_message(m.chat.id, user_card(uid, r[1], r[2]), message_thread_id=tid, parse_mode="HTML")
    elif cmd in ("ban", "unban"):
        if not is_admin:
            return say("Only the owner can do this.")
        banned = 1 if cmd == "ban" else 0
        q("UPDATE users SET banned=? WHERE user_id=?", (banned, uid), commit=True)
        if banned:
            end_chat(uid, by_admin=False)
        say(f"{'🚫 Banned' if banned else '✅ Unbanned'} {uid}")


@bot.message_handler(func=lambda m: m.chat.id == GROUP_ID, content_types=util.content_type_media)
def on_group_message(m):
    """Staff reply inside a user's topic -> delivered to that user (all media types)."""
    if (m.from_user and m.from_user.is_bot) or not m.message_thread_id:
        return
    if m.text and (m.text.startswith("/") or m.text.startswith("#")):
        return  # commands & internal notes are not sent
    row = user_by_thread(m.message_thread_id)
    if not row:
        return
    try:
        bot.copy_message(row[0], GROUP_ID, m.message_id)
        react(GROUP_ID, m.message_id, "👍")
    except ApiTelegramException as e:
        bot.send_message(GROUP_ID, f"⚠️ Could not deliver: {e}", message_thread_id=m.message_thread_id)


def is_private(m):
    return m.chat.type == "private"


@bot.message_handler(commands=list(CMD_VIEWS), func=is_private)
def on_menu_cmd(m):
    upsert_user(m.from_user)
    cmd = m.text.split()[0][1:].split("@")[0].lower()
    text, markup = CMD_VIEWS[cmd]()
    bot.send_message(m.chat.id, text, parse_mode="Markdown", reply_markup=markup)


@bot.message_handler(commands=["support"], func=is_private)
def on_support(m):
    upsert_user(m.from_user)
    support_intro(m.chat.id)


@bot.message_handler(commands=["help"], func=is_private)
def on_help(m):
    bot.send_message(m.chat.id, HELP_TEXT, parse_mode="Markdown")


@bot.message_handler(func=is_private, content_types=util.content_type_media)
def on_user_message(m):
    if m.text and m.text.startswith("/"):
        return
    u = m.from_user
    upsert_user(u)
    row = get_user(u.id)
    if row[4]:
        return bot.send_message(u.id, "🚫 You are blocked from support.")
    was_live = row[5]
    if not relay_to_group(m):
        return bot.send_message(u.id, "⚠️ Support is temporarily unavailable. Please contact us on WhatsApp.",
                                reply_markup=kb(B("📲 WhatsApp", url=WA_LINK)))
    if was_live:
        react(u.id, m.message_id, "👀")
    else:
        bot.send_message(u.id, "✅ Connected to Live Support! Our team will reply here shortly 🙂",
                         reply_markup=kb(B("❌ End Chat", "end_chat")))


@bot.callback_query_handler(func=lambda c: True)
def on_callback(call):
    d = call.data
    try:
        bot.answer_callback_query(call.id)
    except Exception:
        pass

    if d in VIEWS:
        edit(call, *VIEWS[d]())
    elif d in PAGES:
        text, back_cb, back_label = PAGES[d]
        edit(call, text, kb(B("📲 Order via WhatsApp", url=WA_LINK), CHAT_BTN, B(back_label, back_cb)))
    elif d in PLANS:
        title, dur, price, change_cb = PLANS[d]
        text = f"{title}\n\n• Duration: *{dur}*\n• Price: *{price}*\n\nTap below to confirm order on WhatsApp 🙂"
        edit(call, text, kb(B(f"📲 Order ({dur}) on WhatsApp", url=WA_LINK), B("🔙 Change Duration", change_cb)))
    elif d.startswith("fol_platform_"):
        edit(call, *v_followers_qty(d.replace("fol_platform_", "")))
    elif d.startswith("calc_fol_"):
        _, _, platform, qty = d.split("_")
        qty = int(qty)
        rate = 150 if platform == "fbig" else 300
        p_name = "Facebook / Instagram" if platform == "fbig" else "TikTok"
        total = int(qty / 1000 * rate)
        text = (f"🧮 *Follower Order Summary*\n\n• Platform: *{p_name}*\n• Quantity: *{qty:,} Followers*\n"
                f"• Rate: ৳{rate} / 1,000\n---------------------------\n💰 *Total Calculated Price: ৳{total:,}*\n\n"
                "Click below to place this order on WhatsApp 🙂")
        edit(call, text, kb(B(f"📲 Order {qty:,} Followers (৳{total:,})", url=WA_LINK),
                            B("🔄 Change Quantity", f"fol_platform_{platform}"),
                            B("🔙 Back to Growth Menu", "sub_growth")))
    elif d == "live_chat":
        upsert_user(call.from_user)
        support_intro(call.message.chat.id)
    elif d == "end_chat":
        end_chat(call.from_user.id, by_admin=False)
        edit(call, "🔒 Chat ended. Thank you! Send /support anytime to chat again 🙂", kb(BACK_MAIN))


# ====================== START ======================
if __name__ == "__main__":
    print("Starting Keep Alive Server...")
    keep_alive()
    bot.remove_webhook()
    try:
        bot.set_my_commands([
            BotCommand("menu", "Main menu"), BotCommand("support", "Live chat with support"),
            BotCommand("recovery", "Recovery & protection"), BotCommand("growth", "Verification & growth"),
            BotCommand("apps", "Premium apps"), BotCommand("web", "Web & design"),
            BotCommand("followers", "Follower calculator"), BotCommand("protection", "Page protection"),
            BotCommand("help", "Help")])
        chat = bot.get_chat(GROUP_ID)
        if not getattr(chat, "is_forum", False):
            logging.warning("Support group is NOT a forum! Enable Topics in group settings.")
    except Exception as e:
        logging.warning("Startup check: %s", e)
    print("Bot is running with Topic-based Live Chat...")
    bot.infinity_polling(skip_pending=True, timeout=30, long_polling_timeout=30)

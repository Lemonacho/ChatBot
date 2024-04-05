import telebot
import threading
import sqlite3
from datetime import datetime, timedelta
import logging
import time
from telebot import types
import random

TOKEN = '5856301284:AAFkyyN5_lp6N1bHSJxSczS3qsMOYDs8K2Y'
bot = telebot.TeleBot(TOKEN)

# 5856301284:AAFkyyN5_lp6N1bHSJxSczS3qsMOYDs8K2Y CONNOR
# 6637698496:AAGJrzuOV57E9Hpm-6e4CHh-3bkM2yteW6U TEST

logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO)
logger = logging.getLogger(__name__)

ADM_ID = [985329138, 6855430781, 6814115227, 6858984069, 6489407861, 6805313098, 1070083225, 7056431933, 6480044498]
YOUR_CHAT_ID = -1002011863502
# -1002011863502 CONNOR
# -1001909691999 TEST

conn = sqlite3.connect('punishments.db')
cursor = conn.cursor()

cursor.execute('''
    CREATE TABLE IF NOT EXISTS punishments (
        user_id INTEGER PRIMARY KEY,
        punishment_number INTEGER,
        punishment_time INTEGER,
        block INTEGER DEFAULT 0,
        reason TEXT
    )
''')

cursor.execute('''
    CREATE TABLE IF NOT EXISTS bans (
        user_id INTEGER PRIMARY KEY,
        admin_id INTEGER,
        ban_timestamp INTEGER
    )
''')

cursor.execute('''
    CREATE TABLE IF NOT EXISTS users (
        id INTEGER PRIMARY KEY,
        user_id INTEGER,
        username TEXT,
        first_name TEXT,
        last_name TEXT
    )
''')

conn.commit()

def update_users_db():
    try:
        cursor.execute("SELECT user_id FROM users")
        existing_user_ids = {row[0] for row in cursor.fetchall()}

        members = bot.get_chat_members(YOUR_CHAT_ID)

        for member in members:
            user_id = member.user.id
            if user_id not in existing_user_ids:
                username = member.user.username or ''
                first_name = member.user.first_name or ''
                last_name = member.user.last_name or ''
                cursor.execute("INSERT INTO users (user_id, username, first_name, last_name) VALUES (?, ?, ?, ?)",
                               (user_id, username, first_name, last_name))
                conn.commit()
                logger.info(f"Добавлен пользователь {user_id} в базу данных.")

    except Exception as e:
        logger.error(f"Ошибка при обновлении базы данных пользователей: {e}")

    threading.Timer(1200, update_users_db).start()

update_users_db()



def send_welcome_message(chat_id, user):
    welcome_message = """
<i><b>‼️ ПРАВИЛА ЧАТА ‼️</b></i>
<i><b>-Не оскорблять других участников</b></i>
<i><b>-Не попрошайничать</b></i>
<i><b>-Запрещается дезинформация об администрации проекта/проекте </b></i>
<i><b>-Запрещается продажа каких либо услуг/товаров без согласования куратора</b></i>
<i><b>-Запрещается обсуждение политики в любом виде</b></i>
<i><b>-Запрещается упоминание других проектов в чате</b></i>
<i><b>-Запрещается ЧЕК БИО</b></i>
<i><b>-Запрещается 18+ контенту</b></i>

<i><b>⚙️Команды чата⚙️</b></i>
<code>/тп</code> - <b>Поддержка Marvel Team⚙️</b>
<code>/куратор</code> - <b>Наш любимый куратор 👑</b>
<code>/помощники</code> - <b>Помощники куратора📖</b>
<code>/мануал</code> - <b>Наш мануал 📚</b>

<code>/займру</code> - <b>Список займов в России🇷🇺</b>
<code>/займкз</code> - <b>Список в Казахстане🇰🇿</b>
<code>/займукр</code> - <b>Список займов в Украине🇺🇦</b>
 <code>/help</code> - <b>Помощь по командам чата💭</b>
    """.format(
        user_name=user.username,
        user_id=user.id,
        user_first_name=user.first_name,
    )

    msg = bot.send_message(
        chat_id,
        welcome_message,
        parse_mode="HTML",
        disable_web_page_preview=True,
    )

    threading.Timer(15, lambda: bot.delete_message(msg.chat.id, msg.message_id)).start()

@bot.message_handler(content_types=['new_chat_members'])
def handle_new_chat_members(message):
    chat_id = message.chat.id

    new_members = message.new_chat_members
    if new_members:
        for member in new_members:
            send_welcome_message(chat_id, member)

@bot.message_handler(func=lambda message: message.chat.id == YOUR_CHAT_ID, commands=['правила', 'Правила'])
def handle_tp(message):
    user_id = get_user_id(message)

    msg = bot.send_message(
        message.chat.id,
        """
<i><b>‼️ ПРАВИЛА ЧАТА ‼️</b></i>
<i><b>-Не оскорблять других участников</b></i>
<i><b>-Не попрошайничать</b></i>
<i><b>-Запрещается дезинформация об администрации проекта/проекте </b></i>
<i><b>-Запрещается продажа каких либо услуг/товаров без согласования куратора</b></i>
<i><b>-Запрещается обсуждение политики в любом виде</b></i>
<i><b>-Запрещается упоминание других проектов в чате</b></i>
<i><b>-Запрещается ЧЕК БИО</b></i>
<i><b>-Запрещается 18+ контенту</b></i>
        """,
        parse_mode="HTML",
        disable_web_page_preview=True,
    )

    threading.Timer(1, lambda: bot.delete_message(message.chat.id, message.message_id)).start()

    threading.Timer(20, lambda: bot.delete_message(message.chat.id, msg.message_id)).start()

@bot.message_handler(func=lambda message: message.chat.id == YOUR_CHAT_ID, commands=['pressF', 'pressf' , 'Pressf' , 'Pressf'])
def handle_tp(message):
    user_id = get_user_id(message)

    msg = bot.send_message(
        message.chat.id,
        """
<i><b>Press F бывшим помощникам , мы вас любим❤️</b></i>
        """,
        parse_mode="HTML",
        disable_web_page_preview=True,
    )

    threading.Timer(1, lambda: bot.delete_message(message.chat.id, message.message_id)).start()

    threading.Timer(10, lambda: bot.delete_message(message.chat.id, msg.message_id)).start()

import logging

@bot.message_handler(func=lambda message: message.chat.id == YOUR_CHAT_ID, commands=['ban' , 'Ban'])
def handle_ban(message):
    if message.from_user.id not in ADM_ID:
        return

    user_id = message.reply_to_message.from_user.id if message.reply_to_message and message.reply_to_message.from_user else None

    if user_id:
        
        add_ban(user_id, message.from_user.id, datetime.now().timestamp())
        
        bot.kick_chat_member(YOUR_CHAT_ID, user_id)
        
        bot.send_message(message.chat.id, "Пользователь забанен.")

        threading.Timer(1, lambda: bot.delete_message(message.chat.id, message.message_id)).start()
    else:
        bot.send_message(message.chat.id, "Ответьте на сообщение пользователя, чтобы забанить его.")

@bot.message_handler(func=lambda message: message.chat.id == YOUR_CHAT_ID, commands=['unban'])
def handle_unban(message):
    if message.from_user.id not in ADM_ID:
        return

    user_id = None
    
    if len(message.text.split()) > 1:
        user_id = int(message.text.split()[1])

    if user_id:
        bot.unban_chat_member(YOUR_CHAT_ID, user_id)
        msg = bot.send_message(message.chat.id, f"Пользователь разблокирован.")
        
        threading.Timer(1, lambda: bot.delete_message(message.chat.id, message.message_id)).start()
    else:
        bot.send_message(message.chat.id, "📛Укажите ID пользователя после команды /unban.📛")

        threading.Timer(8, lambda: bot.delete_message(message.chat.id, msg.message_id)).start()

def add_ban(user_id, admin_id, ban_timestamp):
    conn = sqlite3.connect('punishments.db')
    cursor = conn.cursor()

    try:
        cursor.execute('INSERT OR REPLACE INTO bans (user_id, admin_id, ban_timestamp) VALUES (?, ?, ?)', (user_id, admin_id, ban_timestamp))
        conn.commit()
    finally:
        conn.close()

def is_user_banned(user_id):
    cursor.execute('SELECT * FROM bans WHERE user_id = ?', (user_id,))
    row = cursor.fetchone()
    return row is not None

def get_user_id(message):
    return message.from_user.id if message.from_user else message.chat.id

def handle_auto_unpunish(user_id):
    punishment_data = get_punishment_data(user_id)

    if punishment_data and punishment_data.get("block") == 1:
        punishment_number = punishment_data.get("punishment_number")
        remove_punishment(user_id)
        user_info = bot.get_chat_member(YOUR_CHAT_ID, user_id).user
        mention = f"@{user_info.username}" if user_info.username else f"[Пользователь](tg://user?id={user_id})"
        message_text = f"🗽 Наказание с {mention} снято. UUID {punishment_number} 🗽"
        
        # Отправляем сообщение
        bot.send_message(YOUR_CHAT_ID, message_text)

def start_auto_unpunish_thread(user_id, punishment_time):
    timer = threading.Timer(punishment_time, handle_auto_unpunish, args=[user_id])
    timer.start()

def add_punishment(user_id, punishment_number, punishment_time, reason):
    conn = sqlite3.connect('punishments.db')
    cursor = conn.cursor()
    
    try:
        cursor.execute('''
            INSERT OR REPLACE INTO punishments (user_id, punishment_number, punishment_time, block, reason)
            VALUES (?, ?, ?, ?, ?)
        ''', (user_id, punishment_number, punishment_time, 1, reason))
        conn.commit()
    finally:
        conn.close()

def remove_punishment(user_id):
    conn = sqlite3.connect('punishments.db')
    cursor = conn.cursor()
    
    try:
        cursor.execute('UPDATE punishments SET block = 0 WHERE user_id = ?', (user_id,))
        conn.commit()
    finally:
        conn.close()

def is_user_punished(user_id):
    conn = sqlite3.connect('punishments.db')
    cursor = conn.cursor()
    
    try:
        cursor.execute('SELECT * FROM punishments WHERE user_id = ?', (user_id,))
        row = cursor.fetchone()
        return row is not None
    finally:
        conn.close()

def remaining_punishment_time(user_id):
    conn = sqlite3.connect('punishments.db')
    cursor = conn.cursor()
    
    try:
        cursor.execute('SELECT punishment_time FROM punishments WHERE user_id = ?', (user_id,))
        row = cursor.fetchone()
        if row:
            punishment_time = row[0]
            remaining_time = max(punishment_time - int(datetime.now().timestamp()), 0)
            return remaining_time
        return 0
    finally:
        conn.close()

def get_punishment_data(user_id):
    conn = sqlite3.connect('punishments.db')
    cursor = conn.cursor()
    
    try:
        cursor.execute('SELECT * FROM punishments WHERE user_id = ?', (user_id,))
        row = cursor.fetchone()
        if row:
            return {
                "user_id": row[0],
                "punishment_number": row[1],
                "punishment_time": row[2],
                "block": row[3],
                "reason": row[4]
            }
        return None
    finally:
        conn.close()

@bot.message_handler(func=lambda message: message.chat.id == YOUR_CHAT_ID, commands=['тп', 'Тп' , 'ТП', 'tp' , 'TP'])
def handle_tp(message):
    user_id = get_user_id(message)

    msg = bot.send_message(
        message.chat.id,
        """
<b>👤 Список ТП проекта</b>

☀️<a href="https://t.me/ParanoikMarvel">Параноик</a>☀️
<b>⌚️Время Работы: 12:00 - 00:00</b>

🌑<a href="https://t.me/DarknessMRVL">Darkness</a>🌑
<b>⌚️Время Работы:00:00 - 12:00</b>

<b>‼️Писать Только В Рабочее Время‼️</b>
        """,
        parse_mode="HTML",
        disable_web_page_preview=True,
    )

    threading.Timer(1, lambda: bot.delete_message(message.chat.id, message.message_id)).start()

    threading.Timer(20, lambda: bot.delete_message(message.chat.id, msg.message_id)).start()

@bot.message_handler(func=lambda message: message.chat.id == YOUR_CHAT_ID, commands=['куратор', 'Куратор'])
def handle_kyr(message):
    user_id = get_user_id(message)

    # Отправка сообщения с форматированием HTML и отключением предварительного просмотра веб-страницы
    msg = bot.send_message(
        message.chat.id,
        """
<b>❤️Ваш любимый Куратор - <a href="https://t.me/ConnorMarvel">CONNOR</a>💎\nОбращаться Если твой личный помощник не отвечает 15 Минут</b>
        """,
        parse_mode="HTML",
        disable_web_page_preview=True,
    )

    threading.Timer(1, lambda: bot.delete_message(message.chat.id, message.message_id)).start()

    threading.Timer(20, lambda: bot.delete_message(message.chat.id, msg.message_id)).start()

@bot.message_handler(func=lambda message: message.chat.id == YOUR_CHAT_ID, commands=['помощники', 'Помощники'])
def handle_helps(message):
    user_id = get_user_id(message)

    msg = bot.send_message(
        message.chat.id,
        """
<b>🔰Помощники:</b>

<b><a href="https://t.me/GefestMarvel">⚡️THOR⚡️</a> - 8:00 - 22:00 МСК⌚️ - Помощник Куратора</b>

<b><a href="https://t.me/SamuraiMarvel">🏮Samurai🏮</a> - 10:00 - 22:00 МСК⌚️ - Помощник Куратора</b>

<b><a href="https://t.me/laivuMRVL">💠Laivu💠</a> - 07:00 - 14:00 МСК⌚️ | 22:00 - 00:00 МСК⌚️ - Помощник Куратора</b>

        """,
        parse_mode="HTML",
        disable_web_page_preview=True,
    )

    threading.Timer(1, lambda: bot.delete_message(message.chat.id, message.message_id)).start()

    threading.Timer(20, lambda: bot.delete_message(message.chat.id, msg.message_id)).start()


@bot.message_handler(func=lambda message: message.chat.id == YOUR_CHAT_ID, commands=['мануал', 'Мануал'])
def handle_man(message):
    user_id = get_user_id(message)

    msg = bot.send_message(
        message.chat.id,
        """
<b>🎓Ты захотел найти ответ на свой Вопрос? Молодец🎓</b>
<b><a href="https://t.me/+XvVxqKuaeucxY2Nk">🎉Переходи в Мануал🎉</a></b>
        """,
        parse_mode="HTML",
        disable_web_page_preview=True,
    )

    threading.Timer(1, lambda: bot.delete_message(message.chat.id, message.message_id)).start()

    threading.Timer(20, lambda: bot.delete_message(message.chat.id, msg.message_id)).start()

@bot.message_handler(func=lambda message: message.chat.id == YOUR_CHAT_ID, commands=['help', 'Help'])
def handle_man(message):
    user_id = get_user_id(message)

    msg = bot.send_message(
        message.chat.id,
        """
<b>⚙️Команды чата⚙️</b>
<code>/тп</code><b> - Поддержка Marvel Team⚙️</b>
<code>/куратор</code><b> - Наш любимый куратор 👑</b>
<code>/помощники</code> - <b> - Помощники куратора📖</b>
<code>/мануал</code><b> - Наш мануал 📚</b>
<code>/правила</code><b> - Правила нашего чата 🛡</b>

<code>/займру</code><b> - Список сайтов для займа в России🇷🇺</b>
<code>/займкз</code><b> - Список сайтов для займа в Казахстане🇰🇿</b>
<code>/займукр</code><b> - Список сайтов для займа в Украине🇺🇦</b>

<code>/help</code><b> - Помощь по командам чата💭</b>

        """,
        parse_mode="HTML",
        disable_web_page_preview=True,
    )

    threading.Timer(1, lambda: bot.delete_message(message.chat.id, message.message_id)).start()

    threading.Timer(20, lambda: bot.delete_message(message.chat.id, msg.message_id)).start()


@bot.message_handler(func=lambda message: message.chat.id == YOUR_CHAT_ID, commands=['займру' , 'Займру' , 'займРу' , 'ЗаймРу'])
def handle_tp(message):
    user_id = get_user_id(message)

    msg = bot.send_message(
        message.chat.id,
        """
<b>💰Займы в 🇷🇺 💰</b>
<b><a href="https://ekapusta.com/">💵Е-Капуста💵</a></b>

<b><a href="https://web-zaim.ru/">💵Веб-Займ💵</a></b>

<b><a href="https://turbozaim.ru/">💵ТурбоЗайм💵</a></b>

<b><a href="https://moneyman.ru/">💵MoneyMan💵</a></b>

<b><a href="https://webbankir.com/">💵Веб-Банкир💵</a></b>

<b><a href="https://migcredit.ru/">💵МигКредит💵</a></b>
        """,
        parse_mode="HTML",
        disable_web_page_preview=True,
    )

    threading.Timer(1, lambda: bot.delete_message(message.chat.id, message.message_id)).start()
    threading.Timer(20, lambda: bot.delete_message(message.chat.id, msg.message_id)).start()

@bot.message_handler(func=lambda message: message.chat.id == YOUR_CHAT_ID, commands=['займукр' , 'Займукр' , 'займУкр' , 'ЗаймУкр'])
def handle_tp(message):
    user_id = get_user_id(message)

    msg = bot.send_message(
        message.chat.id,
        """
<b>💰Займы в 🇺🇦 💰</b>
<b><a href="https://e-groshi.com/">💵E-Groshi💵</a></b>

<b><a href="https://creditkasa.com.ua/ru/">💵CreditKasa💵</a></b>

<b><a href="https://sloncredit.ua/ru/">💵SlonCredit💵</a></b>

<b><a href="https://creditplus.ua/">💵CreditPlus💵</a></b>

<b><a href="https://kachay.com.ua/ru">💵Кача Гроши💵</a></b>

<b><a href="https://selfiecredit.com.ua/ru/">💵SelfieCredit💵</a></b>
        """,
        parse_mode="HTML",
        disable_web_page_preview=True,
    )

    threading.Timer(1, lambda: bot.delete_message(message.chat.id, message.message_id)).start()
    threading.Timer(20, lambda: bot.delete_message(message.chat.id, msg.message_id)).start()

@bot.message_handler(func=lambda message: message.chat.id == YOUR_CHAT_ID, commands=['займкз' , 'Займкз' , 'займКз' , 'ЗаймКз'])
def handle_tp(message):
    user_id = get_user_id(message)

    msg = bot.send_message(
        message.chat.id,
        """
<b>💰Займы в 🇰🇿 💰</b>
<b><a href="https://credit365.kz/">💵Credit365💵</a></b>

<b><a href="https://turbomoney.kz/">💵TurboMoney💵</a></b>

<b><a href="https://evazaym.kz/">💵EvaZaym💵</a></b>

<b><a href="https://timezaim.kz/">💵TimeZaym💵</a></b>

<b><a href="https://dengiclick.kz/">💵DengiClick💵</a></b>

<b><a href="https://gm24.kz/">💵GoMoney💵</a></b>
        """,
        parse_mode="HTML",
        disable_web_page_preview=True,
    )

    threading.Timer(1, lambda: bot.delete_message(message.chat.id, message.message_id)).start()
    threading.Timer(20, lambda: bot.delete_message(message.chat.id, msg.message_id)).start()

@bot.message_handler(func=lambda message: message.chat.id == YOUR_CHAT_ID, commands=['mute'])
def handle_punish(message):
    if message.from_user.id not in ADM_ID:
        return

    user_id = message.reply_to_message.from_user.id if message.reply_to_message and message.reply_to_message.from_user else None

    if user_id:
        args = message.text.split()[1:]
        if len(args) >= 2:
            time_string = args[0]
            reason = ' '.join(args[1:])

            try:
                punishment_time = int(time_string[:-1])
                unit = time_string[-1]

                if unit == 'd':
                    punishment_time *= 24 * 60 * 60
                elif unit == 'h':
                    punishment_time *= 60 * 60
                elif unit == 'm':
                    punishment_time *= 60
                else:
                    raise ValueError()

                next_punishment_number = get_next_punishment_number()

                add_punishment(user_id, next_punishment_number, punishment_time, reason)

                bot.restrict_chat_member(YOUR_CHAT_ID, user_id,
                    until_date=datetime.now().timestamp() + punishment_time,
                    can_send_messages=False,
                    can_send_media_messages=False,
                    can_add_web_page_previews=False,
                    can_send_other_messages=False,
                    can_invite_users=False,
                    can_pin_messages=False,
                    can_change_info=False
                )

                user_info = bot.get_chat_member(YOUR_CHAT_ID, user_id).user
                mention = f"@{user_info.username}" if user_info.username else f"[Пользователь](tg://user?id={user_id})"
                message_text = f"{mention}\n🛡Получил наказание на {time_string}\n\nПо причине: {reason} ❗\n\nUUID наказания: {next_punishment_number}📛"

                bot.send_message(message.chat.id, message_text)

                start_auto_unpunish_thread(user_id, punishment_time)
                
            except ValueError:
                bot.send_message(message.chat.id, "📛Некорректный формат времени. Используйте, например, '7d' для 7 дней.📛")
        else:
            bot.send_message(message.chat.id, "📛Необходимо указать время и причину наказания.📛")
    else:
        bot.send_message(message.chat.id, "📛Ответьте на сообщение пользователя, чтобы выдать наказание.📛")


def get_next_punishment_number():
    conn = sqlite3.connect('punishments.db')
    cursor = conn.cursor()

    try:
        cursor.execute('SELECT MAX(punishment_number) FROM punishments')
        max_punishment_number = cursor.fetchone()[0]
        return max_punishment_number + 1 if max_punishment_number else 1
    finally:
        conn.close()


@bot.message_handler(func=lambda message: message.chat.id == YOUR_CHAT_ID, commands=['unmute'])
def handle_unpunish(message):
    if message.from_user.id not in ADM_ID:
        return

    args = message.text.split()[1:]

    if len(args) == 1:
        try:
            punishment_number = int(args[0])
            punishment_data = get_punishment_by_number(punishment_number)

            if punishment_data:
                user_id = punishment_data["user_id"]
                remove_punishment(user_id)

                # Удаляем ограничения пользователя
                bot.restrict_chat_member(YOUR_CHAT_ID, user_id,
                    can_send_messages=True,
                    can_send_media_messages=True,
                    can_add_web_page_previews=True,
                    can_send_other_messages=True,
                    can_invite_users=True,
                    can_pin_messages=True,
                    can_change_info=True
                )

                user_info = bot.get_chat_member(YOUR_CHAT_ID, user_id).user
                mention = f"@{user_info.username}" if user_info.username else f"[Пользователь](tg://user?id={user_id})"
                message_text = f"🗽{mention}\n UUID {punishment_number} снято. 🗽"

                bot.send_message(message.chat.id, message_text)

            else:
                bot.send_message(message.chat.id, "📛Наказание с указанным номером не найдено.📛")
        except ValueError:
            bot.send_message(message.chat.id, "📛Некорректный номер наказания.📛")
    else:
        bot.send_message(message.chat.id, "📛Используйте команду в формате /unmute <номер наказания>.📛")

def get_punishment_by_number(punishment_number):
    conn = sqlite3.connect('punishments.db')
    cursor = conn.cursor()

    try:
        cursor.execute('SELECT * FROM punishments WHERE punishment_number = ?', (punishment_number,))
        row = cursor.fetchone()
        if row:
            return {
                "user_id": row[0],
                "punishment_number": row[1],
                "punishment_time": row[2],
                "block": row[3],
                "reason": row[4]
            }
        return None
    finally:
        conn.close()

while True:
    try:
        bot.polling(none_stop=True, timeout=120)
    except Exception as e:
        time.sleep(5)
        continue


import telebot
from telebot import types

TOKEN = ''

bot = telebot.TeleBot(TOKEN) # инициализируем нашего бота

usernames = {}

@bot.message_handler(commands=['start'])
def send_welcome(message):
    collect_user(message)
    bot.send_message(
    message.chat.id,
    '''Добро пожаловать на сервер шизофрения
    ''',
    reply_markup=inline_keyboard())

@bot.message_handler(content_types=['text'])
def get_user_id(message):
    collect_user(message)

@bot.message_handler(content_types=['new_chat_members'])
def ask_new_user(message):
    bot.reply_to(message, 'Привет! Купишь слона?')
    collect_user(message)

def collect_user(message):
    username = message.from_user.username
    id = message.from_user.id
    if (username not in usernames):
        usernames[username] = id


@bot.callback_query_handler(func=lambda message:True)
def ans(message):
    chat_id = message.message.chat.id
    if message.data == 'assign_admin':
        mesg = bot.send_message(chat_id, 'Кто же этот счастливчик? \nВведи username пользователя или его id:')
        bot.register_next_step_handler(mesg, assign_admin)
    if message.data == 'ban':
        mesg = bot.send_message(chat_id, 'Кто же этот счастливчик? \nВведи username пользователя или его id:')
        bot.register_next_step_handler(mesg, ban_user)
    if message.data == 'get statistics':
        get_statistics(chat_id)
    if message.data == 'leave':
        leave(chat_id)


def assign_admin(message):
    id = ''
    if not message.text.isdigit() and message.text in usernames:
        id = usernames[message.text]
    elif message.text.isdigit():
        id = message.text
    else:
        bot.send_message(message.chat.id, 'не получилось(')
        return

    try:
        if (bot.promote_chat_member(message.chat.id, id, can_change_info=True)):
            bot.send_message(message.chat.id, 'сделаль')
        else:
            bot.send_message(message.chat.id, 'не получилось(')
    except Exception:
        bot.send_message(message.chat.id, 'не получилось(')

def ban_user(message):
    id = ''
    if not message.text.isdigit() and message.text in usernames:
        id = usernames[message.text]
    elif message.text[0].isdigit():
        id = message.text
    else:
        bot.send_message(message.chat.id, 'не получилось(')
        return

    bot.unban_chat_member(message.chat.id, id, only_if_banned=True)

    try:
        bot.ban_chat_member(message.chat.id, id)
        bot.send_message(message.chat.id, 'сделаль')
    except Exception:
        bot.send_message(message.chat.id, 'не получилось(')

def get_statistics(chat_id):
    adm_amount = len(bot.get_chat_administrators(chat_id))
    mem_amount = bot.get_chat_member_count(chat_id)
    bot.send_message(chat_id, 'Админов : {0}\nВсего участников : {1}'.
                     format(adm_amount, mem_amount))

def leave(chat_id):
    bot.leave_chat(chat_id)

def inline_keyboard():
    keyboard = types.InlineKeyboardMarkup()
    keyboard.add(types.InlineKeyboardButton(text='Сделать админом', callback_data="assign_admin"))
    keyboard.add(types.InlineKeyboardButton(text='Бан', callback_data="ban"))
    keyboard.add(types.InlineKeyboardButton(text='Статистика', callback_data="get statistics"))
    keyboard.add(types.InlineKeyboardButton(text='Покинуть чат', callback_data="leave"))
    return keyboard

bot.polling(none_stop=True, interval=0)


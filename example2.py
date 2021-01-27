import telebot  # pip install pytelegrambotapi
from collections import defaultdict

# Бот для публикации объявлений
# @significante_bot
token = '1613285667:AAHYfDwP1KfrJQytNssbHVY74oguqBrp1oA'
bot = telebot.TeleBot(token)
START, TITLE, PRICE, CONFIRMATION = range(4)  # состояния
USER_STATE = defaultdict(lambda: START)
PRODUCTS = defaultdict(lambda: {})


@bot.message_handler(func=lambda message: get_state(message) == START)
def handle_message(message):
    bot.send_message(message.chat.id, text='Напиши название')
    update_state(message, TITLE)


@bot.message_handler(func=lambda message: get_state(message) == TITLE)
def handle_title(message):
    update_product(message.chat.id, 'title', message.text)  # message.chat.id == user_id
    bot.send_message(message.chat.id, text='Укажи цену')
    update_state(message, PRICE)


@bot.message_handler(func=lambda message: get_state(message) == PRICE)
def handle_price(message):
    update_product(message.chat.id, 'price', message.text)  # message.chat.id == user_id
    product = get_product(message.chat.id)
    bot.send_message(message.chat.id, text=f'Опубликовать объявление "{product}"?')
    update_state(message, CONFIRMATION)


@bot.message_handler(func=lambda message: get_state(message) == CONFIRMATION)
def handle_confirm(message):
    if 'yes' or 'да' in message.text.lower():
        bot.send_message(message.chat.id, text='Объявление опубликовано')
        # отправка объявления в другой чат кдругим пользователям
    update_state(message, START)


def get_state(message):
    return USER_STATE[message.chat.id]


def update_state(message, new_state):
    USER_STATE[message.chat.id] = new_state


def get_product(user_id):
    return PRODUCTS[user_id]


def update_product(user_id, key, value):
    PRODUCTS[user_id][key] = value


bot.polling()

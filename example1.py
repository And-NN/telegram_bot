import telebot  # pip install pytelegrambotapi
from telebot import types


# @significante_bot
token = '1613285667:AAHYfDwP1KfrJQytNssbHVY74oguqBrp1oA'
bot = telebot.TeleBot(token)
currencies = ['евро', 'доллар']


def check_currency(message):
    for c in currencies:
        try:
            if c in message.text.lower():
                return True
        except AttributeError:
            pass  # в сообщении не текст
            return False
    return False


def check_currency_value(text):
    currency_values = {'евро': 90, 'доллар': 70}
    for currency, value in currency_values.items():
        if currency in text.lower():
            return currency, value
    return None, None


@bot.message_handler(commands=['rate'])
@bot.message_handler(func=check_currency)
@bot.message_handler()
def message_handler(message):
    print(message.text)
    keyboard = create_keyboard()
    currency, value = check_currency_value(message.text)
    if currency:
        bot.send_message(chat_id=message.chat.id, text=f'Курс {currency} равен {value}', reply_markup=keyboard)
    else:
        bot.send_message(chat_id=message.chat.id, text='Узнай курс валют', reply_markup=keyboard)


def closest_bank(location):
    lon = location.longitude
    lat = location.latitude
    # имитация нахождения ближайшего объекта по полученным координатам
    bank_address = 'Красноармейская, 20'
    bank_lon, bank_lat = 55.800389, 37.543710
    return bank_address, bank_lon, bank_lat


@bot.message_handler(content_types='location')
def handle_location(message):
    print(message.location)
    bank_address, bank_lon, bank_lat = closest_bank(message.location)
    image = open('bank.jpg', 'rb')
    bot.send_photo(message.chat.id, image, caption='Сберегательная банка')
    bot.send_message(chat_id=message.chat.id, text=f'Ближайший банк: {bank_address}')
    bot.send_location(message.chat.id, bank_lon, bank_lat)


def create_keyboard():
    keyboard = types.InlineKeyboardMarkup (row_width=2)  # кнопки в чате
    # keyboard = types.ReplyKeyboardMarkup(row_width=2)  # кнопки под полем ввода
    buttons = [
        types.InlineKeyboardButton(text=c, callback_data=c) for c in currencies  # создаётся новая кнопка для каждой валюты
    ]
    keyboard.add(*buttons)
    return keyboard


@bot.callback_query_handler(func=lambda x: True)
def callback_handler(callback_query):
    message = callback_query.message
    text = callback_query.data
    currency, value = check_currency_value(text)
    if currency:
        bot.answer_callback_query(callback_query.id, text=f'КУРС: {currency} равен {value}')  # Всплывающее сообщение
        bot.send_message(chat_id=message.chat.id, text=f'Курс {currency} равен {value}')
    else:
        bot.send_message(chat_id=message.chat.id, text='Узнай курс валют')


bot.polling()

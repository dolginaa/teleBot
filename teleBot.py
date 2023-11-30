import time
import telebot
from telebot import types
import datetime
from datetime import datetime
from datetime import date
import re
import schedule
from datetime import timedelta

TOKEN = "6176505642:AAETb0Ih_ja-nIzmRxCQ4vhk3txGTGAsaLw"
bot = telebot.TeleBot(token=TOKEN)
file_path = "C:\dates.txt"
Any = '1531197456'


def is_valid_date(date_string):
    pattern = r'^\d{4}-\d{2}-\d{2}$'
    match = re.match(pattern, date_string)
    if match is not None:
        year = int(date_string[0:4])
        month = int(date_string[5:7])
        day = int(date_string[8:])
        if (month in range(1, 13)) and (day in range(1, 32)) and (year > 2000):
            return True
        else:
            return False


@bot.message_handler(commands=['start'])  # welcome message handler
def start(message):
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    btn1 = types.KeyboardButton("Привет")
    btn2 = types.KeyboardButton("Как дела?")
    btn3 = types.KeyboardButton("Добавить дату")
    markup.add(btn3)
    markup.add(btn1)
    markup.add(btn2)
    bot.send_message(message.from_user.id,
                     "Готов к работе, человек.", reply_markup=markup)


@bot.message_handler(content_types=['text'])
def get_text_messages(message):

    if message.text == 'Привет':
        bot.send_message(message.from_user.id, 'Привет, рыба.')  # ответ бота

    elif message.text == 'Как дела?':
        bot.send_message(message.from_user.id,
                         'хорошо, ведь сегодня 29.', parse_mode='Markdown')

    elif message.text == 'Добавить дату':
        bot.send_message(
            message.from_user.id, "Напишите дату в формате ГГГГ-ММ-ДД", parse_mode='Markdown')
        bot.register_next_step_handler(message, add_date)


def add_text(message):
    new_data = message.text
    with open(file_path, 'a') as file:
        file.write(str(new_data)+'\n')
    bot.send_message(message.from_user.id, 'Записал.', parse_mode='Markdown')


def add_date(message):
    new_date = message.text
    if is_valid_date(str(new_date)):
        with open(file_path, 'a') as file:
            file.write(str(new_date)+' ')
        bot.send_message(message.from_user.id, 'Записал.',
                         parse_mode='Markdown')
        bot.send_message(
            message.from_user.id, "Напишите описание введённой даты.", parse_mode='Markdown')
        bot.register_next_step_handler(message, add_text)
    else:
        bot.send_message(message.from_user.id,
                         "Некорректный формат даты.", parse_mode='Markdown')


def job():
    with open(file_path, 'r') as file:
        lines = file.readlines()
    for line in lines:
        plop = line[0:10]
        date_obj = datetime.strptime(plop, '%Y-%m-%d').date()
        today = date.today()
        if date_obj == today:
            bot.send_message(Any, "Сегодня "+line[11:])
        if date_obj == today+timedelta(days=1):
            bot.send_message(Any, "Завтра "+line[11:])
        if date_obj == today+timedelta(days=2):
            bot.send_message(Any, "Через 2 дня "+line[11:])


schedule.every().day.at('11:03').do(job)
while True:
    schedule.run_pending()
    time.sleep(1)


bot.polling(none_stop=True, interval=0)


def job():
    with open(file_path, 'r') as file:
        lines = file.readlines()
    for line in lines:
        plop = line[0:10]
        date_obj = datetime.strptime(plop, '%Y-%m-%d').date()
        if date_obj == datetime.date.today():
            bot.send_message(Any, "Сегодня "+line[11:])


schedule.every().day.at('10:07').do(job)
while True:
    schedule.run_pending()
    time.sleep(1)

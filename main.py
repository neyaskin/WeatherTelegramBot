import telebot
import open_weather_data

# API токен бота в Telegram
API_TOKEN = 'TOKEN'

bot = telebot.TeleBot(API_TOKEN)

# Добавление кнопок
RESERVER_WORDS = ['отмена', '/help', '/start']
keyboards_view_weather = telebot.types.ReplyKeyboardMarkup(True, True)
keyboards_view_weather.row('Погода')

# Обработка команд (Функция реагирует на команды)
@bot.message_handler(commands=['help', 'start'])
def welcome_message(message):
    bot.send_message(message.chat.id, 'Если хочешь посмотреть погоду напиши мне - Погода',
                     reply_markup=keyboards_view_weather)

# Обработка сообщений (Функция считывает все сообщения)
@bot.message_handler(func=lambda message: True)
def get_user_message(message):
    if message.text.lower() == "погода":
        bot.send_message(message.chat.id, 
                        "Напиши название пункта (Например: Томск) или Отмена")
        bot.register_next_step_handler(message, get_weather_one_day)

# Выводит пользователю подсказки
# Делает обращение к серверу для получение прогноза погоды
def get_weather_one_day(message):
    keyboard_city = telebot.types.ReplyKeyboardMarkup(True)

    if message.text.lower() not in RESERVER_WORDS:
        weather_data = open_weather_data.get_open_weather_one_day(message.text)

        if weather_data != 'Напишите название пункта':
            keyboard_city.row(message.text, 'Отмена')
            bot.send_message(message.chat.id, weather_data, reply_markup=keyboard_city)
            bot.register_next_step_handler(message, get_weather_one_day)
        else:
            bot.reply_to(message, 'Так не пойдет.. -_-')
            bot.send_message(message.chat.id, 
                            "Напиши название пункта (Например: Томск) или Отмена",
                            reply_markup=keyboard_city)
            bot.register_next_step_handler(message, get_weather_one_day)
    else:
        if  message.text.lower() == RESERVER_WORDS[0]:
            bot.send_message(message.chat.id, 
                            "Если что, пиши - Погода",
                            reply_markup=keyboards_view_weather)
        if  message.text == RESERVER_WORDS[1] or message.text == RESERVER_WORDS[2]:
            bot.send_message(message.chat.id,
                            'Если хочешь посмотреть погоду напиши мне - Погода',
                            reply_markup=keyboards_view_weather)
                        

bot.polling(none_stop=True, interval=0)

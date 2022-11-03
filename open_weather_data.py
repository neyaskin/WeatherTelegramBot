import json
import requests

# API ключ для получения прогноза погоды с сервера OpenWeatherMap
OPEN_WEATHER_API_KEY = 'aebf204b101c8b173750b669ce15b279';

# Получение данных с сервера
def get_open_weather_one_day(city_name):
    # Запрос серверу
    url = "http://api.openweathermap.org/data/2.5/""weather?" \
          "q={}&" \
          "appid={}&" \
          "units=metric&" \
          "lang=ru".format(city_name, OPEN_WEATHER_API_KEY)
    # Отправка запроса и получение данных с сервера
    weather_data = json.loads(requests.get(url).text)

    # Форматирование полученных данных
    if len(weather_data) == 2 and weather_data['cod'] == "404":
        return 'Напишите название пункта'
    else:
        return 'Город: {} - {}\n'\
               'Температура:\n'\
               '\t\t\t\tТекущая {}, ощущается как {}\n' \
               'Влажность: {}%\n' \
               'Скорость ветра: {}м/с'.format(weather_data['name'],
                                              weather_data['weather'][0]['description'],
                                              weather_data['main']['temp'],
                                              weather_data['main']['feels_like'],
                                              weather_data['main']['humidity'],
                                              weather_data['wind']['speed'])

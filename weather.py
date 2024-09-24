import requests
from config import API_KEY

BASE_URL = 'http://api.weatherapi.com/v1'


def get_weather(city):
    if type(city) is not str or len(city) == 0:
        return None
    
    api_method = '/forecast.json'    # get current weather
    res = requests.get(
        BASE_URL + api_method + '?key=' + API_KEY + '&q=' + city
    )

    if res.status_code == 404:
        return f'Weather data not available for {city}.'
    if res.status_code >= 400:
        return f'Weather data currently not available for {city}.'
    
    try:
        weather_data = res.json()

        current_data = weather_data['current']
        temp_f = current_data['temp_f']
        condition = current_data['condition']['text']

        forecast_data = weather_data['forecast']['forecastday'][0]['day']
        maxtemp_f = forecast_data['maxtemp_f']
        mintemp_f = forecast_data['mintemp_f']
        rain_chance = forecast_data['daily_chance_of_rain']
    except:
        return 'Error while trying to retrieve weather data.'

    return f'{city}: {condition}, {temp_f}°F, high {maxtemp_f}°F, low {mintemp_f}°F, {rain_chance}% chance of rain.'


if __name__ == '__main__':
    city = 'Charlottesville'
    print(get_weather(city))

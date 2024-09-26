import requests
from config import WEATHER_API_KEY

BASE_URL = 'http://api.weatherapi.com/v1'


def get_weather(city, temp_mode='fahrenheit'):
    if type(city) is not str or len(city) == 0:
        return None
    
    api_method = '/forecast.json'    # get current weather
    res = requests.get(
        BASE_URL + api_method + '?key=' + WEATHER_API_KEY + '&q=' + city
    )

    if res.status_code == 404:
        return f'Weather data not available for {city}.'
    if res.status_code >= 400:
        return f'Weather data currently not available for {city}.'
    
    try:
        weather_data = res.json()

        current_data = weather_data['current']
        if temp_mode == 'celsius':
            temp = current_data['temp_c']
        else:
            temp = current_data['temp_f']
        condition = current_data['condition']['text']

        forecast_data = weather_data['forecast']['forecastday'][0]['day']
        if temp_mode == 'celsius':
            maxtemp = forecast_data['maxtemp_c']
            mintemp = forecast_data['mintemp_c']
        else:
            maxtemp = forecast_data['maxtemp_f']
            mintemp = forecast_data['mintemp_f']
        rain_chance = forecast_data['daily_chance_of_rain']
    except:
        return 'Error while trying to retrieve weather data.'
    
    if temp_mode == 'celsius':
        unit = 'C'
    else:
        unit = 'F'

    return f'{city}: {condition}, {temp}°{unit}, high {maxtemp}°{unit}, low {mintemp}°{unit}, {rain_chance}% chance of rain.'


if __name__ == '__main__':
    # Test code
    city = 'Charlottesville'
    temp_mode = input('Type "celsius" or "fahrenheit": ')
    print(get_weather(city, temp_mode.lower()))

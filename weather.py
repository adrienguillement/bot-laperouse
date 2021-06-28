from datetime import datetime
import requests

LAT = 46.883670
LONG = -0.900050

TOKEN_WEATHER = os.getenv('WEATHER_TOKEN')

one_call_api_url = "https://api.openweathermap.org/data/2.5/onecall?lat=46.883670&lon=-0.900050&exclude=current,minutely,daily&units=metric&appid={}".format(TOKEN_WEATHER)
one_call_api_url = "https://api.openweathermap.org/data/2.5/onecall?lat=46.883670&lon=-0.900050&exclude=current,minutely,hourly,alerts&units=metric&appid={}".format(TOKEN_WEATHER)

def call_api():
    resp = requests.get(one_call_api_url)
    if resp.status_code != 200:
        # This means something went wrong.
        return False

    data = resp.json()['daily']
    return data


def get_temperature():
    daily = call_api()
    min = daily[1]['temp']['min']
    max = daily[1]['temp']['max']

    return "{} - {}".format(round(min), round(max))


def get_rain():
    daily = call_api()

    try:
        rain = daily[1]['rain']
        return True
    except:
        return False

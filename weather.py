from datetime import datetime
import requests

LAT = 46.883670
LONG = -0.900050

TOKEN_WEATHER = os.getenv('WEATHER_TOKEN')

one_call_api_url = "https://api.openweathermap.org/data/2.5/onecall?lat=46.883670&lon=-0.900050&exclude=current,minutely,daily&units=metric&appid={}".format(TOKEN_WEATHER)

def call_api():
    resp = requests.get(one_call_api_url)
    if resp.status_code != 200:
        # This means something went wrong.
        return False
    
    data = resp.json()['hourly']
    return data


def get_temperature():
    hourly = call_api()
    
    temps = {}

    for item in hourly:
        # Convert epoch to datetime and get only hour
        d = datetime.utcfromtimestamp(3600 * ((item['dt'] + 1800) // 3600))

        # Stop at midnight to only have current hour
        if(d.hour == 0):
            break
        
        temps[str(d.hour) + 'h'] = item['temp']

    return temps
    

def get_humidity():
    hourly = call_api()
    
    humidity = {}

    for item in hourly:
        # Convert epoch to datetime and get only hour
        d = datetime.utcfromtimestamp(3600 * ((item['dt'] + 1800) // 3600))

        # Stop at midnight to only have current hour
        if(d.hour == 0):
            break
        
        humidity[str(d.hour) + '%'] = item['humidity']

    return humidity

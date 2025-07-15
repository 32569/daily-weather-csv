import requests
import time
import csv
from datetime import datetime

API_KEY = '9d87b35ef81c86659aedec4d1b549965'  # <- Tavo OpenWeather API raktas
BASE_URL = 'https://api.openweathermap.org/data/2.5/weather'
CITY = 'Islamabad,PK'                          # <- Pasirink miestą/kodą pagal poreikį
UNITS = 'metric'                              # 'metric' (°C), 'imperial' (°F) arba palikti be šio parametro (K)

def fetch_weather():
    params = {
        'q': CITY,
        'appid': API_KEY,
        'units': UNITS
    }
    response = requests.get(BASE_URL, params=params)
    response.raise_for_status()
    return response.json()

def parse_data(data):
    # Konvertuojam UNIX timestamp į atskaitos datą
    dt = datetime.utcfromtimestamp(data['dt']).strftime('%Y-%m-%d %H:%M:%S')
    coord = data.get('coord', {})
    main = data.get('main', {})
    wind = data.get('wind', {})
    clouds = data.get('clouds', {})
    weather = data.get('weather', [{}])[0]
    rain = data.get('rain', {}).get('1h', 0)
    snow = data.get('snow', {}).get('1h', 0)

    return [
        dt,
        coord.get('lat', ''),
        coord.get('lon', ''),
        main.get('temp', ''),
        main.get('feels_like', ''),
        main.get('temp_min', ''),
        main.get('temp_max', ''),
        main.get('pressure', ''),
        main.get('humidity', ''),
        wind.get('speed', ''),
        wind.get('deg', ''),
        clouds.get('all', ''),
        weather.get('main', ''),
        weather.get('description', ''),
        rain,
        snow
    ]

def write_csv(row, filename='weather.csv'):
    header = [
        'datetime','lat','lon',
        'temp','feels_like','temp_min','temp_max',
        'pressure','humidity',
        'wind_speed','wind_deg',
        'clouds','weather_main','weather_desc',
        'rain_1h','snow_1h'
    ]
    # Patikrinam, ar failas jau egzistuoja
    try:
        with open(filename, 'r', encoding='utf-8'):
            file_exists = True
    except FileNotFoundError:
        file_exists = False

    # Atidarom CSV rašymui
    with open(filename, 'a', newline='', encoding='utf-8') as f:
        writer = csv.writer(f)
        if not file_exists:
            writer.writerow(header)
        writer.writerow(row)

if __name__ == '__main__':
    data = fetch_weather()
    row = parse_data(data)
    write_csv(row)

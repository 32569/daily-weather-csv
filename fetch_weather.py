import requests
import csv
from datetime import datetime

API_KEY = '9d87b35ef81c86659aedec4d1b549965'
BASE_URL = 'https://api.openweathermap.org/data/2.5/weather'

# K2 Base Camp koordinatės ir aukštis
LAT = 35.83455
LON = 76.50927
ELEVATION = 4965           # metrais
UNITS = 'metric'           # 'metric' (°C), 'imperial' (°F) arba palikti be šio parametro (K)

def fetch_weather():
    params = {
        'lat': LAT,
        'lon': LON,
        'appid': API_KEY,
        'units': UNITS
    }
    resp = requests.get(BASE_URL, params=params)
    resp.raise_for_status()
    return resp.json()

def parse_data(d):
    dt = datetime.utcfromtimestamp(d['dt']).strftime('%Y-%m-%d %H:%M:%S')
    coord = d.get('coord', {})
    main = d.get('main', {})
    wind = d.get('wind', {})
    clouds = d.get('clouds', {})
    weather = d.get('weather', [{}])[0]
    rain = d.get('rain', {}).get('1h', 0)
    snow = d.get('snow', {}).get('1h', 0)

    return [
        dt,
        coord.get('lat',''),
        coord.get('lon',''),
        main.get('temp',''),
        main.get('feels_like',''),
        main.get('temp_min',''),
        main.get('temp_max',''),
        main.get('pressure',''),
        main.get('humidity',''),
        wind.get('speed',''),
        wind.get('deg',''),
        clouds.get('all',''),
        weather.get('main',''),
        weather.get('description',''),
        rain,
        snow,
        ELEVATION            # pridedam konstantinį aukštį
    ]

def write_csv(row, filename='weather.csv'):
    header = [
        'datetime','lat','lon',
        'temp','feels_like','temp_min','temp_max',
        'pressure','humidity',
        'wind_speed','wind_deg',
        'clouds','weather_main','weather_desc',
        'rain_1h','snow_1h',
        'elevation_m'         # naujas stulpelis
    ]
    try:
        with open(filename,'r',encoding='utf-8'):
            exists = True
    except FileNotFoundError:
        exists = False

    with open(filename,'a',newline='',encoding='utf-8') as f:
        w = csv.writer(f)
        if not exists:
            w.writerow(header)
        w.writerow(row)

if __name__ == '__main__':
    data = fetch_weather()
    row = parse_data(data)
    write_csv(row)

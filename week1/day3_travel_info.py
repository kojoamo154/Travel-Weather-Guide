import os
from dotenv import load_dotenv
import requests

load_dotenv()
weather_api_key = os.getenv("OPENWEATHER_API_KEY")
country_api_key = os.getenv("RESTCOUNTRY_API_KEY")


def get_weather(city):
    url = f"https://api.openweathermap.org/data/2.5/weather?q={city}&appid={weather_api_key}&units=metric"
    response = requests.get(url)
    if response.status_code == 200:
        return response.json()
    return None

def get_country_info(country_code):
    url = f'https://api.restcountries.com/countries/v5?q={country_code}'
    headers = {'Authorisation': f'Bearer {weather_api_key}'}
    response = requests.get(url, headers=headers)
    if response.status_code == 200:
        return response.json()[0]
    return None

def run_tool(city):
    print("Travel Weather Tool")
    print(---------------------)
    city = input("Enter the name of city: ").strip

    if not city:
        print("No city entered. Exiting...")
        return

    print(f"/nFetching Weather Data of {city}")

    weather_data = get_weather(city)

    if not weather_data:
        print(f"Weather data for {city} not found. Check the spelling of your city")
        return

    country_code = weather_data["sys"]["country"]
    country_data = get_country_info(country_code)


import os
from dotenv import load_dotenv
import requests
import json

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
    url = f"https://api.restcountries.com/countries/v5/codes.alpha_2/{country_code}"
    headers = {"Authorization": f"Bearer {country_api_key}"}
    response = requests.get(url, headers=headers)
    if response.status_code == 200:
        try:
            data = response.json()
            if data:
                return data   # return the first dict in the list
        except ValueError:
            print("Response is not JSON:", response.text)
    else:
        print("Error:", response.status_code, response.text)
    return None

def save_to_file(data, filename):
    with open(filename, "w") as f:
        json.dump(data, f, indent=2)
    print(f"Data saved to {filename}")

def run_tool():
    print("\nTravel Weather Tool")
    print("---------------------")
    city = input("Enter the name of city: ").strip()

    if not city:
        print("No city entered. Exiting...")
        return

    print(f"\nFetching Weather Data of {city}")

    weather_data = get_weather(city)

    if not weather_data:
        print(f"Weather data for {city} not found. Check the spelling of your city")
        return

    country_code = weather_data["sys"]["country"]
    country_data = get_country_info(country_code)

    print(f"\n=== {city.title()}, {country_code} ===")
    print(f"Temperature : {weather_data['main']['temp']} C")
    print(f"Condition   : {weather_data['weather'][0]['description'].title()}")
    print(f"Humidity    : {weather_data['main']['humidity']}%")
    print(f"Wind        : {weather_data['wind']['speed']} m/s")

    if country_data:
        population = country_data.get("population", 0)
        region = country_data.get('subregion', "Unknown")
        
        # Extract currencies properly
        currencies_list = country_data.get('currencies', [])
        if currencies_list:
        # Get all currency names instead of just codes
            currencies = [c.get('code') for c in currencies_list]
        else:
            currencies = "Unknown"

        print(f"\n=== Country Info ===")
        print(f"Region      : {region}")
        print(f"Population  : {population:,}")
        print(f"Currency    : {currencies}")
    
    if weather_data:
        save_to_file(weather_data, f"{city.lower()}_weather.json")

run_tool()
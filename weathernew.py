import os
import requests

# API URL
BASE_URL = "https://api.openweathermap.org/data/2.5/weather"


def get_api_key() -> str:
    """Get API key from environment; fallback to previous hardcoded value."""
    fallback_api_key = "c3000a14e38c00fe86621d3b897766c6"   
    return os.getenv("OPENWEATHER_API_KEY", fallback_api_key).strip()


def get_weather(city: str) -> None:
    city = (city or "").strip()
    if not city:
        print("\nPlease enter a city name.")
        return

    api_key = get_api_key()
    if not api_key:
        print("\nMissing OpenWeatherMap API key.")
        print("Set environment variable OPENWEATHER_API_KEY to your key and try again.")
        return

    params = {
        "q": city,
        "appid": api_key,
        "units": "metric",
    }

    try:
        response = requests.get(BASE_URL, params=params, timeout=15)

        # OpenWeatherMap returns JSON even on errors.
        try:
            data = response.json()
        except ValueError:
            data = {}

        if response.status_code == 200:
            city_name = data.get("name", "")
            country = (data.get("sys") or {}).get("country", "")

            temperature = (data.get("main") or {}).get("temp")
            humidity = (data.get("main") or {}).get("humidity")

            weather_list = data.get("weather") or []
            weather_desc = weather_list[0].get("description", "") if weather_list else ""

            wind_speed = (data.get("wind") or {}).get("speed")

            print("\n===== WEATHER REPORT =====")
            print(f"City        : {city_name}, {country}")
            if temperature is not None:
                print(f"Temperature : {temperature}°C")
            if humidity is not None:
                print(f"Humidity    : {humidity}%")
            if weather_desc:
                print(f"Condition   : {weather_desc.title()}")
            if wind_speed is not None:
                print(f"Wind Speed  : {wind_speed} m/s")
        else:
            msg = (data.get("message") or "Request failed").strip() if isinstance(data, dict) else "Request failed"
            print(f"\nRequest failed ({response.status_code}): {msg}")

    except requests.exceptions.Timeout:
        print("\nRequest timed out. Please try again.")
    except requests.exceptions.RequestException as e:
        print("\nNetwork error:", e)


if __name__ == "__main__":
    print("====== WEATHER APP ======")
    city = input("Enter city name: ")
    get_weather(city)


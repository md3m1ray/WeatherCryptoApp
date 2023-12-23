import requests
import tkinter


def get_weather(api_key, city):
    base_url = "http://api.openweathermap.org/data/2.5/weather"
    params = {"q": city, "appid": api_key, "lang": "tr"}

    response = requests.get(base_url, params=params)
    data = response.json()

    if response.status_code == 200:
        temperature = round(data["main"]["temp"] - 273.15, 2)
        feel_temp = round(data["main"]["feels_like"] - 273.15, 2)
        description = str(data["weather"][0]["description"]).capitalize()

        print(f"Hava Durumu: {description}, Sıcaklık: {temperature}°C, Hissedilen Sıcaklık: {feel_temp}°C")
    else:
        print("Hava durumu bilgisi alınamadı.")


def get_crypto_price(crypto):
    base_url = "https://api.coingecko.com/api/v3/simple/price"
    params = {"ids": crypto, "vs_currencies": "try"}

    response = requests.get(base_url, params=params)
    data = response.json()

    if crypto in data:
        price = data[crypto]["try"]
        print("{} Fiyatı: {:,.2f} TL".format(crypto.capitalize(), price))
    else:
        print("Kripto para bilgisi alınamadı.")


openweathermap_api_key = "your_api"
get_weather(openweathermap_api_key, "Ankara,TR")
get_crypto_price("bitcoin")

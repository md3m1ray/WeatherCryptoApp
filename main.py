import requests
import tkinter as tk
from tkinter import ttk


def get_weather(api_key, city):
    base_url = "http://api.openweathermap.org/data/2.5/weather"
    params = {"q": city, "appid": api_key, "lang": "tr"}

    response = requests.get(base_url, params=params)
    data = response.json()

    if response.status_code == 200:
        temperature = round(data["main"]["temp"] - 273.15, 2)
        feel_temp = round(data["main"]["feels_like"] - 273.15, 2)
        description = str(data["weather"][0]["description"]).capitalize()

        result_label.config(
            text=f"Hava {description}\nSıcaklık: {temperature}°C, Hissedilen Sıcaklık: {feel_temp}°C")
    else:
        result_label.config(text="Hava durumu bilgisi alınamadı.")


def get_crypto_price(crypto):
    base_url = "https://api.coingecko.com/api/v3/simple/price"
    params = {"ids": crypto, "vs_currencies": "try"}

    response = requests.get(base_url, params=params)
    data = response.json()

    if crypto in data:
        price = data[crypto]["try"]
        result_label2.config(text="{} Fiyatı: {:,.2f} TL".format(crypto.capitalize(), price))
    else:
        result_label2.config(text="Kripto para bilgisi alınamadı.")


def button_click():
    city = city_combobox.get()
    crypto = crypto_combobox.get()

    get_weather(openweathermap_api_key, city)
    get_crypto_price(crypto)


def add_city():
    new_city = str(city_add_label.get()).capitalize()
    if new_city:
        if new_city not in cities:
            cities.append(new_city)
            city_combobox['values'] = cities
            city_add_label.delete(0, tk.END)
            result_label3.config(text=f"{new_city} Eklendi")
            save_cities_to_file()
        else:
            result_label3.config(text="Bu Şehir Zaten Listede")
    else:
        result_label3.config(text="Bir Şehir İsmi Giriniz")


def delete_city():
    city = str(city_add_label.get()).capitalize()
    if city:
        if city in cities:
            cities.remove(city)
            city_combobox['values'] = cities
            city_add_label.delete(0, tk.END)
            result_label3.config(text=f"{city} Silindi")
            save_cities_to_file()
        else:
            result_label3.config(text="Bu Şehir Listede Değil")
    else:
        result_label3.config(text="Bir Şehir İsmi Giriniz")


def add_crypto():
    crypto = str(crypto_add_label.get()).lower()
    if crypto:
        if crypto not in cryptos:
            cryptos.append(crypto)
            crypto_combobox['values'] = cryptos
            crypto_add_label.delete(0, tk.END)
            result_label3.config(text=f"{crypto} Eklendi")
            save_cryptos_to_file()
        else:
            result_label3.config(text="Bu Kripto Zaten Listede")
    else:
        result_label3.config(text="Bir Kripto İsmi Giriniz")


def delete_crypto():
    crypto = str(crypto_add_label.get()).lower()
    if crypto:
        if crypto in cryptos:
            cryptos.remove(crypto)
            crypto_combobox['values'] = cryptos
            crypto_add_label.delete(0, tk.END)
            result_label3.config(text=f"{crypto} Silindi")
            save_cryptos_to_file()
        else:
            result_label3.config(text="Bu Kripto Listede Değil")
    else:
        result_label3.config(text="Bir Kripto İsmi Giriniz")


def save_cities_to_file():
    with open("cities.txt", "w") as file:
        for city in cities:
            file.write(city + "\n")


def load_cities_from_file():
    try:
        with open("cities.txt", "r") as file:
            return [line.strip() for line in file.readlines()]
    except FileNotFoundError:
        return []


def save_cryptos_to_file():
    with open("cryptos.txt", "w") as file:
        for crypto in cryptos:
            file.write(crypto + "\n")


def load_cryptos_from_file():
    try:
        with open("cryptos.txt", "r") as file:
            return [line.strip() for line in file.readlines()]
    except FileNotFoundError:
        return []


def clear_default(event):
    event.widget.delete(0, 'end')
    event.widget.unbind('<FocusIn>')


# UI
root = tk.Tk()
root.title("Hava Durumu ve Kripto Fiyatları")

openweathermap_api_key = "yourapi"
cities = load_cities_from_file()
cryptos = load_cryptos_from_file()

# Şehir Giriş
city_label = tk.Label(root, text="Şehir:")
city_label.grid(row=0, column=0, padx=10, pady=10, sticky="e")

city_combobox = ttk.Combobox(root, values=cities)
city_combobox.grid(row=0, column=1, padx=10, pady=10)

# Kripto Para Seçimi
crypto_label = tk.Label(root, text="Kripto Para:")
crypto_label.grid(row=1, column=0, padx=10, pady=10, sticky="e")

crypto_combobox = ttk.Combobox(root, values=cryptos)
crypto_combobox.grid(row=1, column=1, padx=10, pady=10)

# Güncelleme Butonu
send_button = tk.Button(root, text="Bilgileri Getir / Güncelle", command=button_click)
send_button.grid(row=2, column=0, columnspan=2, pady=10)

# Sonuç
result_label = tk.Label(root, text="")
result_label.grid(row=3, column=0, columnspan=2, pady=10)

result_label2 = tk.Label(root, text="")
result_label2.grid(row=4, column=0, columnspan=2, pady=10)

# Şehir /  Ekleme / Silme
city_add_label = tk.Entry()
city_add_label.grid(row=5, column=0, columnspan=2, pady=15)

city_add_label.insert(0, 'Yeni Şehir')
city_add_label.bind('<FocusIn>', clear_default)

# Şehir Butonu
send_button = tk.Button(root, text="Listeye Şehir Ekle", command=add_city)
send_button.grid(row=6, column=0, pady=15, sticky="e")

send_button = tk.Button(root, text="Listeden Şehir Sil", command=delete_city)
send_button.grid(row=6, column=1, pady=15)

# Kripto /  Ekleme / Silme
crypto_add_label = tk.Entry()
crypto_add_label.grid(row=7, column=0, pady=15, columnspan=2)

crypto_add_label.insert(0, 'Yeni Kripto')
crypto_add_label.bind('<FocusIn>', clear_default)

# Kripto Butonu
send_button = tk.Button(root, text="Listeye Kripto Ekle", command=add_crypto)
send_button.grid(row=8, column=0, pady=15, sticky="e")

send_button = tk.Button(root, text="Listeden Kripto Sil", command=delete_crypto)
send_button.grid(row=8, column=1, pady=15)

result_label3 = tk.Label(root, text="")
result_label3.grid(row=9, column=0, columnspan=2, pady=5)

root.mainloop()

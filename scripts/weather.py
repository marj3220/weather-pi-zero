import time

import requests
from RPi import GPIO
from RPLCD.gpio import CharLCD

from config import api_key


class WeatherAPI():

    def __init__(self):
        self.complete_url = "https://api.openweathermap.org/data/2.5/onecall?lat=45.400&lon=-71.899&exclude=minutely,hourly&appid=" + api_key
        self.init_lcd()

    def init_lcd(self):
        self.lcd = CharLCD(pin_rs=15, pin_rw=18, pin_e=16, pins_data=[21, 22, 23, 24],
              numbering_mode=GPIO.BOARD,
              cols=20, rows=4, dotsize=8,
              charmap='A02',
              auto_linebreaks=True)

    def validate_weather(self):
        response = requests.get(self.complete_url)
        weather = response.json()
        #current = weather["current"]
        daily = weather["daily"][0]
        min_temp = "Min: " + self.K_to_C(daily["temp"]["min"]) + "°C\n"
        max_temp = "Max: " + self.K_to_C(daily["temp"]["max"]) + "°C\n"
        possibility_of_rain = "Rain: " + str(daily["pop"]*100)
        description = str(daily["weather"][0]["description"]).title() + "\n"
        full_lcd_message = description + min_temp + max_temp + possibility_of_rain
        print(full_lcd_message)
        self.lcd.clear()
        self.lcd.write_string(full_lcd_message)

    def K_to_C(self, temp_K):
        return str(int(temp_K - 273.15))

if __name__ == "__main__":
    weather_api = WeatherAPI()
    while True:
        weather_api.validate_weather()
        time.sleep(6) #nb_hours * seconds/hour

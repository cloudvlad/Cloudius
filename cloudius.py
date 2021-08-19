from PIL import ImageTk, Image
import requests
from tkinter import ttk
from tkinter.font import BOLD
import tkinter as tk
import time
import json
import os
import math
from io import BytesIO


# Beaufor scale (https://en.wikipedia.org/wiki/Beaufort_scale) (the unit is meter/second)
wind_scale = list()
wind_scale_section = dict()
def loadBeauforScale():
    # 0
    wind_scale_section = dict()
    wind_scale_section['min'] = 0.0
    wind_scale_section['max'] = 0.4
    wind_scale_section['description'] = "Calm"
    wind_scale.append(wind_scale_section)
    # 1
    wind_scale_section = dict()
    wind_scale_section['min'] = 0.5
    wind_scale_section['max'] = 1.5
    wind_scale_section['description'] = "Light air"
    wind_scale.append(wind_scale_section)
    # 2
    wind_scale_section = dict()
    wind_scale_section['min'] = 1.6
    wind_scale_section['max'] = 3.3
    wind_scale_section['description'] = "Light breeze"
    wind_scale.append(wind_scale_section)
    # 3
    wind_scale_section = dict()
    wind_scale_section['min'] = 3.4
    wind_scale_section['max'] = 5.4
    wind_scale_section['description'] = "Gentle breeze"
    wind_scale.append(wind_scale_section)
    # 4
    wind_scale_section = dict()
    wind_scale_section['min'] = 5.5
    wind_scale_section['max'] = 7.9
    wind_scale_section['description'] = "Moderate breeze"
    wind_scale.append(wind_scale_section)
    # 5
    wind_scale_section = dict()
    wind_scale_section['min'] = 8.0
    wind_scale_section['max'] = 10.7
    wind_scale_section['description'] = "Fresh breeze"
    wind_scale.append(wind_scale_section)
    # 6
    wind_scale_section = dict()
    wind_scale_section['min'] = 10.8
    wind_scale_section['max'] = 13.8
    wind_scale_section['description'] = "Strong breeze"
    wind_scale.append(wind_scale_section)
    # 7
    wind_scale_section = dict()
    wind_scale_section['min'] = 13.9
    wind_scale_section['max'] = 17.1
    wind_scale_section['description'] = "Moderate gale"
    wind_scale.append(wind_scale_section)
    # 8
    wind_scale_section = dict()
    wind_scale_section['min'] = 17.2
    wind_scale_section['max'] = 20.7
    wind_scale_section['description'] = "Fresh gale"
    wind_scale.append(wind_scale_section)
    # 9
    wind_scale_section = dict()
    wind_scale_section['min'] = 20.8
    wind_scale_section['max'] = 24.4
    wind_scale_section['description'] = "Strong gale"
    wind_scale.append(wind_scale_section)
    # 10
    wind_scale_section = dict()
    wind_scale_section['min'] = 24.5
    wind_scale_section['max'] = 28.4
    wind_scale_section['description'] = "Whole gale"
    wind_scale.append(wind_scale_section)
    # 11
    wind_scale_section = dict()
    wind_scale_section['min'] = 28.5
    wind_scale_section['max'] = 32.6
    wind_scale_section['description'] = "Violent storm"
    wind_scale.append(wind_scale_section)
    # 12 
    """
    wind_scale_section['min'] = 32.7
    wind_scale_section['max'] = 
    wind_scale_section['description'] = "Hurricane force"
    wind_scale.append(wind_scale_section)
    """
loadBeauforScale()

def calculateWindDirection(deg: int) -> int:
    index =  float(deg) / 45.0
    down = math.floor(index)
    up = math.ceil(index)
    print(down, index, up)
    if index - down <= up - index:
        return down
    else:
        return up

eight_wind_directions = dict()
eight_wind_directions[0]="N"
eight_wind_directions[1]="NE"
eight_wind_directions[2]="E"
eight_wind_directions[3]="SE"
eight_wind_directions[4]="S"
eight_wind_directions[5]="SW"
eight_wind_directions[6]="W"
eight_wind_directions[7]="NW"
eight_wind_directions[8]="N"

global weather
weather = dict()

# Constants
CELSIUS_SYMBOL = u'\N{DEGREE SIGN}' + "C"
ICONS_RESIZE = 90
BACKGROUND_COLOR = "#E5E5E5"

# Root window properties
root = tk.Tk()
root.title("Cloudius")
root.geometry("400x800")
root.resizable(False, False)
root.tk.call('wm', 'iconphoto', root._w, tk.PhotoImage(file='./icons/icon.ico'))
root.configure(background=BACKGROUND_COLOR)
root.grid_rowconfigure(0, weight=0)
root.grid_columnconfigure(0, weight=1)

wind_p_img = Image.open("./icons/wind_p.png").resize((ICONS_RESIZE - 50, ICONS_RESIZE - 50))
wind_x_img = Image.open("./icons/wind_x.png").resize((ICONS_RESIZE - 50, ICONS_RESIZE - 50))

not_found_img = ImageTk.PhotoImage(Image.open("./icons/not_found.png"))
sunrise_img = ImageTk.PhotoImage(Image.open("./icons/sunrise.png").resize((ICONS_RESIZE, ICONS_RESIZE)))
sunset_img = ImageTk.PhotoImage(Image.open("./icons/sunset.png").resize((ICONS_RESIZE, ICONS_RESIZE)))

# The common part of the URL for status icons
status_icons_url = "https://openweathermap.org/img/wn/"

# API request separated
url1 = "http://api.openweathermap.org/data/2.5/weather?q="
url2 = "&appid="


# Updating GUI
def update():
    weatherLookup()
    root.after(100000, update)

# Fetch data from the API from OpenWeather
def weatherLookup() -> None:
    location = str(lookupField.get())
    if len(location) == 0:
        icon.configure(image="")
        icon.image = ""
        description.config(text="")
        curr_temp.config(text="")
        feels_like.config(text="")
        sunrise_icon.configure(image="")
        sunrise_icon.image = ""
        sunset_icon.configure(image="")
        sunset_icon.image = ""
        sunrise_time.config(text="")
        sunset_time.config(text="")
        return

    try:
        api_request = requests.get(url1 + str(location) + url2 + os.getenv("OW_API_KEY"))
        results = json.loads(api_request.content)

        if results['cod'] == '404':
            icon.configure(image=not_found_img)
            icon.image = not_found_img
            description.config(text="")
            curr_temp.config(text="Location not found")
            curr_temp.config(font=("Arial", 20))
            feels_like.config(text="")
            sunrise_icon.config(image="")
            sunrise_icon.image = None
            sunset_icon.config(image="")
            sunset_icon.image = ""
            sunrise_time.config(text="")
            sunset_time.config(text="")
            wind_icon.configure(image="")
            wind_icon.image = ""
            return
        # Weather properties
        
        weather['id'] = results['weather'][0]['id']
        weather['description'] = str(results['weather'][0]['description']).capitalize()
        weather['status_icon'] = str(results['weather'][0]['icon'] + "@4x.png")
        weather['temp'] = str(int(float(results['main']['temp']) - 273.15))
        weather['feels_like'] = str(round(float(results['main']['feels_like']) - 273.15))
        weather['sunrise'] =  time.localtime(int(results['sys']['sunrise']))
        weather['sunset'] = time.localtime(int(results['sys']['sunset']))
        weather['wind_speed'] = float(results['wind']['speed'])
        weather['wind_description'] = ""
        weather['wind_deg'] = int(results['wind']['deg'])
        weather['wind_direction'] = ""

        

        status_icon_img = ImageTk.PhotoImage(Image.open(BytesIO((requests.get(status_icons_url + weather['status_icon'])).content)))
        icon.configure(image=status_icon_img)
        icon.image = status_icon_img
        curr_temp.config(text=str(weather['temp']) + CELSIUS_SYMBOL)
        curr_temp.config(font=("Arial", 30))
        feels_like.config(text="Feels like " + weather['feels_like'] + CELSIUS_SYMBOL)
        description.config(text=weather['description'])
        temp_time = str(weather['sunrise'].tm_hour) + ":"
        if int(weather['sunrise'].tm_hour) <= 9:
            temp_time = '0' + temp_time
        if int(weather['sunrise'].tm_min) <= 9:
            temp_time = temp_time + "0" + str(weather['sunrise'].tm_min)
        else:
            temp_time = temp_time + str(weather['sunrise'].tm_min)
        sunrise_time.config(text=temp_time)
        temp_time = str(weather['sunset'].tm_hour) + ":"
        if int(weather['sunset'].tm_hour) <= 9:
            temp_time = '0' + temp_time
        if int(weather['sunset'].tm_min) <= 9:
            temp_time = temp_time + "0" + str(weather['sunset'].tm_min)
        else:
            temp_time = temp_time + str(weather['sunset'].tm_min)
        sunset_time.config(text=temp_time)

        for section in wind_scale:
            if round(weather['wind_speed'], 1) >= section['min'] and round(weather['wind_speed'], 1) <= section['max']:
                weather['wind_description'] = section['description']
                break

        if weather['wind_description'] == "":
            weather['wind_description'] = "Hurricane force"


        sunrise_icon.configure(image=sunrise_img)
        sunrise_icon.image = sunrise_img
        sunset_icon.configure(image=sunset_img)
        sunset_icon.image = sunset_img
        
        temp_wind_direction = calculateWindDirection(weather['wind_deg'])
        weather['wind_direction'] = eight_wind_directions[temp_wind_direction]
        new_wind_direction = temp_wind_direction * 45
        if new_wind_direction % 90 == 0:
            img = ImageTk.PhotoImage(wind_p_img.rotate((temp_wind_direction + 1) * -45)) # -45 for clockwise rotation
            wind_icon.configure(image=img)
            wind_icon.image = img
        else:
            img = ImageTk.PhotoImage(wind_x_img.rotate((temp_wind_direction - 1) * -45)) # -45 for clockwise rotation
            wind_icon.configure(image=img)
            wind_icon.image = img      
        
        wind_speed.config(text=str(weather['wind_speed']) + "m/s " + weather['wind_direction'])

    except:
        icon.configure(image="")
        icon.image = ""
        description.config(text="Error...")
        curr_temp.config(text="")
        feels_like.config(text="")
        sunrise_icon.configure(image="")
        sunrise_icon.image = ""
        sunset_icon.configure(image="")
        sunset_icon.image = ""
        sunrise_time.config(text="")
        sunset_time.config(text="")
        wind_icon.configure(image="")
        wind_icon.image = ""



ttk.Style().configure("TEntry", padding=5, relief="flat", background="#ccc")

# Defining widgets
lookupField = ttk.Entry(root, width=40)
icon = ttk.Label(root, background=BACKGROUND_COLOR)
curr_temp = ttk.Label(root, font=("Arial", 30), background=BACKGROUND_COLOR)
feels_like = ttk.Label(root, background=BACKGROUND_COLOR)
description = ttk.Label(root, background=BACKGROUND_COLOR)
sunrise_icon = ttk.Label(root, background=BACKGROUND_COLOR)
sunset_icon = ttk.Label(root, background=BACKGROUND_COLOR)
sunrise_time = ttk.Label(root, font=("Arial", 12, BOLD), background=BACKGROUND_COLOR)
sunset_time = ttk.Label(root, font=("Arial", 12, BOLD), background=BACKGROUND_COLOR)
wind_icon = ttk.Label(root, background=BACKGROUND_COLOR)
wind_speed = ttk.Label(root, font=("Arial", 12, BOLD), background=BACKGROUND_COLOR)



# Positioning widgets
lookupField.grid(row=0, column=0, columnspan=3, pady=(10, 0))
icon.grid(row=1, column=0, columnspan=3)
curr_temp.grid(row=2, column=0, columnspan=3)
feels_like.grid(row=3, column=0, columnspan=3)
description.grid(row=4, column=0, columnspan=3)
sunrise_icon.grid(row=5, column=0, sticky="W", padx=(60, 0), pady=(30, 0))
sunset_icon.grid(row=5, column=2, sticky="S", padx=(0, 60), pady=(30, 0))
sunrise_time.place(x=85, y=455)
sunset_time.place(x=272, y=455)
wind_icon.grid(row=6, column=0, sticky="E", padx=(0, 0), pady=(100, 0))
wind_speed.grid(row=6, column=1, sticky="W",  padx=(0, 0), pady=(100, 0))

# Additional widget settings
lookupField.insert(0, "Rousse, BG")
lookupField.bind("<Return>", (lambda event: update()))
icon.grid_rowconfigure(1, weight=1)
icon.grid_columnconfigure(1, weight=1)

sunrise_icon.configure(image=None)
sunrise_icon.image = None
sunset_icon.configure(image=None)
sunset_icon.image = None


update()

root.mainloop()

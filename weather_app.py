import tkinter
from PIL import ImageTk, Image
import requests
from tkinter import ttk
from tkinter.font import BOLD
import tkinter as tk
import requests
import time
import json
import os
from io import BytesIO

# Global variables
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
    root.after(1000, update)

# Fetch data from the API from OpenWeather
def weatherLookup():
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
            return

        # Weather properties
        weather = dict()
        weather['id'] = results['weather'][0]['id']
        weather['description'] = str(results['weather'][0]['description']).capitalize()
        weather['status_icon'] = str(results['weather'][0]['icon'] + "@4x.png")
        weather['temp'] = str(int(float(results['main']['temp']) - 273.15))
        weather['feels_like'] = str(round(float(results['main']['feels_like']) - 273.15))
        weather['sunrise'] =  time.localtime(int(results['sys']['sunrise']))
        weather['sunset'] = time.localtime(int(results['sys']['sunset']))


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

        sunrise_icon.configure(image=sunrise_img)
        sunrise_icon.image = sunrise_img
        sunset_icon.configure(image=sunset_img)
        sunset_icon.image = sunset_img

        

    except:
        description.config(text="Error...")


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


# Positioning widgets
lookupField.grid(row=0, column=0, columnspan=3, pady=(10, 0))
icon.grid(row=1, column=0, columnspan=3)
curr_temp.grid(row=2, column=0, columnspan=3)
feels_like.grid(row=3, column=0, columnspan=3)
description.grid(row=4, column=0, columnspan=3)
sunrise_icon.grid(row=5, column=0, sticky="W", padx=(60, 0), pady=(30, 0))
sunset_icon.grid(row=5, column=2, sticky="S", padx=(0, 60), pady=(30, 0))
sunrise_time.place(x=85, y=455)#grid(row=5, column=0, rowspan=2, sticky="W", padx=(90, 0), pady=(30, 0))
sunset_time.place(x=272, y=455)#grid(row=6, column=2, rowspan=2, sticky="S", padx=(0, 60), pady=(30, 0))


# Additional widget settings
lookupField.insert(0, "Ruse, BG")
lookupField.bind("<Return>", (lambda event: update()))
icon.grid_rowconfigure(1, weight=1)
icon.grid_columnconfigure(1, weight=1)

sunrise_icon.configure(image=None)
sunrise_icon.image = None
sunset_icon.configure(image=None)
sunset_icon.image = None


update()

root.mainloop()

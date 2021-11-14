import tkinter, requests, time, json, os, math
from tkinter.constants import DISABLED, END
import tkinter as tk
from PIL import ImageTk, Image
from tkinter import Toplevel, ttk
from tkinter.font import BOLD
from io import BytesIO
from requests import api
import sys

from initial_data_load import *
from user_tweeks_methods import *

# Constants
CELSIUS_SYMBOL = u'\N{DEGREE SIGN}' + "C"
ICONS_RESIZE = 90
BACKGROUND_COLOR = "#E4D4C9" #Other colors: #FCDBC5 #90BBBD



settings_icon = Image.open("./icons/settings.png")
logo = Image.open("./icons/icon.png")

weather = dict()
ow_api_key = ""
welcome_msg = "This is Cloudius, \nyour weather app assistant! \n\nHe can help with some weather searching\n by city name but sometimes needs\n country, just to be sure there is no uncertainty."
instructions = "The only thing you have to do is to \nenter API key(s) from OpenWeather. \nAnd you are ready to go!"

load_beaufor_scale()
load_eight_wind_directions()

# Transforms wind angle direction in cardinal or ordinal direction (0deg = N(North))
def calculate_wind_direction(deg: int) -> int:
    index =  float(deg) / 45.0
    down = math.floor(index)
    up = math.ceil(index)
    if index - down <= up - index:
        return down
    else:
        return up

def check_api_key(api_key: str) -> bool:
    api_request = requests.get("http://api.openweathermap.org/data/2.5/weather?q=Sofia, BG&appid=" + api_key)
    results = json.loads(api_request.content)
    if results['cod'] == 200:
        return True
    return False

def add_api_key(api_key: str) -> None:
    global ow_api_key
    ow_api_key = api_key
    home_dir = os.path.expanduser("~")
    os.chdir(home_dir)

    if api_key == "":
        return
    if os.name != "nt":
        app_dir = ".cloudius"
        app_dir_path = os.path.join(home_dir, app_dir)
        if os.path.exists(app_dir) == False:
            os.makedirs(app_dir_path)
        
        os.chdir(app_dir_path)
        api_keys_filename = "api_keys"
        with open(api_keys_filename, "a") as f:
            f.write(api_key + "\n")

    # For Windows set file attribute.
    if os.name == "nt":
        app_dir = ".cloudius"
        app_dir_path = os.path.join(home_dir, app_dir)
        if os.path.exists(app_dir) == False:
            os.makedirs(app_dir_path)
            os.system("attrib +h app_dir_path")
        
        os.chdir(app_dir_path)
        api_keys_filename = "api_keys"
        with open(api_keys_filename, "a") as f:
            f.write(api_key + "\n")

    return api_key

def main():
    global ow_api_key
    ow_api_key = get_api_key()
    pref_location = get_pref_location().strip("\n")

    # Root window properties
    root = tk.Tk(className="Cloudius")
    root.bind('<Control-z>', quit)
    root.title("Cloudius")
    root.geometry("400x800")
    root.resizable(False, False)
    icon = ImageTk.PhotoImage(logo)
    root.iconphoto(False, icon)
    root.configure(background=BACKGROUND_COLOR)
    root.grid_rowconfigure(0, weight=0)
    root.grid_columnconfigure(0, weight=1)
    
    wind_p_img = Image.open("./icons/wind_p.png").resize((ICONS_RESIZE - 60, ICONS_RESIZE - 60))
    wind_x_img = Image.open("./icons/wind_x.png").resize((ICONS_RESIZE - 60, ICONS_RESIZE - 60))

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
            
            logo_img = ImageTk.PhotoImage(logo)
            icon.configure(image=logo_img)
            icon.image = logo_img

            description.config(font=("Arial", 14, "italic"))
            description.config(text=welcome_msg)
            curr_temp.config(text="Greetings!")
            feels_like.config(text="")
            sunrise_icon.configure(image="")
            sunrise_icon.image = ""
            sunset_icon.configure(image="")
            sunset_icon.image = ""
            sunrise_time.config(text="")
            sunset_time.config(text="")
            wind_icon.configure(image="")
            wind_icon.image = ""
            wind_speed.config(text="")
            wind_description.config(text=instructions)
            return

        try:
            api_request = requests.get(url1 + str(location) + url2 + ow_api_key)
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
                wind_icon.config(image="")
                wind_icon.image = ""
                wind_speed.config(text="")
                wind_description.config(text="")
                return
            description.config(font=("Arial", 11, "normal"))

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
            
            wind_description.config(text=weather['wind_description'])

            sunrise_icon.configure(image=sunrise_img)
            sunrise_icon.image = sunrise_img
            sunset_icon.configure(image=sunset_img)
            sunset_icon.image = sunset_img
            
            temp_wind_direction = calculate_wind_direction(weather['wind_deg'])
            weather['wind_direction'] = eight_wind_directions[temp_wind_direction]
            new_wind_direction = temp_wind_direction * 45
            if new_wind_direction % 90 == 0:
                img = ImageTk.PhotoImage(wind_p_img.rotate((temp_wind_direction - 2) * -45)) # -45 for clockwise rotation
                wind_icon.configure(image=img)
                wind_icon.image = img
            else:
                img = ImageTk.PhotoImage(wind_x_img.rotate((temp_wind_direction - 1) * -45)) # -45 for clockwise rotation
                wind_icon.configure(image=img)
                wind_icon.image = img      
            wind_speed.config(text=str(weather['wind_speed']) + "m/s " + weather['wind_direction'])

        except:
            icon.configure(image=not_found_img)
            icon.image = not_found_img
            description.config(text="")
            curr_temp.config(text="Connection error!", font=("Arial", 20))
            feels_like.config(text="")
            sunrise_icon.configure(image="")
            sunrise_icon.image = ""
            sunset_icon.configure(image="")
            sunset_icon.image = ""
            sunrise_time.config(text="")
            sunset_time.config(text="")
            wind_icon.configure(image="")
            wind_icon.image = ""
            wind_description.config(text="")

    ttk.Style().configure("TEntry", padding=5, relief="flat", background="#ccc")

    # Defining widgets
    lookupField = ttk.Entry(root, width=40)
    icon = ttk.Label(root, background=BACKGROUND_COLOR)
    curr_temp = ttk.Label(root, font=("Arial", 30), background=BACKGROUND_COLOR)
    feels_like = ttk.Label(root, background=BACKGROUND_COLOR)
    description = ttk.Label(root, background=BACKGROUND_COLOR, justify="center", font=("Arial", 11, "italic"))
    sunrise_icon = ttk.Label(root, background=BACKGROUND_COLOR)
    sunset_icon = ttk.Label(root, background=BACKGROUND_COLOR)
    sunrise_time = ttk.Label(root, font=("Arial", 12, BOLD), background=BACKGROUND_COLOR)
    sunset_time = ttk.Label(root, font=("Arial", 12, BOLD), background=BACKGROUND_COLOR)
    wind_icon = ttk.Label(root, background=BACKGROUND_COLOR)
    wind_speed = ttk.Label(root, font=("Arial", 12, BOLD), background=BACKGROUND_COLOR)
    wind_description = ttk.Label(root, font=("Arial", 12, "italic"), justify="center", background=BACKGROUND_COLOR)
    user_api_keys = tk.Button(root, text="Manage API keys", borderwidth=0, background="#8e8e8e", padx=0, pady=0, command=(lambda: manage_api_keys(root)))
    user_pref_location = tk.Button(root, text="Favorite location \u2665", borderwidth=0, background="#8e8e8e", padx=0, pady=0, command=lambda: add_pref_location(lookupField.get()))

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
    wind_icon.grid(row=6, column=0, sticky="E", padx=(50, 10), pady=(100, 0))
    wind_speed.grid(row=6, column=1, sticky="W", padx=(0, 0), pady=(100, 0))
    wind_description.grid(row=7, column=0, columnspan=3, ipadx=(5), pady=(10, 0))
    user_api_keys.place(x=0-1, y=770+1, width=133, height=30)
    user_pref_location.place(x=133-1, y=770+1, width=133, height=30)

    # Additional widget settings
    lookupField.insert(0, pref_location)
    lookupField.bind("<Return>", (lambda event: update()))
    icon.grid_rowconfigure(1, weight=1)
    icon.grid_columnconfigure(1, weight=1)

    sunrise_icon.configure(image=None)
    sunrise_icon.image = None
    sunset_icon.configure(image=None)
    sunset_icon.image = None

    update()
    root.mainloop()

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print('Interrupted')
        
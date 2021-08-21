import tkinter, requests, time, json, os, math
from typing import Collection
from tkinter.constants import DISABLED, END
import tkinter as tk
from PIL import ImageTk, Image
from tkinter import Toplevel, ttk
from tkinter.font import BOLD
from io import BytesIO
from requests import api

# Constants
CELSIUS_SYMBOL = u'\N{DEGREE SIGN}' + "C"
ICONS_RESIZE = 90
BACKGROUND_COLOR = "#E4D4C9" #Other colors: #FCDBC5 #90BBBD

settings_icon = Image.open("./icons/settings.ico")
logo = Image.open("./icons/icon.ico")

weather = dict()
wind_scale = list()
eight_wind_directions = dict()
ow_api_key = ""
welcome_msg = "This is Cloudius, \nyour weather app friend! \n\nHe can help with your wishes searching\n by city name but sometimes needs\n country, because as people sometimes we \nare not very creative."


# Beaufor (wind) scale (https://en.wikipedia.org/wiki/Beaufort_scale) (the unit is meter/second)
def load_beaufor_scale() -> None:
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
load_beaufor_scale()

# Cardinal(4) and ordinal(4) directions
def load_eight_wind_directions() -> None:
    eight_wind_directions[0]="N"
    eight_wind_directions[1]="NE"
    eight_wind_directions[2]="E"
    eight_wind_directions[3]="SE"
    eight_wind_directions[4]="S"
    eight_wind_directions[5]="SW"
    eight_wind_directions[6]="W"
    eight_wind_directions[7]="NW"
    eight_wind_directions[8]="N"
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

def add_api_key(api_key: str):
    global ow_api_key
    ow_api_key = api_key
    home_dir = os.path.expanduser("~")
    os.chdir(home_dir)

    if not check_api_key(api_key):
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
        

    # For windows set file attribute.
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

class ShowKeys:
    def __init__(self, root):
        keys = (open(os.path.join(os.path.expanduser("~"), ".cloudius", "api_keys"), "r")).readlines()
        for i in range(0, len(keys)):
            self.e = ttk.Entry(root, width=36, font=("Arial", 12, BOLD), justify="center")
            self.e.grid(row=i, column=0)
            self.e.insert(END, keys[i].strip("\n"))

def show_keys(root: tkinter.Tk):
    table = tk.Toplevel(root)
    scrollbar = ttk.Scrollbar(table)
    table.geometry("330x300")
    ShowKeys(table)

def manage_api_keys(root: tkinter.Tk) -> None:
    form = tk.Toplevel(root)
    form.title("API Keys Menagement")
    icon = ImageTk.PhotoImage(settings_icon)
    form.wm_iconphoto(False, icon)
    form.geometry("400x200")

    input_label = ttk.Label(form, text="Insert your API key from OpenWeather")
    input_field = ttk.Entry(form, width=36)
    add_btn = ttk.Button(form, text="Add key", command=(lambda: add_api_key(input_field.get())))
    delete_btn = ttk.Button(form, text="Delete key", command=(lambda: delete_api_key(input_field.get())))
    show_btn = ttk.Button(form, text="Show keys", command=(lambda: show_keys(root)))

    input_label.pack(pady=(20, 0))
    input_field.pack(pady=(10, 0))
    add_btn.pack(pady=(10, 0))
    delete_btn.pack(pady=(10, 0))
    show_btn.pack(pady=(10, 0))

def delete_api_key(api_key: str):
    api_keys_file = os.path.join(os.path.expanduser("~"), ".cloudius", "api_keys")
    
    old_keys = open(api_keys_file, "r")
    lines = old_keys.readlines()
    old_keys.close()

    new_keys = open(api_keys_file, "w")
    for line in lines:
        if line.strip("\n") != api_key:
            new_keys.write(line)

    new_keys.close()

def get_api_key() -> str:
    keys = (open(os.path.join(os.path.expanduser("~"), ".cloudius", "api_keys"), "r")).readlines()
    ow_api_key = ""
    for key in keys:
        if check_api_key(key.strip("\n")):
            ow_api_key = key.strip("\n")
            break
    return ow_api_key

def add_pref_location(location: str) -> None:
    home_dir = os.path.expanduser("~")
    os.chdir(home_dir)
        
    app_dir = ".cloudius"
    app_dir_path = os.path.join(home_dir, app_dir)
    if os.path.exists(app_dir) == False:
        os.makedirs(app_dir)
    
    os.chdir(app_dir_path)
    filename = "pref_location"
    with open(filename, "w") as f:
        f.write(location + "\n")

def get_pref_location():
    path = os.path.join(os.path.expanduser("~"), ".cloudius", "pref_location")
    if os.path.exists(path) == False:
        print("nope")
        return

    file = open(path, "r")
    location = file.readline().strip("\n")
    file.close()
    return location


def main():
    global ow_api_key
    ow_api_key = get_api_key()
    pref_location = get_pref_location()

    # Root window properties
    root = tk.Tk()
    root.title("Cloudius")
    root.geometry("400x800")
    root.resizable(False, False)
    icon = ImageTk.PhotoImage(logo)
    root.wm_iconphoto(False, icon)
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
            wind_description.config(text="")
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
    main()
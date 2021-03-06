<p align="center">
  <img src="./icons/icon.png" alt="Cloudius logo">
</p>

# Cloudius - your simple weather assistant
### Cloudius is GUI weather software that uses OpenWeather data by connecting trought personal API.

<p align="center"><img src="https://i.imgur.com/RWwb4aN.png" width="100%" alt="-line-separator-"></p>

## Table of Contents
*  [:page_with_curl: General Information](#page_with_curl-general-information)
*  [:camera_flash: Screenshots](#camera_flash-screenshots)
*  [:gear: Setup](#gear-setup)
*  [:wrench: Usage](#wrench-usage)
*  [:old_key: Features](#old_key-features)
*  [:telescope: Technologies Used](#telescope-technologies-used)
*  [:arrow_forward: Executable](#arrow_forward-executable)

<p align="center"><img src="https://i.imgur.com/RWwb4aN.png" width="100%" alt="-line-separator-"></p>

## :page_with_curl: General Information
Cloudius has simple user interface and the most important information that people need. The only thing that the user has to do is to make account in OpenWeather and insert their API key(s).

<p align="center"><img src="https://i.imgur.com/RWwb4aN.png" width="100%" alt="-line-separator-"></p>

## :camera_flash: Screenshots
<p align="center">
  <img alt="App greetings screen" width="40%" src="https://i.imgur.com/98h3uaG.png">
  <img alt="Usage example 1" width="40%" src="https://i.imgur.com/HfnD8zc.png">
  <img alt="Usage example 2" width="80%" src="https://i.imgur.com/ocuarsq.png">
</p>

<p align="center"><img src="https://i.imgur.com/RWwb4aN.png" width="100%" alt="-line-separator-"></p>

## :gear: Setup
- Clone the project repository
- Run <kbd>pip install -r requirements.txt</kbd> (Python 2), or <kbd>pip3 install -r requirements.txt</kbd> (Python 3)

<p align="center"><img src="https://i.imgur.com/RWwb4aN.png" width="100%" alt="-line-separator-"></p>

## :wrench: Usage
#### **Executable file:** Go to the directory, where executable is placed, and run <kbd>./cloudius</kbd>.(Check "Executable" section)
#### **All project files:** Go to the project directory and run<kbd>./python3 ./cloudius.py</kbd>

<p align="center"><img src="https://i.imgur.com/RWwb4aN.png" width="100%" alt="-line-separator-"></p>

## :old_key: Features
- Dispplay weather information
- API keys management
- Favorite location

<p align="center"><img src="https://i.imgur.com/RWwb4aN.png" width="100%" alt="-line-separator-"></p>

## :telescope: Technologies Used
- [Tkinter](https://docs.python.org/3/library/tkinter.html)
- [Python3](https://www.python.org/)
- [OpenWeather API](https://openweathermap.org/)

<p align="center"><img src="https://i.imgur.com/RWwb4aN.png" width="100%" alt="-line-separator-"></p>

## :arrow_forward: Executable
- Go to the project directory
- Run <kbd>pip install pyinstaller</kbd>, and then <kbd>pyinstaller --onefile --hidden-import='PIL._tkinter_finder' ./cloudius.py</kbd>
- The executable should be in "dist" folder


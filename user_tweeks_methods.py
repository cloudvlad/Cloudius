from cloudius import tk, tkinter, ImageTk, END, BOLD, os, ttk, check_api_key, add_api_key, Image

settings_icon = Image.open("./icons/settings.png")
class ShowKeys:
    def __init__(self, root):
        if os.path.exists(os.path.join(os.path.expanduser("~"), ".cloudius", "api_keys")) == False:
            return
        keys = (open(os.path.join(os.path.expanduser("~"), ".cloudius", "api_keys"), "r")).readlines()
        for i in range(0, len(keys)):
            self.e = ttk.Entry(root, width=36, font=("Arial", 12, BOLD), justify="center")
            self.e.grid(row=i, column=0)
            self.e.insert(END, keys[i].strip("\n"))

def show_keys(root: tkinter.Tk):
    table = tk.Toplevel(root)
    table.title("API Keys")
    icon = ImageTk.PhotoImage(settings_icon)
    table.iconphoto(False, icon)
    table.resizable(False, False)
    scrollbar = ttk.Scrollbar(table)
    table.geometry("330x300")
    ShowKeys(table)

def manage_api_keys(root: tkinter.Tk) -> None:
    form = tk.Toplevel(root)
    form.title("API Keys Management")
    icon = ImageTk.PhotoImage(settings_icon)
    form.resizable(False, False)
    form.iconphoto(False, icon)
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

def delete_api_key(api_key: str) -> None:
    api_keys_file = os.path.join(os.path.expanduser("~"), ".cloudius", "api_keys")
    
    if os.path.exists(api_keys_file) == False:
        return
    old_keys = open(api_keys_file, "r")
    lines = old_keys.readlines()
    old_keys.close()

    new_keys = open(api_keys_file, "w")
    for line in lines:
        if line.strip("\n") != api_key:
            new_keys.write(line)

    new_keys.close()

def get_api_key() -> str:
    program_dir = os.getcwd()
    home = os.path.expanduser("~")
    if os.path.exists(os.path.join(home, ".cloudius", "api_keys")) == False:
        return ""
    file = open(os.path.join(home, ".cloudius", "api_keys"), "r")
    keys = file.readlines()
    file.close()
    ow_api_key = ""
    for key in keys:
        if check_api_key(key.strip("\n")):
            ow_api_key = key.strip("\n")
            break

    os.chdir(program_dir)
    return ow_api_key

def add_pref_location(location: str) -> None:
    program_dir = os.getcwd()
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
    os.chdir(program_dir)

def get_pref_location() -> str:
    program_dir = os.getcwd()
    home = os.path.expanduser("~")
    if os.path.exists(os.path.join(home, ".cloudius", "pref_location")) == False:
        return ""
    file = open(os.path.join(home, ".cloudius", "pref_location"), "r")
    location = file.readline()
    file.close()
    os.chdir(program_dir)
    return location
    
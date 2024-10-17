import json
from tkinter import Tk, Canvas, Button
from PIL import ImageDraw, ImageFont

# Initialize the Tkinter window
root = Tk()
root.title("Settings Screen UI")
root.geometry("500x700")

# Create canvas for the settings screen
canvas = Canvas(root, width=480, height=640, bg="white")
canvas.pack()

# Load fonts (adjust font sizes for clarity)
try:
    font_large = ImageFont.truetype("arial.ttf", 30)
    font_medium = ImageFont.truetype("arial.ttf", 20)
except IOError:
    font_large = ImageFont.load_default()
    font_medium = ImageFont.load_default()

# Available languages with full names
languages = ['English', 'Spanish', 'French', 'German']  # Add more languages as needed
selected_language_index = 0  # Default language is the first one (English)

# Translations dictionary
translations = {
    'English': {
        'settings': "Settings",
        'brightness': "Brightness",
        'volume': "Volume",
        'main_menu': "Main Menu",
        'confirm': "Confirm",
        'up': "Up",
        'down': "Down",
        'left': "Left",
        'right': "Right",
        'restore_defaults': "Restore Defaults",
        'select_language': "Select Language"
    },
    'Spanish': {
        'settings': "Ajustes",
        'brightness': "Brillo",
        'volume': "Volumen",
        'main_menu': "Menú Principal",
        'confirm': "Confirmar",
        'up': "Arriba",
        'down': "Abajo",
        'left': "Izquierda",
        'right': "Derecha",
        'restore_defaults': "Restaurar Valores",
        'select_language': "Seleccionar Idioma"
    },
    'French': {
        'settings': "Paramètres",
        'brightness': "Luminosité",
        'volume': "Volume",
        'main_menu': "Menu Principal",
        'confirm': "Confirmer",
        'up': "Haut",
        'down': "Bas",
        'left': "Gauche",
        'right': "Droite",
        'restore_defaults': "Restaurer les valeurs",
        'select_language': "Choisir la langue"
    },
    'German': {
        'settings': "Einstellungen",
        'brightness': "Helligkeit",
        'volume': "Lautstärke",
        'main_menu': "Hauptmenü",
        'confirm': "Bestätigen",
        'up': "Oben",
        'down': "Unten",
        'left': "Links",
        'right': "Rechts",
        'restore_defaults': "Werkseinstellungen",
        'select_language': "Sprache auswählen"
    },
}

# Load settings from a file if it exists
def load_settings():
    global brightness_level, volume_level, selected_language_index
    try:
        with open('settings.json', 'r') as f:
            settings = json.load(f)
            brightness_level = settings.get('brightness', 100)
            volume_level = settings.get('volume', 50)
            selected_language_index = settings.get('language_index', 0)
    except FileNotFoundError:
        brightness_level = 100
        volume_level = 50
        selected_language_index = 0

# Save settings to a file
def save_settings():
    settings = {
        'brightness': brightness_level,
        'volume': volume_level,
        'language_index': selected_language_index
    }
    with open('settings.json', 'w') as f:
        json.dump(settings, f)

# Variables to track brightness and volume levels
selected_option = 0  # Tracks if 'Volume', 'Brightness' or 'Language' is selected
adjust_mode = False  # Tracks if we are in adjust mode for brightness or volume
language_mode = False  # Tracks if we are selecting a language

# Options for selection (brightness, volume, language selection)
options = ["Brightness", "Volume", "Select Language"]

# Function to change the language based on selection
def change_language(new_index):
    global selected_language_index
    selected_language_index = new_index
    update_button_labels()  # Update button labels for new language
    draw_settings_ui()

# Function to update button labels based on selected language
def update_button_labels():
    current_language = languages[selected_language_index]
    translation = translations[current_language]

    # Update button labels for navigation
    up_button.config(text=translation['up'])
    down_button.config(text=translation['down'])
    left_button.config(text=translation['left'])
    right_button.config(text=translation['right'])
    confirm_button.config(text=translation['confirm'])
    back_button.config(text=translation['main_menu'])
    restore_defaults_button.config(text=translation['restore_defaults'])

# Function to map brightness to a grayscale background color
def get_brightness_color(brightness_level):
    brightness_color = int((brightness_level / 100) * 255)
    return f'#{brightness_color:02x}{brightness_color:02x}{brightness_color:02x}'

# Function to simulate volume adjustment and display in CMD
def simulate_volume_change(volume_level):
    print(f"Volume adjusted to: {volume_level}%")

# Function to adjust brightness or volume
def adjust_brightness_or_volume(change):
    global brightness_level, volume_level
    if selected_option == 0:  # Adjust Brightness
        brightness_level = max(0, min(100, brightness_level + change))
    elif selected_option == 1:  # Adjust Volume
        volume_level = max(0, min(100, volume_level + change))
        simulate_volume_change(volume_level)

    draw_settings_ui()

# Function to reset brightness and volume to defaults
def restore_defaults():
    global brightness_level, volume_level
    brightness_level = 100
    volume_level = 50
    print("Settings restored to defaults.")
    draw_settings_ui()

# Function to draw the settings UI
def draw_settings_ui():
    canvas.delete("all")  # Clear the canvas
    canvas.config(bg=get_brightness_color(brightness_level))  # Set brightness

    # Get current language
    current_language = languages[selected_language_index]
    translation = translations[current_language]

    # Display the settings title based on the current language
    canvas.create_text(240, 50, text=translation['settings'], font=("Arial", 20), fill="black")
    
    # Display brightness and volume options, highlighting the selected option
    for i, option in enumerate(options):
        color = "red" if i == selected_option else "black"
        if option == "Select Language":
            canvas.create_text(240, 300 + i * 60, text=f"{translation['select_language']}: {languages[selected_language_index]}", font=("Arial", 20), fill=color)
        else:
            text_value = brightness_level if option == 'Brightness' else volume_level
            canvas.create_text(240, 150 + i * 60, text=f"{translation[option.lower()]}: {text_value}", font=("Arial", 20), fill=color)

    # Ensure buttons are displayed appropriately
    place_buttons()

# Function to place navigation buttons
def place_buttons():
    up_button.place(x=50, y=20)
    down_button.place(x=400, y=20)
    select_button.place(x=400, y=600)
    back_button.place(x=50, y=600)
    
    if adjust_mode or language_mode:
        left_button.place(x=50, y=20)
        right_button.place(x=400, y=20)
        confirm_button.place(x=400, y=600)
        restore_defaults_button.place(x=205, y=600)
        
        up_button.place_forget()
        down_button.place_forget()
        select_button.place_forget()
    else:
        left_button.place_forget()
        right_button.place_forget()
        confirm_button.place_forget()
        restore_defaults_button.place_forget()

# Function to handle button presses
def select_button_press():
    global adjust_mode, language_mode
    if language_mode:
        language_mode = False
        save_settings()  # Save the language setting when confirmed
    elif selected_option == len(options) - 1:  # If "Select Language" is highlighted
        language_mode = True
    else:
        adjust_mode = not adjust_mode
    draw_settings_ui()

# Function to navigate between settings options (up and down)
def up_button_press():
    global selected_option
    if language_mode:
        selected_language_index = (selected_language_index - 1) % len(languages)
        change_language(selected_language_index)
    elif not adjust_mode:
        selected_option = (selected_option - 1) % len(options)  # Include "Select Language" option
        draw_settings_ui()

def down_button_press():
    global selected_option
    if language_mode:
        selected_language_index = (selected_language_index + 1) % len(languages)
        change_language(selected_language_index)
    elif not adjust_mode:
        selected_option = (selected_option + 1) % len(options)  # Include "Select Language" option
        draw_settings_ui()

# Function to navigate language selection using left/right buttons
def navigate_language(change):
    global selected_language_index
    selected_language_index = (selected_language_index + change) % len(languages)
    change_language(selected_language_index)

# Function to go back to the main menu
def back_to_main_menu():
    save_settings()  # Save settings when returning to main menu
    root.destroy()  # Close the health UI window
    subprocess.run(["python", "menu.py"])  # Launch the main menu UI

# Create navigation buttons and assign the functions to them
up_button = Button(root, text="Up", command=up_button_press)
down_button = Button(root, text="Down", command=down_button_press)
select_button = Button(root, text="Select", command=select_button_press)
back_button = Button(root, text="Main Menu", command=back_to_main_menu)

# Create left, right, and confirm buttons for adjusting in 'adjust mode'
left_button = Button(root, text="Left", command=lambda: navigate_language(-1) if language_mode else adjust_brightness_or_volume(-5))
right_button = Button(root, text="Right", command=lambda: navigate_language(1) if language_mode else adjust_brightness_or_volume(5))
confirm_button = Button(root, text="Confirm", command=select_button_press)

# Create restore defaults button
restore_defaults_button = Button(root, text="Restore Defaults", command=restore_defaults)

# Load initial settings
load_settings()

# Draw initial settings UI
draw_settings_ui()

# Start Tkinter event loop
root.mainloop()


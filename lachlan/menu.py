from tkinter import Tk, Canvas, Button
from PIL import Image, ImageDraw, ImageFont, ImageTk
import os  # To call the health UI script

# Initialize the Tkinter window
root = Tk()
root.title("Main Menu UI with Dog GIF")
root.geometry("500x700")

# Create a canvas to display the UI
canvas = Canvas(root, width=480, height=640, bg="white")
canvas.pack()

# Path to your GIF
gif_path = r"C:\Users\super\OneDrive\Desktop\UOW 2024 - Spring Sem\ECTE250\Flash.gif"

# Load the GIF using Pillow
gif_image = Image.open(gif_path)
gif_image = gif_image.resize((150, 150))  # Larger size for the GIF

# Convert the GIF to a format Tkinter can display
gif_frames = []
try:
    while True:
        gif_frames.append(ImageTk.PhotoImage(gif_image.copy()))
        gif_image.seek(len(gif_frames))  # Go to next frame
except EOFError:
    pass  # When no more frames, catch the error

# Load fonts for the UI
try:
    font_large = ImageFont.truetype("arial.ttf", 50)
    font_medium = ImageFont.truetype("arial.ttf", 35)
    font_small = ImageFont.truetype("arial.ttf", 20)  # Increased size for buttons
except IOError:
    font_large = ImageFont.load_default()
    font_medium = ImageFont.load_default()
    font_small = ImageFont.load_default()

# Define the different screens (Main Menu and Medication)
current_screen = "main_menu"  # Start with the main menu
menu_items = ["Medication", "Health", "Weather", "Date"]
current_selection = 0  # Tracks the index of the currently selected item

# Function to draw the main menu UI
def draw_main_menu_ui():
    canvas.delete("all")  # Clear the canvas

    # Create a blank image to draw on
    img = Image.new('RGB', (480, 640), color='white')
    draw = ImageDraw.Draw(img)

    # Draw the time and date
    draw.text((140, 50), "6:42 AM", font=font_large, fill="black")

    # Draw weather (with outline if selected)
    if current_selection == 2:
        draw.rectangle([(90, 200), (380, 240)], outline="red", width=3)  # Outline for Weather
    draw.text((120, 200), "Weather: 22°C", font=font_medium, fill="black")

    # Draw Medication and Health buttons with an outline around the selected item
    if current_selection == 0:
        draw.rectangle([(100, 300), (240, 340)], outline="red", width=3)  # Outline for Medication
    draw.text((120, 300), "Medication", font=font_small, fill="black")

    if current_selection == 1:
        draw.rectangle([(260, 300), (400, 340)], outline="red", width=3)  # Outline for Health
    draw.text((280, 300), "Health", font=font_small, fill="black")

    # Draw the date (with outline if selected)
    if current_selection == 3:
        draw.rectangle([(140, 510), (340, 590)], outline="red", width=3)  # Outline for Date
    draw.text((160, 520), "Tuesday\n10/09/2024", font=font_medium, fill="black", align="center")

    # Convert the Pillow image to Tkinter's PhotoImage
    tk_img = ImageTk.PhotoImage(img)
    canvas.create_image(0, 0, anchor="nw", image=tk_img)
    canvas.image = tk_img  # Keep reference to avoid garbage collection

    # Display the GIF in the designated space
    if gif_frames:
        canvas.create_image(240, 400, anchor="center", image=gif_frames[0])
        update_gif(1)

# Function to update the GIF frames
def update_gif(frame):
    frame = (frame + 1) % len(gif_frames)
    canvas.create_image(240, 400, anchor="center", image=gif_frames[frame])
    root.after(100, update_gif, frame)  # 100 milliseconds between frames

# Button functions to control the selection
def up_button_press():
    global current_selection
    current_selection = (current_selection - 1) % len(menu_items)
    if current_screen == "main_menu":
        draw_main_menu_ui()

def down_button_press():
    global current_selection
    current_selection = (current_selection + 1) % len(menu_items)
    if current_screen == "main_menu":
        draw_main_menu_ui()

def select_button_press():
    global current_screen
    if current_screen == "main_menu":
        if current_selection == 0:  # Medication is selected
            current_screen = "medication"
            root.destroy()  # Close the main menu window
            os.system('python Medication.py')  # Switch to the Medication UI
        elif current_selection == 1:  # Health is selected
            current_screen = "health"
            root.destroy()  # Close the main menu window
            os.system('python health.py')  # Switch to the Health UI
        elif current_selection == 2:  # Weather
            print("Weather selected!")
        elif current_selection == 3:  # Date
            print("Date selected!")

def settings_button_press():
    root.destroy()  # Close the main menu window
    os.system('python settings.py')  # Open the Settings UI

# Create navigation buttons
up_button = Button(root, text="Up", command=up_button_press)
up_button.place(x=50, y=20)

down_button = Button(root, text="Down", command=down_button_press)
down_button.place(x=400, y=20)

select_button = Button(root, text="Select", command=select_button_press)
select_button.place(x=50, y=600)

settings_button = Button(root, text="Settings", command=settings_button_press)
settings_button.place(x=400, y=600)

# Draw the UI for the first time
draw_main_menu_ui()

# Run the Tkinter event loop
root.mainloop()



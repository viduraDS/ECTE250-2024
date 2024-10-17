from tkinter import Tk, Canvas, Button
from PIL import Image, ImageDraw, ImageFont, ImageTk
import subprocess

# Initialize Tkinter window
root = Tk()
root.title("Health Screen UI")
root.geometry("500x700")

# Create canvas
canvas = Canvas(root, width=480, height=640, bg="white")
canvas.pack()

# Load fonts (adjusted for the same scale as the menu UI)
try:
    font_huge = ImageFont.truetype("arial.ttf", 40)
    font_large = ImageFont.truetype("arial.ttf", 30)
    font_medium = ImageFont.truetype("arial.ttf", 20)
    font_small = ImageFont.truetype("arial.ttf", 18)
except IOError:
    font_huge = ImageFont.load_default()
    font_large = ImageFont.load_default()
    font_medium = ImageFont.load_default()
    font_small = ImageFont.load_default()

# Variables to track interaction (for to-do list selection)
selected_checklist_item = 0
checklist_items = ["Go for a walk", "Call a loved one", "Take my medication", "Drink enough water"]
checklist_status = [False] * len(checklist_items)  # False means not completed, True means completed

# Function to draw the health screen UI
def draw_health_screen():
    # Create image for the screen
    screen = Image.new('RGB', (480, 640), 'white')
    draw = ImageDraw.Draw(screen)

    # Add the time in the top left and the date in the top right
    draw.text((60, 80), "6:42 AM", font=font_medium, fill="black")
    draw.text((340, 80), "10/10/2024", font=font_medium, fill="black")

    # Add encouragement text
    draw.text((80, 140), "You are strong", font=font_large, fill="black")
    draw.text((80, 180), "Today is a new day", font=font_large, fill="black")

    # Add the to-do list title
    draw.text((80, 250), "To do list:", font=font_medium, fill="black")

    # Add checkboxes and to-do list items with matching scale
    for i, item in enumerate(checklist_items):
        color = "red" if i == selected_checklist_item else "black"
        # Draw checkbox
        draw.rectangle([60, 300 + i * 40, 80, 320 + i * 40], outline=color, fill="white")
        # If the item is marked as done, add a cross
        if checklist_status[i]:
            draw.line((60, 300 + i * 40, 80, 320 + i * 40), fill=color, width=2)
            draw.line((60, 320 + i * 40, 80, 300 + i * 40), fill=color, width=2)
        # Draw the item text
        draw.text((100, 300 + i * 40), item, font=font_medium, fill="black")

    # Add "Begin breathing exercise" text with a different color when selected
    color = "red" if selected_checklist_item == len(checklist_items) else "black"
    draw.text((70, 500), "Begin breathing exercise", font=font_large, fill=color)

    # Convert the image to something Tkinter can display
    tk_img = ImageTk.PhotoImage(screen)

    # Display the image on the canvas
    canvas.create_image(0, 0, anchor="nw", image=tk_img)
    canvas.image = tk_img  # Keep reference to avoid garbage collection

# Functions for button actions
def up_button_press():
    global selected_checklist_item
    selected_checklist_item = (selected_checklist_item - 1) % (len(checklist_items) + 1)
    draw_health_screen()

def down_button_press():
    global selected_checklist_item
    selected_checklist_item = (selected_checklist_item + 1) % (len(checklist_items) + 1)
    draw_health_screen()

def select_button_press():
    global selected_checklist_item
    if selected_checklist_item < len(checklist_items):  # If a to-do item is selected
        checklist_status[selected_checklist_item] = not checklist_status[selected_checklist_item]  # Toggle status
        draw_health_screen()  # Redraw the screen to reflect the updated checklist
    else:
        # If "Begin Breathing Exercise" is selected, open the breathing exercise UI
        print("Launching Breathing Exercise UI")
        root.destroy()  # Close the health UI window
        subprocess.run(["python", "breath.py"])  # Launch the breathing exercise UI

def back_button_press():
    root.destroy()  # Close the health UI window
    subprocess.run(["python", "menu.py"])  # Launch the main menu UI


# Create navigation buttons and assign the functions to them
up_button = Button(root, text="Up", command=up_button_press)
up_button.place(x=50, y=20)

down_button = Button(root, text="Down", command=down_button_press)
down_button.place(x=400, y=20)

select_button = Button(root, text="Select", command=select_button_press)
select_button.place(x=400, y=600)

back_button = Button(root, text="Main Menu", command=back_button_press)
back_button.place(x=50, y=600)

# Initial drawing of the health screen
draw_health_screen()

# Start Tkinter event loop
root.mainloop()





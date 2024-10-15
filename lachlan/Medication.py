from tkinter import Tk, Canvas, Button
from PIL import Image, ImageDraw, ImageFont, ImageTk  # Import ImageTk to handle the display of images
import subprocess  # For running the main menu script

# Initialize variables
current_day = 0  # Start with Monday
days_of_week = ["M", "T", "W", "T", "F", "S", "S"]
full_days = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"]
medication_schedule = {
    "Monday": {"Breakfast": ["Fish Oil", "Iron"], "Dinner": ["Multivitamin"]},
    "Tuesday": {"Breakfast": ["Vitamin C"], "Dinner": ["Calcium"]},
    "Wednesday": {"Breakfast": ["Omega-3"], "Dinner": ["Iron"]},
    "Thursday": {"Breakfast": ["Fish Oil", "Vitamin D"], "Dinner": []},
    "Friday": {"Breakfast": ["Multivitamin"], "Dinner": ["Fish Oil"]},
    "Saturday": {"Breakfast": [], "Dinner": []},
    "Sunday": {"Breakfast": ["Vitamin B12"], "Dinner": ["Magnesium"]}
}

# Create a window using Tkinter
root = Tk()
root.title("Medication UI")
root.geometry("500x700")  # Set window size

# Create a canvas for drawing
canvas = Canvas(root, width=480, height=640, bg="white")
canvas.pack()

# Load fonts for PIL ImageDraw
try:
    font_large = ImageFont.truetype("arial.ttf", 24)
    font_small = ImageFont.truetype("arial.ttf", 18)
except IOError:
    font_large = ImageFont.load_default()
    font_small = ImageFont.load_default()

# Function to draw the UI on the canvas
def draw_ui(selected_day):
    # Create a blank image with white background to draw on
    img = Image.new('RGB', (480, 640), color='white')
    draw = ImageDraw.Draw(img)

    # Draw the time and date
    draw.text((20, 70), "6:42 AM", font=font_large, fill="black")
    draw.text((360, 70), "6/10/2024", font=font_large, fill="black")

    # Draw the calendar structure
    for i in range(7):
        x_start = 60 + i * 50
        y_start = 150
        face_color = 'red' if i == selected_day else 'lightgray'
        text_color = 'white' if i == selected_day else 'black'
        draw.rectangle([x_start - 20, y_start - 10, x_start + 30, y_start + 30], fill=face_color, outline="black")
        draw.text((x_start, y_start), days_of_week[i], font=font_large, fill=text_color)

    # Draw selected day's name
    day_name = full_days[selected_day]
    draw.text((20, 210), f"{day_name}:", font=font_large, fill="black")

    # Display the medications
    breakfast_meds = medication_schedule[day_name]["Breakfast"]
    dinner_meds = medication_schedule[day_name]["Dinner"]

    draw.text((20, 250), "Breakfast:", font=font_large, fill="black")
    draw.text((20, 280), "\n".join(breakfast_meds), font=font_small, fill="dimgray")

    draw.text((20, 350), "Dinner:", font=font_large, fill="black")
    draw.text((20, 380), "\n".join(dinner_meds), font=font_small, fill="dimgray")

    # Convert the Pillow image to a format Tkinter can display
    tk_img = ImageTk.PhotoImage(img)

    # Clear the canvas and redraw the UI
    canvas.delete("all")
    canvas.create_image(0, 0, anchor="nw", image=tk_img)
    canvas.image = tk_img  # Keep a reference to avoid garbage collection

# Callback functions for button presses
def left_button_press():
    global current_day
    current_day = (current_day - 1) % len(days_of_week)
    draw_ui(current_day)

def right_button_press():
    global current_day
    current_day = (current_day + 1) % len(days_of_week)
    draw_ui(current_day)

def main_menu_button_press():
    # Close the Medication UI and run the main menu UI
    root.destroy()  # Close the current window
    subprocess.run(["python", "menu.py"])  # Replace with the correct path to 'menu.py'

def select_button_press():
    print("Select button pressed!")

# Create buttons for navigation
left_button = Button(root, text="< Left", command=left_button_press)
left_button.place(x=50, y=20)

right_button = Button(root, text="Right >", command=right_button_press)
right_button.place(x=400, y=20)

main_menu_button = Button(root, text="Main Menu", command=main_menu_button_press)
main_menu_button.place(x=50, y=600)

select_button = Button(root, text="Select", command=select_button_press)
select_button.place(x=400, y=600)

# Initial drawing of the UI
draw_ui(current_day)

# Start the Tkinter event loop
root.mainloop()


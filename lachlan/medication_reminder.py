from PIL import Image, ImageDraw, ImageFont

# Set up the e-paper display size (substitute your actual e-paper resolution here)
DISPLAY_WIDTH = 640
DISPLAY_HEIGHT = 384

# Create a blank image for drawing
image = Image.new('RGB', (DISPLAY_WIDTH, DISPLAY_HEIGHT), 'white')
draw = ImageDraw.Draw(image)

# Load a font (ensure the font path is correct, or use a default Pillow font)
try:
    font_large = ImageFont.truetype("arial.ttf", 20)  # Adjust the path to your font
    font_medium = ImageFont.truetype("arial.ttf", 16)
    font_small = ImageFont.truetype("arial.ttf", 14)
except IOError:
    # Fallback to default font if the specified font isn't available
    font_large = ImageFont.load_default()
    font_medium = ImageFont.load_default()
    font_small = ImageFont.load_default()

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

# Function to update the UI
def update_ui(selected_day):
    # Clear the image
    draw.rectangle((0, 0, DISPLAY_WIDTH, DISPLAY_HEIGHT), fill='white')

    # Display the time and date in black
    time_text = "6:42 AM"
    date_text = "6/10/2024"
    draw.text((50, 20), time_text, font=font_large, fill='black')
    draw.text((500, 20), date_text, font=font_large, fill='black')

    # Draw the calendar structure with colors
    for i in range(7):
        x_start = 100 + i * 70
        y_start = 100
        face_color = 'red' if i == selected_day else 'lightgrey'
        text_color = 'white' if i == selected_day else 'black'
        draw.rectangle([x_start, y_start, x_start + 50, y_start + 50], fill=face_color, outline='black')
        draw.text((x_start + 15, y_start + 15), days_of_week[i], font=font_medium, fill=text_color)

    # Display selected day's name in black
    day_name = full_days[selected_day]
    draw.text((250, 200), f"{day_name}:", font=font_large, fill='black')

    # Display the medications under "Breakfast" and "Dinner" in shades of grey
    breakfast_meds = medication_schedule[day_name]["Breakfast"]
    dinner_meds = medication_schedule[day_name]["Dinner"]

    # Display Breakfast and Dinner in bold black, and meds in dark grey
    draw.text((100, 250), "Breakfast:", font=font_medium, fill='black')
    draw.text((100, 280), "\n".join(breakfast_meds), font=font_small, fill='dimgray')

    draw.text((100, 330), "Dinner:", font=font_medium, fill='black')
    draw.text((100, 360), "\n".join(dinner_meds), font=font_small, fill='dimgray')

# Function to navigate left (previous day)
def left():
    global current_day
    current_day = (current_day - 1) % len(days_of_week)
    update_ui(current_day)
    image.show()

# Function to navigate right (next day)
def right():
    global current_day
    current_day = (current_day + 1) % len(days_of_week)
    update_ui(current_day)
    image.show()

# Function for the "Back" button
def back():
    print("Back button pressed!")
    # Add back functionality here

# Initialize the UI
update_ui(current_day)

# Save the image or display it
image.show()  # For testing on your PC

# For an actual e-paper, send the `image` to the display using the appropriate driver.

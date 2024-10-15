import time
from tkinter import Tk, Canvas, Button
from PIL import Image, ImageDraw, ImageFont, ImageTk
import threading
import subprocess

# Initialize Tkinter window
root = Tk()
root.title("Breathing Exercise")
root.geometry("500x700")

# Create canvas
canvas = Canvas(root, width=480, height=640, bg="white")
canvas.pack()

# Load fonts
try:
    font_large = ImageFont.truetype("arial.ttf", 40)
    font_medium = ImageFont.truetype("arial.ttf", 30)
except IOError:
    font_large = ImageFont.load_default()
    font_medium = ImageFont.load_default()

# Variables to track the loop count
loop_count = 0
max_loops = 2  # We want to loop twice
is_exercise_running = False  # To track if the exercise is running
stop_exercise = False  # To track if the exercise should stop

# Function to display different phases (Breathe In, Hold, Exhale, etc.)
def draw_exercise_phase(phase_text):
    background = create_background()
    draw = ImageDraw.Draw(background)

    # Calculate text size and center it horizontally
    bbox = draw.textbbox((0, 0), phase_text, font=font_large)
    text_width = bbox[2] - bbox[0]  # Text width
    text_height = bbox[3] - bbox[1]  # Text height

    x_position = (480 - text_width) // 2  # Center the text horizontally
    y_position = (640 - text_height) // 2  # Center the text vertically

    # Draw the text at the calculated position
    draw.text((x_position, y_position), phase_text, font=font_large, fill="black")

    # Convert image to displayable format and show it on the canvas
    tk_img = ImageTk.PhotoImage(background)
    canvas.create_image(0, 0, anchor="nw", image=tk_img)
    canvas.image = tk_img  # Keep a reference to avoid garbage collection

    root.update()  # Force update to display the changes

# Main breathing exercise sequence
def breathing_exercise():
    global loop_count, is_exercise_running

    while loop_count < max_loops and not stop_exercise:
        if stop_exercise:
            break

        # First phase: Breathe In
        draw_exercise_phase("Breathe In")
        for _ in range(4):  # Use small time steps and check for stop signal
            if stop_exercise:
                return
            time.sleep(1)

        # Second phase: Hold
        draw_exercise_phase("Hold")
        for _ in range(3):
            if stop_exercise:
                return
            time.sleep(1)

        # Third phase: Exhale
        draw_exercise_phase("Exhale")
        for _ in range(4):
            if stop_exercise:
                return
            time.sleep(1)

        loop_count += 1

    if not stop_exercise:
        # After loops, display 'Exercise Complete'
        draw_exercise_phase("Exercise Complete")

    is_exercise_running = False  # Mark exercise as stopped

# Start the exercise
def start_exercise():
    global is_exercise_running, stop_exercise, loop_count
    if not is_exercise_running:
        is_exercise_running = True
        stop_exercise = False
        loop_count = 0  # Reset loop count
        # Delay for 1 second before starting the exercise
        draw_exercise_phase("Starting in 1 second...")
        time.sleep(1)
        # Start the exercise in a separate thread to keep the UI responsive
        exercise_thread = threading.Thread(target=breathing_exercise)
        exercise_thread.start()

# Stop the exercise
def stop_exercise_button():
    global is_exercise_running, stop_exercise
    if is_exercise_running:
        stop_exercise = True  # Set the flag to stop the exercise
        is_exercise_running = False
        # Immediately display "Begin exercise?" message after stopping
        draw_exercise_phase("Begin exercise?")

# Create background with the mountain silhouette and concentric circles
def create_background():
    img = Image.new('RGB', (480, 640), 'white')
    draw = ImageDraw.Draw(img)

    # Draw concentric circles with decreasing opacity (simulating a peaceful design)
    for i in range(0, 640, 40):
        shade = 255 - int(i / 2)
        draw.ellipse((240 - i, 320 - i, 240 + i, 320 + i), outline=(shade, shade, shade), width=2)

    # Draw a centered mountain-like silhouette with wider peaks
    silhouette_color = (50, 50, 50)

    # Adjust the widths of the peaks slightly
    draw.polygon([(0, 580), (100, 420), (200, 580)], fill=silhouette_color)  # Left peak, wider
    draw.polygon([(150, 580), (240, 380), (330, 580)], fill=silhouette_color)  # Central, higher peak, wider
    draw.polygon([(280, 580), (380, 460), (480, 580)], fill=silhouette_color)  # Right peak, wider

    draw.rectangle([0, 580, 480, 640], fill=silhouette_color)  # Fill the bottom area

    return img

def back_button_press():
    # Close the current window and open the main menu UI
    root.destroy()  # Close the current breathing exercise window
    subprocess.run(["python", "menu.py"])  # Run the menu.py to launch the main menu

# Create buttons for starting, stopping the exercise, and returning to main menu
start_button = Button(root, text="Start", command=start_exercise)
start_button.place(x=380, y=600)

stop_button = Button(root, text="Stop", command=stop_exercise_button)
stop_button.place(x=280, y=600)

main_menu_button = Button(root, text="Main Menu", command=back_button_press)
main_menu_button.place(x=50, y=600)

# Initially display the silhouette with the "Begin exercise?" prompt
draw_exercise_phase("Begin exercise?")

# Start the Tkinter event loop
root.mainloop()



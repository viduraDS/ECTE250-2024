from PIL import Image, ImageDraw, ImageFont

# Set up the e-paper display size (substitute your actual e-paper resolution here)
DISPLAY_WIDTH = 400
DISPLAY_HEIGHT = 300

# Create a blank image for drawing
image = Image.new('RGB', (DISPLAY_WIDTH, DISPLAY_HEIGHT), 'white')
draw = ImageDraw.Draw(image)

# Load a font (ensure the font path is correct, or use a default Pillow font)
try:
    font_large = ImageFont.truetype("arial.ttf", 50)  # Adjust the path to your font
    font_medium = ImageFont.truetype("arial.ttf", 35)
    font_small = ImageFont.truetype("arial.ttf", 14)
except IOError:
    # Fallback to default font if the specified font isn't available
    font_large = ImageFont.load_default()
    font_medium = ImageFont.load_default()
    font_small = ImageFont.load_default()

# Set up the static UI layout with red accents, larger time/date, and space for GIF
def create_ui():
    # Clear the image
    draw.rectangle((0, 0, DISPLAY_WIDTH, DISPLAY_HEIGHT), fill='white')

    # Display the time in large font
    time_text = "6:42 AM"
    time_bbox = draw.textbbox((0, 0), time_text, font=font_large)  # Using textbbox instead of textsize
    time_w = time_bbox[2] - time_bbox[0]  # Calculate width of text
    draw.text(((DISPLAY_WIDTH - time_w) / 2, 20), time_text, font=font_large, fill='black')

    # Display the date with red background
    date_text = "Tuesday\n10/09/2024"
    date_bbox = draw.textbbox((0, 0), date_text, font=font_medium)
    date_w = date_bbox[2] - date_bbox[0]
    date_x = (DISPLAY_WIDTH - date_w) / 2
    date_y = 200
    draw.rectangle([date_x - 10, date_y - 10, date_x + date_w + 10, date_y + date_bbox[3] + 10], fill="red", outline="black")
    draw.text((date_x, date_y), date_text, font=font_medium, fill="black")

    # Draw two buttons for "Record" and "Load"
    draw.rectangle([150, 280, 300, 340], fill="white", outline="red")
    draw.text((175, 300), "Record", font=font_small, fill="black")

    draw.rectangle([350, 280, 500, 340], fill="white", outline="red")
    draw.text((375, 300), "Load", font=font_small, fill="black")

    # Placeholder for the Dog GIF
    gif_text = "[Dog GIF Here]"
    gif_bbox = draw.textbbox((0, 0), gif_text, font=font_small)
    gif_w = gif_bbox[2] - gif_bbox[0]
    draw.rectangle([200, 160, 440, 200], outline="black", fill="white")
    draw.text(((DISPLAY_WIDTH - gif_w) / 2, 170), gif_text, font=font_small, fill="black")

    # Buttons around the screen edges
    draw.rectangle([10, 10, 100, 60], fill="black", outline="red")  # Up button
    draw.text((35, 30), "Up", font=font_small, fill="white")

    draw.rectangle([540, 10, 630, 60], fill="black", outline="red")  # Down button
    draw.text((555, 30), "Down", font=font_small, fill="white")

    draw.rectangle([10, 320, 100, 370], fill="red", outline="black")  # Select button
    draw.text((30, 340), "Select", font=font_small, fill="white")

    draw.rectangle([540, 320, 630, 370], fill="red", outline="black")  # Settings button
    draw.text((550, 340), "Settings", font=font_small, fill="white")

# Create the updated UI
create_ui()

# Save the image for testing or send it to the e-paper display
image.save('epaper_ui_test_fixed.png')

# If you're testing on actual hardware, you can now send the `image` to the e-paper display driver.































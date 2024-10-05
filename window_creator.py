import os
import tkinter as tk
from PIL import Image, ImageTk
import pyautogui
import time
import logging


def show_image_in_window(image, x=0, y=0):
    logging.info("Initializing window to display image.")

    # Check if there is already a Tk instance, and create a Toplevel if so
    if not tk._default_root:
        logging.debug("No Tk instance found. Creating new Tk instance.")
        window = tk.Tk()
    else:
        logging.debug("Tk instance found. Creating Toplevel window.")
        window = tk.Toplevel()

    # Convert image to RGB if not already in RGB mode
    if image.mode != "RGB":
        logging.debug("Image mode is not RGB. Converting image to RGB.")
        image = image.convert("RGB")
    else:
        logging.debug("Image is already in RGB mode.")

    # Store click position and window coordinates
    click_position = [None, None]
    window_coordinates = [None, None, None, None]

    # Function to handle mouse click
    def on_click(event):
        logging.info(f"Mouse click detected at position ({event.x_root}, {event.y_root})")

        # Record the click coordinates relative to the screen
        click_position[0] = event.x_root
        click_position[1] = event.y_root
        logging.debug(f"Click coordinates recorded: {click_position}")

        # Minimize the window
        logging.debug("Minimizing window.")
        window.iconify()

        # Replay the click after minimizing
        time.sleep(1)  # Give time for the window to minimize
        logging.debug(f"Replaying click at position: {click_position}")
        pyautogui.click(click_position[0], click_position[1])  # Replay click

        # Get current size and position of the window
        x1 = window.winfo_x()
        y1 = window.winfo_y()
        x2 = x1 + window.winfo_width()
        y2 = y1 + window.winfo_height()

        # Store the window coordinates
        window_coordinates[0], window_coordinates[1] = x1, x2
        window_coordinates[2], window_coordinates[3] = y1, y2
        logging.debug(f"Window coordinates: x1={x1}, x2={x2}, y1={y1}, y2={y2}")

        # Close the window after the click is recorded
        logging.debug("Closing window.")
        window.quit()  # Stop the Tkinter mainloop
        window.destroy()  # Properly close the window

    # Create a label to display the image
    logging.info("Creating label to display the image.")
    tk_image = ImageTk.PhotoImage(image)
    label = tk.Label(window, image=tk_image)
    label.image = tk_image  # Keep a reference to the image to prevent garbage collection
    label.pack()

    # Bring the window to the front
    logging.debug("Bringing window to the front (topmost).")
    window.attributes("-topmost", True)

    # Bind the left mouse click event to the on_click function
    logging.debug("Binding left mouse click event to on_click function.")
    window.bind("<Button-1>", on_click)

    # Set the window size to the image size
    logging.debug(f"Setting window size to {image.width}x{image.height}.")
    window.geometry(f"{image.width}x{image.height}")

    # Set the window position to cover the specified coordinates (x, y)
    logging.debug(f"Positioning window at coordinates ({x}, {y}).")
    window.geometry(f"+{x}+{y}")  # Position the window at the coordinates where the screenshot was taken

    # Start the Tkinter event loop
    logging.info("Starting Tkinter mainloop.")
    window.mainloop()

    # After window.quit(), return the click position and window coordinates
    logging.info(f"Returning click position: {click_position} and window coordinates: {window_coordinates}")
    return click_position, window_coordinates


if __name__ == "__main__":
    # Get the current script filename (without extension) to create a log file
    script_name = os.path.splitext(os.path.basename(__file__))[0]
    log_filename = f"{script_name}.log"

    # Set up logging
    console_handler = logging.StreamHandler()
    file_handler = logging.FileHandler(log_filename)

    # Set logging levels
    console_handler.setLevel(logging.INFO)  # Print info and above to console
    file_handler.setLevel(logging.WARNING)   # Write warning and above to file

    # Create a logging formatter
    formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')
    console_handler.setFormatter(formatter)
    file_handler.setFormatter(formatter)

    # Add handlers to the root logger
    logging.getLogger().setLevel(logging.DEBUG)  # Capture all messages
    logging.getLogger().addHandler(console_handler)
    logging.getLogger().addHandler(file_handler)
    # Load the image using PIL
    logging.info("Loading image.")
    
    # Example usage
    img = Image.open("1.jpg")
    screenshot_x, screenshot_y = 100, 100  # Replace with the actual coordinates of your screenshot

    # Show the image and return the screen click position and window coordinates
    logging.info("Showing image in window and waiting for user interaction.")
    click_position, coordinates = show_image_in_window(img, screenshot_x, screenshot_y)

    # Print the coordinates
    logging.info(f"Screen Click Position: {click_position}")
    logging.info(f"Window Coordinates: {coordinates}")

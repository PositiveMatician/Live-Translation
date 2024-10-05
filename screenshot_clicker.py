import logging
from PIL import Image
import pyautogui
import os

def capture_screenshot(coords: tuple) -> Image.Image:
    logger.debug(f"Received coordinates: {coords}")
    
    x1, x2, y1, y2 = coords
    # Calculate the width and height from the coordinates
    width = x2 - x1
    height = y2 - y1

    try:
        # Capture the screenshot of the specific region
        logger.info(f"Capturing screenshot for region: (x1: {x1}, y1: {y1}, width: {width}, height: {height})")
        screenshot = pyautogui.screenshot(region=(x1, y1, width, height))

        # Convert the screenshot to a PIL Image object
        img = screenshot.convert("RGB")
        logger.info("Screenshot captured successfully.")
        
        return img
    except Exception as e:
        logger.error(f"Failed to capture screenshot: {e}")
        return None

if __name__ == '__main__':

    # Configure logging
    # Get the name of the current script without the extension
    script_name = os.path.splitext(os.path.basename(__file__))[0]
    log_file_name = f"{script_name}.log"

    # Create a logger
    logger = logging.getLogger()
    logger.setLevel(logging.DEBUG)

    # Create handlers
    # Console handler for info level and above
    console_handler = logging.StreamHandler()
    console_handler.setLevel(logging.INFO)

    # File handler for logs of level DEBUG and above
    file_handler = logging.FileHandler(log_file_name)
    file_handler.setLevel(logging.DEBUG)

    # Create a formatter and set it for both handlers
    formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')
    console_handler.setFormatter(formatter)
    file_handler.setFormatter(formatter)

    # Add the handlers to the logger
    logger.addHandler(console_handler)
    logger.addHandler(file_handler)
    # Example usage:
    # Capture an image between (100, 100) and (500, 400)
    region = (100, 500, 100, 400)  # (x1, x2, y1, y2)
    image = capture_screenshot(region)
    
    if image:
        image.show()  # Opens the captured image using the default viewer
    else:
        logger.error("Screenshot could not be displayed due to capture failure.")

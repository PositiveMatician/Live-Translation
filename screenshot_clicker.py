from PIL import Image
import pyautogui
import os


def capture_screenshot(coords: tuple) -> Image.Image:
    with open(os.path.basename(__file__).replace('.py', '.log'),'a') as file:
        file.write(f"Received coordinates: {coords}")
    
    x1, x2, y1, y2 = coords
    # Calculate the width and height from the coordinates
    width = x2 - x1
    height = y2 - y1

    try:
        # Capture the screenshot of the specific region
        print(f"Capturing screenshot for region: (x1: {x1}, y1: {y1}, width: {width}, height: {height})")
        screenshot = pyautogui.screenshot(region=(x1, y1, width, height))

        # Convert the screenshot to a PIL Image object
        img = screenshot.convert("RGB")
        print("Screenshot captured successfully.")
        
        return img
    except Exception as e:
        with open(os.path.basename(__file__).replace('.py', '.log'),'a') as file:
            file.write(f"Failed to capture screenshot: {e}")
        return None

if __name__ == '__main__':
    # Example usage:
    # Capture an image between (100, 100) and (500, 400)
    region = (100, 500, 100, 400)  # (x1, x2, y1, y2)
    image = capture_screenshot(region)
    
    if image:
        image.show()  # Opens the captured image using the default viewer
    else:
        with open(os.path.basename(__file__).replace('.py', '.log'),'a') as file:
            file.write("Screenshot could not be displayed due to capture failure.")

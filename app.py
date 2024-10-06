import extract_image_text
import text_translator
import caption_maker
import overlay_caption_on_image
import window_creator
import screenshot_clicker
from PIL import Image
import io
import os
import win32clipboard 
from win32con import CF_DIB
import keyboard
import threading

# Define the thread variable globally
translation_thread = None


def mid_process(img) -> Image.Image:
    """
    Extracts Japanese text from the given image, translates it, and creates captioned images.

    Args:
        img: The input image to process.

    Returns:
        An image with overlaid captions based on the extracted and translated text.
    """
    # Extract Japanese text from the image
    extraction_result = extract_image_text.extract_japanese_text(img)

    # Process each extracted item
    for pos, item in enumerate(extraction_result):
        text = item['text']

        try:
            # Translate the extracted text
            translated_text = text_translator.translate_text(text)
        except Exception as err:
            with open(os.path.basename(__file__).replace('.py', '.log'), 'a') as file:
                file.write(f"Translation error: {err}\n")
            translated_text = text  # Fallback to original text if translation fails

        # Create a captioned image object
        caption_image_obj = caption_maker.create_captioned_image(translated_text)

        coords = item['coordinates']
        confidence = item['confidence']

        # Update extraction result with translation and captioned image
        extraction_result[pos]['text'] = translated_text
        extraction_result[pos]['original_text'] = text
        extraction_result[pos]['cap img obj'] = caption_image_obj

    # Overlay captions on the original image
    result = overlay_caption_on_image.overlay_images_with_coordinates(img, {'sentences': extraction_result})
    return result

def screen_maker(coords: tuple = (500, 1000, 0, 1000)) -> None:
    """
    Captures a screenshot from the specified coordinates, processes the image,
    and displays it in a window.

    Args:
        coords: A tuple of coordinates in the format (x1, x2, y1, y2).
                 The coordinates should not contain None values.
    """
    # Validate coordinates
    if None in coords:
        with open(os.path.basename(__file__).replace('.py', '.log'), 'a') as file:
            file.write("Invalid coordinates: None detected.\n")
        return None

    print(f"Capturing screenshot with coordinates: {coords}")

    # Capture a screenshot of the specified area
    screenshot = screenshot_clicker.capture_screenshot(coords)


    # Process the captured screenshot
    screenshot = mid_process(screenshot)

    # Display the processed image in a window and get new click coordinates
    click_position, coordinates = window_creator.show_image_in_window(screenshot, coords[0] - 9, coords[2] - 38)

    # Recursive call to allow continuous screenshot capturing
    screen_maker(coordinates)

def copy_image_to_clipboard(image:Image.Image):
    """
    Copies a Pillow Image object to the clipboard without saving it locally.

    Args:
        image (PIL.Image.Image): The Pillow Image object to copy to the clipboard.

    Raises:
        ValueError: If the provided object is not a Pillow Image instance.
    """
    # Validate the input
    if not isinstance(image, Image.Image):
        with open(os.path.basename(__file__).replace('.py', '.log'), 'a') as file:
            file.write("Invalid input: Provided object is not a Pillow Image instance.\n")
        raise ValueError("The provided object is not a Pillow Image instance.")

    try:
        # Create a BytesIO buffer to hold the image data
        with io.BytesIO() as output:
            # Save the image to the buffer in PNG format
            image.save(output, format='PNG')  
            output.seek(0)  # Move to the beginning of the BytesIO buffer

            # Open the clipboard and set the image data
            win32clipboard.OpenClipboard()
            win32clipboard.EmptyClipboard()
            win32clipboard.SetClipboardData(win32clipboard.CF_DIB, output.getvalue())  # Set the image data

        print("Image copied to clipboard successfully.")
    except Exception as e:
        with open(os.path.basename(__file__).replace('.py', '.log'), 'a') as file:
            file.write(f"Failed to copy image to clipboard: {e}\n")
    finally:
        win32clipboard.CloseClipboard()  # Ensure the clipboard is closed

def get_image_from_clipboard() -> Image.Image:
    """
    Retrieves an image from the clipboard and returns it as a Pillow Image object.

    Returns:
        PIL.Image.Image: The Pillow Image object retrieved from the clipboard.

    Raises:
        ValueError: If there is no image in the clipboard or the image format is unsupported.
    """
    try:
        # Open the clipboard
        win32clipboard.OpenClipboard()

        # Check if the clipboard contains an image in DIB format
        if win32clipboard.IsClipboardFormatAvailable(CF_DIB):
            # Get the image data from the clipboard
            dib_data = win32clipboard.GetClipboardData(CF_DIB)
            
            # Create a BytesIO object from the DIB data
            image = Image.open(io.BytesIO(dib_data))

            print("Image retrieved from clipboard successfully.")
            return image
        else:
            with open(os.path.basename(__file__).replace('.py', '.log'), 'a') as file:
                file.write("Clipboard does not contain a DIB image.\n")
            raise ValueError("No image found in the clipboard or unsupported format.")
    except Exception as e:
        with open(os.path.basename(__file__).replace('.py', '.log'), 'a') as file:
            file.write(f"Failed to retrieve image from clipboard: {e}\n")
        raise
    finally:
        win32clipboard.CloseClipboard()  # Ensure the clipboard is closed


def start_translation():
    """
    The function to be called when Num Lock is pressed. This will initiate the translation process.
    """
    print("Starting translation process...")
    # Call your translation functions here, like screen_maker or mid_process.
    screen_maker((0,0,0,0))

def on_demand_translation():
    """
    Listens for the Num Lock key. Starts a new thread to run the translation process
    when the key is pressed, and restarts the thread if it has finished running.
    """
    global translation_thread

    def toggle_translation():
        global translation_thread

        if translation_thread and translation_thread.is_alive():
            print("Translation is already running.")
        else:
            print("Num Lock pressed. Starting a new translation thread.")
            translation_thread = threading.Thread(target=start_translation)
            translation_thread.start()

    # Listen for Num Lock key press
    print("Listening for Num Lock key press to start/stop translation...")
    keyboard.add_hotkey('num lock', toggle_translation)

    # Keep the program running to listen for the key press
    keyboard.wait('esc')  # Press 'esc' to stop listening



if __name__ == "__main__":
    pass
    ## live translation
    # screen_maker((0,100,0,100))
    
    # # Single Image Translation
    # img = Image.open('1.jpg')
    # result = mid_process(img)
    # result.show()

    # # Translate image from clipboard
    # img = get_image_from_clipboard()
    # result = mid_process(img)
    # copy_image_to_clipboard(result)
    # result.show()

    # # On demand Translation 
    # on_demand_translation()

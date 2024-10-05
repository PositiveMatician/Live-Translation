import logging
import extract_image_text
import text_translator
import caption_maker
import overlay_caption_on_image
import window_creator
import screenshot_clicker
from PIL import Image
import io
import win32clipboard 
from win32con import CF_DIB

# Set up logging
logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)  # Set the overall logging level

# Create handlers
console_handler = logging.StreamHandler()  # For console output
file_handler = logging.FileHandler('app.log')  # For logging to a file

# Set logging levels for handlers
console_handler.setLevel(logging.INFO)  # Only info level logs for the console
file_handler.setLevel(logging.WARNING)   # Warning and above for the file

# Create log formatters
console_formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')
file_formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')

# Attach formatters to handlers
console_handler.setFormatter(console_formatter)
file_handler.setFormatter(file_formatter)

# Add handlers to the logger
logger.addHandler(console_handler)
logger.addHandler(file_handler)

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
            logger.error(f"Translation error: {err}")
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
        logger.warning("Invalid coordinates: None detected.")
        return None

    logger.info(f"Capturing screenshot with coordinates: {coords}")

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
        logger.error("Invalid input: Provided object is not a Pillow Image instance.")
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

        logger.info("Image copied to clipboard successfully.")
    except Exception as e:
        logger.error(f"Failed to copy image to clipboard: {e}")
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

            logger.info("Image retrieved from clipboard successfully.")
            return image
        else:
            logger.error("Clipboard does not contain a DIB image.")
            raise ValueError("No image found in the clipboard or unsupported format.")
    except Exception as e:
        logger.error(f"Failed to retrieve image from clipboard: {e}")
        raise
    finally:
        win32clipboard.CloseClipboard()  # Ensure the clipboard is closed


# Starting the screen maker function with initial coordinates
if __name__ == "__main__":
    pass
    ## live translation
    # screen_maker((66, 1490, 76, 694))
    
    ## Single Image Translation
    # img = Image.open('1.jpg')
    # result = mid_process(img)
    # result.show()

    # Translate image from clipboard
    img = get_image_from_clipboard()
    result = mid_process(img)
    copy_image_to_clipboard(result)
    result.show()

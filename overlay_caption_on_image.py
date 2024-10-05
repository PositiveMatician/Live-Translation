import logging
from PIL import Image
from caption_maker import *


def overlay_images_with_coordinates(primary_image, input_data) -> Image.Image:
    """
    Overlays secondary images on a primary image based on specified coordinates.
    
    :param primary_image: The primary image object (PIL Image).
    :param input_data: A dictionary containing sentences and their coordinates.
    
    :return: The updated primary image object.
    """
    updated_image = primary_image.copy()
    logging.info("Starting to overlay images on the primary image.")

    for sentence in input_data['sentences']:
        secondary_image = sentence['cap img obj']
        coords = sentence['coordinates']
        width = coords['x2'] - coords['x1']
        height = coords['y2'] - coords['y1']
        
        # Ensure the secondary image is in RGBA mode
        if secondary_image.mode != 'RGBA':
            secondary_image = secondary_image.convert('RGBA')

        # Resize the secondary image to fit the specified coordinates
        resized_image = secondary_image.resize((width, height), Image.LANCZOS)

        x = coords['x1']
        y = coords['y1']
        
        # Paste the resized secondary image onto the updated primary image
        updated_image.paste(resized_image, (x, y), resized_image)
        logging.info(f"Pasted image at coordinates: ({x}, {y}) with size: ({width}, {height})")

    logging.info("Image overlay completed successfully.")
    return updated_image

def run(input_data):
    """
    Loads the primary image and overlays captioned images based on input data.
    
    :param input_data: A dictionary containing sentences and their coordinates.
    
    :return: The resulting image after overlaying captions.
    """
    logging.info("Loading primary image.")
    primary_img = Image.open('1.jpg')

    secondary_images = []
    for sentence in input_data['sentences']:
        # Load secondary images (make sure these paths are correct)
        text = sentence['text']
        secondary_img1 = create_captioned_image(text)

        # Append the secondary image to the list
        sentence['cap img obj'] = secondary_img1  # Store the captioned image in the sentence dictionary
        secondary_images.append(secondary_img1)

    # Overlay images
    result_image = overlay_images_with_coordinates(primary_img, input_data)

    return result_image

# Example usage:
if __name__ == "__main__":
    # Set up logging configuration
    logging.basicConfig(
        level=logging.INFO,  # Set the default level to INFO
        format='%(asctime)s - %(levelname)s - %(message)s',
        handlers=[
            logging.FileHandler('overlay_caption_on_image.log'),  # Log file
            logging.StreamHandler()  # Console output
        ]
    )
    # Example input data
    input_data = {
        'sentences': [
            {'text': 'Just like', 'coordinates': {'x1': 78, 'y1': 222, 'x2': 1185, 'y2': 496}}
        ],
        'dimensions': {'width': 1280, 'height': 720}
    }

    result_image = run(input_data)
    # To save or display the result image
    result_image.show()  # Display the image
    # result_image.save('path/to/save/overlay_image.png')  # Uncomment to save

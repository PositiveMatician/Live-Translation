import logging
from PIL import Image, ImageDraw, ImageFont
import os
from text_translator import detect_language  # Ensure this import is correct

def create_captioned_image(text: str, font_size: int = 360, top_margin_pct: float = 0.1, bottom_margin_pct: float = 0.3, left_margin_pct: float = 0.1, right_margin_pct: float = 0.1, background_opacity: int = 200) -> Image.Image:
    """
    Create an image with a caption.

    Parameters:
        text (str): The text to be displayed on the image.
        font_size (int): The size of the font for the text. Default is 360.
        top_margin_pct (float): Percentage of font size for the top margin. Default is 0.1.
        bottom_margin_pct (float): Percentage of font size for the bottom margin. Default is 0.3.
        left_margin_pct (float): Percentage of font size for the left margin. Default is 0.1.
        right_margin_pct (float): Percentage of font size for the right margin. Default is 0.1.
        background_opacity (int): Opacity of the background color (0-255). Default is 200.

    Returns:
        Image: A Pillow Image object with the caption.
    """
    # Detect language of the input text
    language = detect_language(text)

    logging.info('Creating captioned image with text: "%s" (Detected language: %s)', text, language)

    # Create a temporary white background image
    temp_image = Image.new('RGBA', (400, 200), (255, 255, 255, 255))  # Initial size with white background
    draw = ImageDraw.Draw(temp_image)

    # Load a TrueType font with the specified size
    try:
        if language == 'ja':  # If Japanese is detected
            font_path = 'NotoSansJP-Regular.ttf'  # Replace with your Japanese font path
        else:
            font_path = 'arial.ttf'  # Replace with your standard font path
            
        font = ImageFont.truetype(font_path, font_size)
        logging.info('Loaded font: %s at size: %d', font_path, font_size)
    except IOError:
        logging.warning("TTF font not found, using default font.")
        font = ImageFont.load_default()

    # Calculate the bounding box of the text
    bbox = draw.textbbox((0, 0), text, font=font)
    text_width = bbox[2] - bbox[0]
    text_height = bbox[3] - bbox[1]

    # Calculate the margin sizes based on font size and percentages
    top_margin = int(font_size * top_margin_pct)
    bottom_margin = int(font_size * bottom_margin_pct)
    left_margin = int(font_size * left_margin_pct)
    right_margin = int(font_size * right_margin_pct)

    # Calculate the size of the final image including margins
    final_width = text_width + left_margin + right_margin
    final_height = text_height + top_margin + bottom_margin

    # Create the final image with the size of the text box plus margins
    image = Image.new('RGBA', (final_width, final_height), (255, 255, 255, 0))  # Transparent background
    draw = ImageDraw.Draw(image)

    # Draw a semi-transparent background rectangle behind the text
    background_color = (255, 255, 255, background_opacity)  # White background with specified opacity
    draw.rectangle(
        [0, 0, final_width, final_height],
        fill=background_color
    )

    # Calculate position to draw the text considering the margins
    position = (left_margin, top_margin)  # Offset by respective margins
    draw.text(position, text, fill='red', font=font)

    logging.info('Captioned image created successfully with dimensions: %dx%d', final_width, final_height)
    return image

if __name__ == '__main__':
    # Configure logging
    log_filename = os.path.splitext(os.path.basename(__file__))[0] + '.log'
    logging.basicConfig(
        level=logging.INFO,
        format='%(asctime)s - %(levelname)s - %(message)s',
        handlers=[
            logging.FileHandler(log_filename),  # Log to file
            logging.StreamHandler()  # Log to console
        ]
    )

    # Example usage
    captioned_image = create_captioned_image('好きなだけ')  # Example Japanese text
    captioned_image.show()  # To display the image
    # captioned_image.save('captioned_image.png')  # To save the image

# Image Translation and Captioning Application

This application captures screenshots or retrieves images from the clipboard, extracts Japanese text from these images, translates it, and overlays captions onto the original image. It uses various modules for image handling, text extraction, translation, and display.

## Table of Contents

- [Features](#features)
- [Technologies Used](#technologies-used)
- [Setup Instructions](#setup-instructions)
- [Usage](#usage)
- [Functions](#functions)
- [Logging](#logging)
- [Todo](#TODO)

## Features

- Capture screenshots of specified areas.
- Retrieve images from the clipboard.
- Extract Japanese text from images.
- Translate extracted text to English.
- Overlay translated captions on the original images.
- Copy the processed images back to the clipboard.

## Technologies Used

- **Python**: Programming language used to develop the application.
- **Pillow**: For image manipulation.
- **pywin32**: For clipboard operations on Windows.
- **Custom Modules**: 
  - `extract_image_text`: For extracting text from images.
  - `text_translator`: For translating text.
  - `caption_maker`: For creating captioned images.
  - `overlay_caption_on_image`: For overlaying captions on images.
  - `window_creator`: For displaying images in a window.
  - `screenshot_clicker`: For capturing screenshots.

## Setup Instructions

1. **Clone the repository**:
   ```bash
   git clone <repository_url>
   cd <repository_directory>
   ```

2. **Install the required packages**:
   ```bash
   pip install Pillow pywin32
   ```

3. **Set up your logging configuration**:
   - The application logs messages to the console and a file named `app.log`. Ensure that you have write permissions in the working directory.

## Usage

To run the application, you can uncomment specific sections in the `if __name__ == "__main__":` block at the bottom of the code.

### Examples:

1. **Live Translation**: 
   - Uncomment the `screen_maker` function call with desired coordinates to start capturing and processing screenshots.
   ```python
   screen_maker((66, 1490, 76, 694))
   ```

2. **Single Image Translation**: 
   - Uncomment the lines to open a single image, process it, and display the result.
   ```python
   img = Image.open('1.jpg')
   result = mid_process(img)
   result.show()
   ```

3. **Translate Image from Clipboard**:
   - Uncomment the lines to get an image from the clipboard, process it, and copy the result back to the clipboard.
   ```python
   img = get_image_from_clipboard()
   result = mid_process(img)
   copy_image_to_clipboard(result)
   result.show()
   ```

## Functions

### `mid_process(img: Image.Image) -> Image.Image`
Extracts Japanese text from the input image, translates it, and creates captioned images. Returns the image with overlaid captions.

### `screen_maker(coords: tuple) -> None`
Captures a screenshot from specified coordinates, processes the image, and displays it in a window.

### `copy_image_to_clipboard(image: Image.Image)`
Copies a Pillow Image object to the clipboard without saving it locally.

### `get_image_from_clipboard() -> Image.Image`
Retrieves an image from the clipboard and returns it as a Pillow Image object.

## Logging

The application uses Python's built-in `logging` library to log messages at different levels (INFO, WARNING, ERROR). Console logs display messages of INFO level and higher, while logs in `app.log` include WARNING and ERROR messages. 



## TODO:
   -  make the screenshot maker and window make accept coordinates as percentage of screen rather than absolute points.
   - When user starts typing , minimize the tk window , and when no typing is detected for a interval , click a screenshot and put its translation out 
   - Make a python script whuch could dry run all the rest of the scripts and debug them if needed
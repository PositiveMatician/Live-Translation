import easyocr
from PIL import Image
import numpy as np
import cv2  # Optional: For displaying images if needed
import os


def extract_japanese_text(image: Image.Image) -> list:
    """
    Extract Japanese text from a given Pillow image.

    Args:
        image (Image.Image): The image from which to extract text.

    Returns:
        list: A list of dictionaries containing detected text,
              coordinates (x1, x2, y1, y2), and confidence.
    """
    # Convert the Pillow image to a NumPy array
    image_np = np.array(image)

    # Create a reader for Japanese
    reader = easyocr.Reader(['ja'])  # You can specify multiple languages here, e.g., ['ja', 'en']

    # Read the text from the image
    results = reader.readtext(image_np)

    # Collecting extracted text and coordinates in x1, x2, y1, y2 format
    extracted_text = []
    for (bbox, text, prob) in results:
        # Convert coordinates from list of points to x1, x2, y1, y2
        x_coordinates = [point[0] for point in bbox]
        y_coordinates = [point[1] for point in bbox]

        x1 = min(x_coordinates)
        x2 = max(x_coordinates)
        y1 = min(y_coordinates)
        y2 = max(y_coordinates)

        extracted_text.append({
            'text': text,
            'coordinates': {
                'x1': int(x1),
                'x2': int(x2),
                'y1': int(y1),
                'y2': int(y2)
            },
            'confidence': float(prob)
        })

    print(f"Extracted {len(extracted_text)} text items from the image.")
    return extracted_text

def display_image_with_boxes(image: Image.Image, results: list):
    """
    Display the image with bounding boxes drawn around detected text.

    Args:
        image (Image.Image): The image to display.
        results (list): The list of results containing detected text and coordinates.
    """
    # Convert the Pillow image to a NumPy array for OpenCV
    image_np = np.array(image)

    for result in results:
        bbox = result['coordinates']
        # Draw bounding box
        cv2.rectangle(image_np, 
                      (bbox['x1'], bbox['y1']), 
                      (bbox['x2'], bbox['y2']), 
                      color=(0, 255, 0), 
                      thickness=2)
        # Put the text above the bounding box
        cv2.putText(image_np, result['text'], 
                    (bbox['x1'], bbox['y1'] - 10), 
                    cv2.FONT_HERSHEY_SIMPLEX, 
                    0.5, 
                    (0, 255, 0), 
                    1, 
                    cv2.LINE_AA)

    # Show the image
    cv2.imshow('Detected Text', image_np)
    cv2.waitKey(0)
    cv2.destroyAllWindows()

if __name__ == '__main__':



    # Example usage:
    img_path = '1.jpg'  # Replace with your image path
    img = Image.open(img_path)  # Open the image using Pillow
    extracted_results = extract_japanese_text(img)

    print(f"Extracted results: {extracted_results}")
    for result in extracted_results:
        print(f"Detected text: {result['text']} with confidence {result['confidence']:.2f}")
        print(f"Bounding box: x1={result['coordinates']['x1']}, x2={result['coordinates']['x2']}, y1={result['coordinates']['y1']}, y2={result['coordinates']['y2']}")

    # Optionally display the image with bounding boxes
    display_image_with_boxes(img, extracted_results)

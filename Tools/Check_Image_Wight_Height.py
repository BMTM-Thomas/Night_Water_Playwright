import pytesseract
from PIL import Image
import cv2

# Load the image
image = cv2.imread('./image/v_code.png')

# Convert image to RGB (Pillow uses RGB)
image_rgb = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)

# Run OCR and get bounding box data
data = pytesseract.image_to_data(image_rgb, output_type=pytesseract.Output.DICT)

# Iterate through all detected text elements
for i in range(len(data['text'])):
    if int(data['conf'][i]) > 0:  # Filter out low-confidence results
        x = data['left'][i]
        y = data['top'][i]
        w = data['width'][i]
        h = data['height'][i]
        text = data['text'][i]
        print(f"Text: {text}, x: {x}, y: {y}, width: {w}, height: {h}")

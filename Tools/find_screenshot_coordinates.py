import pytesseract
from PIL import Image
import cv2
import pyautogui

# Load the image
image = cv2.imread('/Users/n02-19/Desktop/demo5.png')

print(pyautogui.locateOnScreen(image))


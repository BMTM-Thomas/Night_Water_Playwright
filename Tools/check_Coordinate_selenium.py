import pyautogui
import time

while True:
    time.sleep(2)
    position = pyautogui.position()
    print(position)
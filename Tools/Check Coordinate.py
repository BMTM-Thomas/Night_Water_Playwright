import pyautogui
import time

while True:
    time.sleep(2)
    x = pyautogui.position()
    print(x)
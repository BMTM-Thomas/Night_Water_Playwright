import pyautogui
import time

while True:
    time.sleep(2)
    position = pyautogui.position()
    print(f"Point(x={position.x +10}, y={position.y +150})") # Adjusting the coordinates by adding 10 to both x and y
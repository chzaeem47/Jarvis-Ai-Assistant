import time
import pyautogui

print("Get ready! Move your mouse and hold it over the WhatsApp Audio Call icon...")
for i in range(5, 0, -1):
    print(f"{i}...")
    time.sleep(1)

# Grab where your cursor is currently pointing
x, y = pyautogui.position()
print("\n" + "="*40)
print(f"🎯 SUCCESS! The current coordinates are: X = {x}, Y = {y}")
print("="*40)
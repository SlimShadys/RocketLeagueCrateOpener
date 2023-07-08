import datetime

import cv2
import keyboard
import numpy as np
import pyautogui

def checkButtons(okTemplate, equipNowTemplate, threshold):
    # - Capture the screen using pyautogui
    # - Convert the captured image to a format compatible with OpenCV
    # - RGB to BGR
    screenshot = cv2.cvtColor(np.array(pyautogui.screenshot()), cv2.COLOR_RGB2GRAY)

    # Perform template matching
    ok_result = cv2.matchTemplate(screenshot, okTemplate, cv2.TM_CCOEFF_NORMED)
    equip_result = cv2.matchTemplate(screenshot, equipNowTemplate, cv2.TM_CCOEFF_NORMED)

    # Check if the "Ok" / "Equip now" button is found in the screenshot
    ok_screen_present = cv2.minMaxLoc(ok_result)[1] > threshold
    equip_screen_present = cv2.minMaxLoc(equip_result)[1] > threshold

    # Determine the type of screen based on the presence of the template images
    if ok_screen_present and equip_screen_present:
        return (1443, 1296) # Both 'Ok' and 'Equip now' screens are present.
    elif ok_screen_present:
        return (1443, 1296) # Only 'Ok' screen is present.
    elif equip_screen_present:
        return (1443, 1296) # Only 'Equip now' screen is present.
    else:
        print(F"{add_timestamp()}: No matching buttons for this screen. Maybe crates are finished?")
        return (0, 0)

def add_timestamp():
    return datetime.datetime.now().strftime("[%H:%M:%S]")

def checkKeyThread(stop_event):
    while True:
        if keyboard.is_pressed('F4'):
            stop_event.set()  # Set the event to inform other threads to stop
            print(F"{add_timestamp()}: Pressed F4! Stop event triggered.")
            break
        if stop_event.is_set():
            break

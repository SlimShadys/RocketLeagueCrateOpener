import datetime

import cv2
import keyboard
import numpy as np
import pyautogui
import locale

def getLanguage(lang) -> str:
    if lang:
        language_mapping = {code: name.split('.')[0] for code, name in locale.locale_alias.items()}
        filtered_codes = [code for name, code in language_mapping.items() if name.lower().startswith(lang.lower())]
        
        if len(filtered_codes) < 1:
            print("You set an invalid default language preference. Exiting.")
            exit(0)
        elif len(filtered_codes) > 1:
            print(f"Multiple language codes detected for '{lang}'.")
            while True:
                response = input(f"Choose one between {list(set(filtered_codes))}: ")
                if response in filtered_codes:
                    return response
                print("You chose an invalid code. Try again.")
        else:
            return filtered_codes[0]            
    
    default_language = locale.getdefaultlocale()[0]
    print(f"Your language is set as: {default_language}")
    response = input("Press '1' for correct, otherwise write your preferred language (e.g. 'English'): ")

    if response == "1":
        return default_language
    else:
        return getLanguage(lang=response)

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
        screen_type = "both 'Ok' and 'Equip now'"
        coords = (1458, 1320)
    elif ok_screen_present:
        screen_type = "only 'Ok'"
        coords = (1267, 1320)
    elif equip_screen_present:
        screen_type = "only 'Equip now'"
        coords = (1458, 1320)
    else:
        print(F"{add_timestamp()}: No 'Equip now' and/or 'Ok' screen. Maybe crates are finished?")
        coords = (0, 0)
    
    print(F"{add_timestamp()}: Opened crate with {screen_type} screen.")
    return coords

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

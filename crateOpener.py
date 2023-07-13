# -----------------------------------------------------------
# Automatic script for opening crates in Rocket League
#
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in all
# copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
# SOFTWARE.
#
# Released under MIT License
#
# (C) 2023 | Gianmarco Scarano, Rome, Italy
# Email: gianmarcoscarano@gmail.com
# -----------------------------------------------------------

import os
import sys
import threading
import time

import cv2
import pyautogui
import pygetwindow as gw

from utils import add_timestamp, checkButtons, checkKeyThread, getLanguage

def mainThread(ratioX, ratioY) -> None:
    # -------------------- List of commands for opening a crate --------------------
    #             selectCrate,  openCrate,  confirmOpening, confirmItem
    listCommands = [[133, 371], [274, 1218], [1135, 811], [0, 0]]

    # We loop for all windows starting with "Rocket League" and we check if the Window title starts with "Rocket League (" 
    # since the default window is called: "Rocket League (64-bit, DX11, Cooked)"
    # We could've directly passed the above string to the getWindowsWithTitle() function, but I don't know if
    # there is still a 32-Bit version of Rocket League floating around.
    # Also, we check if the window is active, meaning that the user is inside the game's window.
    print(F"{add_timestamp()}: Waiting for Rocket League screen...")
    while not any(win.title.startswith("Rocket League (") and win.isActive for win in gw.getWindowsWithTitle("Rocket League")):
        if stop_event.is_set(): # Always check if the stop_event (F4) is called.
            sys.exit(0)
        time.sleep(0.2) # Sleep for 0.2ms before checking again

    # Rocket League screen has been opened and is active
    print(F"{add_timestamp()}: Rocket League opened!")

    # Assuming user is at the "Rewards" item list
    # Until the user does not trigger the mouse to a corner of the screen or press F4, let's loop the rewards
    while True:
        for idx, pos in enumerate(listCommands):
             # If we are in the "confirmItem" command, let's sleep for 7.5 seconds (due to crate animation)
            if(idx == len(listCommands) - 1):
                time.sleep(durationCrateAnimation)
                pos = checkButtons(okTemplate, equipNowTemplate, threshold, ratioX, ratioY)
                if(pos[0] == 0):
                    stop_event.set()

            if (stop_event.is_set()): # Always check if the stop_event (F4) is called.
                print(F"{add_timestamp()}: -- Exiting now from main loop --")
                sys.exit(0)

            pyautogui.moveTo(pos[0]/ratioX, pos[1]/ratioY, duration=durationMouseMovement)
            pyautogui.click(x=pos[0]/ratioX, y=pos[1]/ratioY, clicks=1, interval=0, button='left', duration=durationMouseClick)

        pyautogui.press('esc', interval=0.1)
        time.sleep(0.2)

# ----- ACTUAL MAIN LOOP ----- #
if __name__ == '__main__':

    screenWidth, screenHeight = pyautogui.size() # Get the size of the primary monitor.

    ratioX = 2560 / screenWidth
    ratioY = 1440 / screenHeight

    print(F"{add_timestamp()}: Operating on a screen with following resolution: {screenWidth}x{screenHeight}")
    print(F"{add_timestamp()}: Ratio is: {ratioX}")

    # ======================= #
    #         A R G S         #
    # ======================= #
    lang = None                     # Example: 'English' / 'Italian' / 'French' etc.
    code = None                     # Example: 'en_US' / 'en_GB' / 'en_EN'
    threshold = 0.85                # Set a threshold value for template matching results (Now accepting only values => 0.86)
    durationMouseClick = 0.02       # Duration (in seconds) for mouse click. Default = 0.02 (Almost instant. We set it 0.02 for avoiding crashes)
    durationMouseMovement = 0.0     # Duration (in seconds) for mouse movement. Default = 0.0 (Instant)
    durationCrateAnimation = 7.5    # Duration (in seconds) for crate animation. Estimated around 7.5
    # ======================= #

    # If there is a 'code' available, then directly load that file instead of asking the language to the user
    if code != None:
        preferred_language = code
        file_path = f'buttons/EquipNow-{code}.png'
    else:
        preferred_language = getLanguage(lang) 
        file_path = f'buttons/EquipNow-{preferred_language}.png'

    print("-------------------------------------")
    if not os.path.isfile(file_path):
        print(f"{add_timestamp()}: File '{file_path}' not found.\nMost probably the 'Equip now' image for your language has not been implemented yet.\nContact the developer or send a PR with the 'Equip now' button in your language. Check 'buttons' folder for examples.")
        exit(0)
    else:
        print(F"{add_timestamp()}: Language correctly set as: {preferred_language}")

    # Load the template images for "Ok" and "Equip now" buttons
    okTemplate = cv2.imread(os.path.join('buttons', "Ok.png"), cv2.IMREAD_GRAYSCALE)
    equipNowTemplate = cv2.imread(os.path.join('buttons', f'EquipNow-{preferred_language}.png'), cv2.IMREAD_GRAYSCALE)

    # Let's resize the templates with the ratio w.r.t to user screen.
    # This is crucial, due to the fact that OpenCV needs to match the templates,
    # but fails if the buttons are larger/smaller than the buttons in the screenshot.
    okTemplate = cv2.resize(okTemplate, (int(okTemplate.shape[1]/ratioY), int(okTemplate.shape[0]/ratioX)))
    equipNowTemplate = cv2.resize(equipNowTemplate, (int(equipNowTemplate.shape[1]/ratioY), int(equipNowTemplate.shape[0]/ratioX)))
    print(F"{add_timestamp()}: Correctly resized the templates following your screen resolution.") 

    stop_event = threading.Event() # Stop event Thread

    # Create and start the main thread
    mainThread = threading.Thread(target=mainThread(ratioX, ratioY))
    mainThread.start()

    # Create and start the key checking thread
    checkKeyThread = threading.Thread(target=checkKeyThread(stop_event))
    checkKeyThread.start()

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

import datetime
import sys
import threading
import time

import keyboard
import pyautogui
import pygetwindow as gw

stop_event = threading.Event()

def add_timestamp():
    return datetime.datetime.now().strftime("[%H:%M:%S]")

def check_key_thread():
    while True:
        if keyboard.is_pressed('F4'):
            stop_event.set()  # Set the event to inform other threads to stop
            print(F"{add_timestamp()}: Pressed F4! Stop event triggered.")
            break

def main_thread():
    screenWidth, screenHeight = pyautogui.size() # Get the size of the primary monitor.

    ratioX = 2560 / screenWidth
    ratioY = 1440 / screenHeight

    print(F"{add_timestamp()}: Operating on a screen with following resolution: {screenWidth}x{screenHeight}")
    print(F"{add_timestamp()}: Ratio is: {ratioX}")

    # List of commands for opening a crate.
    # ----------------------
    # Some items, when unpacked, have the "Equip now" button along with "Ok".
    # In "confirmItem", 1434 on the X-axis should be the value for pressing 
    # the "Ok" button (in case we have only the "Ok" button) and for pressing
    # the same "Ok" button, in case we have the "Equip now" and "Ok" screen.
    # To be tested
    # ----------------------
    '''            selectCrate,  openCrate, confirmOpening, confirmItem'''
    listCommands = [[133, 371], [274, 1218], [1135, 811], [1443, 1296]]
    durationMove = 0.0 # Duration for moving mouse. Default = 0.0 (Instant)

    # We loop for all windows starting with "Rocket League" and we check if the Window title starts with "Rocket League (" 
    # since the default window is called: "Rocket League (64-bit, DX11, Cooked)"
    # We could've directly passed the above string to the getWindowsWithTitle() function, but I don't know if
    # there is still a 32-Bit version of Rocket League floating around.
    # Also, we check if the window is active, meaning that the user is inside the game's window.
    print(F"{add_timestamp()}: Waiting for Rocket League screen...")
    while not any(win.title.startswith("Rocket League (") and win.isActive == True for win in gw.getWindowsWithTitle("Rocket League")):
        if stop_event.is_set(): # Always check if the stop_event (F4) is called.
            sys.exit(0)
        time.sleep(0.2) # Sleep for 0.2ms before checking again

    # Rocket League screen has been opened and is active
    print(F"{add_timestamp()}: Rocket League opened!")

    # Assuming user is at the "Rewards" item list
    # Until the user does not trigger the mouse to a corner of the screen or press F4, let's loop the rewards
    while True:
        for idx, pos in enumerate(listCommands):
            if stop_event.is_set(): # Always check if the stop_event (F4) is called.
                print(F"{add_timestamp()}: Exiting now from main loop.")
                sys.exit(0)
             # If we are in the "confirmItem" command, let's switch the mouse movement from 0.0 seconds (instant) to 5.5 (due to crate animation)
            durationMove = 5.5 if idx == len(listCommands)-1 else 0.0
            pyautogui.moveTo(pos[0]/ratioX, pos[1]/ratioY, duration=durationMove)
            pyautogui.click(x=pos[0]/ratioX, y=pos[1]/ratioY, clicks=1, interval=0, button='left', duration=0.05)

        pyautogui.press('esc', interval=0.1)
        time.sleep(0.2)

# Create and start the main thread
main_thread = threading.Thread(target=main_thread)
main_thread.start()

# Create and start the key checking thread
check_key_thread = threading.Thread(target=check_key_thread)
check_key_thread.start()

# Wait for the main thread to complete
main_thread.join()

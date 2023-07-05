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

import pyautogui
import time

screenWidth, screenHeight = pyautogui.size() # Get the size of the primary monitor.

print(F"Operating on a screen with following resolution: {screenWidth}x{screenHeight}")
print(F"Ratio is: {2560 / screenWidth}")

ratioX = 2560 / screenWidth
ratioY = 1440 / screenHeight

selectCrate = [133, 371]
openCrate = [274, 1218]
confirmOpening = [1135, 811]
confirmItem = [1455, 1315] # To be checked. Maybe some items have "Equip now" along with "Ok"

# Assuming user is at the "Rewards" item list
# Until the user does not trigger the mouse to a corner of the screen, let's loop the rewards
while(True):
    # 133 x 371 -> Select crate
    pyautogui.moveTo(selectCrate[0]/ratioX, selectCrate[1]/ratioY, duration=0)  # Move mouse towards the first crate to open
    pyautogui.click(x=selectCrate[0]/ratioX, y=selectCrate[1]/ratioY, clicks=1, interval=0, button='left', duration=0.1)

    # 274 x 1218 -> Position over "Open Crate" and click it
    pyautogui.moveTo(openCrate[0]/ratioX, openCrate[1]/ratioY, duration=0)
    pyautogui.click(x=openCrate[0]/ratioX, y=openCrate[1]/ratioY, clicks=1, interval=0, button='left', duration=0.1)

    # 1135 x 811 -> Confirm the "Open Crate" and click
    pyautogui.moveTo(confirmOpening[0]/ratioX, confirmOpening[1]/ratioY, duration=0)
    pyautogui.click(x=confirmOpening[0]/ratioX, y=confirmOpening[1]/ratioY, clicks=1, interval=0, button='left', duration=0.1)

    # 1455 x 1315 -> Confirm the item received
    pyautogui.moveTo(confirmItem[0]/ratioX, confirmItem[1]/ratioY, duration=5.0) # Let's wait 5 seconds for the animation
    pyautogui.click(x=confirmItem[0]/ratioX, y=confirmItem[1]/ratioY, clicks=1, interval=0, button='left', duration=0.1)

    # Need to go back to item list -> Press 'Esc'
    pyautogui.press('esc', interval=0.1)
    time.sleep(0.3) # Let's sleep 0.3ms
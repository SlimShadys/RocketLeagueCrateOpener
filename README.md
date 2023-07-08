# RocketLeagueCrateOpener
This Python script automatically opens crates for you without the need to push/click buttons here and there, since there is no skip animation for the unpacking phase.

---
<p align="center">
  <img title="Test" src="media/Test.gif" align="center" width="700">
</p>

---

## Installation
In order to run the script, make sure to meet the following library requirement:
- pyautogui
- pygetwindow
- keyboard

You can install it through:
```
pip install -U pyautogui pygetwindow keyboard
```

## Usage
- Place yourself in the Crate items list (_where all the crates are present_).<br>
- Then, start the program by: ```python crateOpener.py```. The program will wait for you to switch back to the Rocket League screen in order to run the actual loop.<br>
- The loop will run until you either press F4 (_recommended_) or quickly move your mouse to the top-left corner.

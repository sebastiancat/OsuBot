import time

import pywinauto
from pywinauto import Application
import mouseInput
from mouseInput import click_position_osu

import levelDataExtractor
from levelDataExtractor import extractLineData, extractMapData
def print_hi(name):
    # Use a breakpoint in the code line below to debug your script.
    print(f'Hi, {name}')  # Press Ctrl+F8 to toggle the breakpoint.

def testing():
    file = open("Test/Toby Fox - BIG SHOT (Sylas) [ADVANCED].osu", 'r')
    print(len("asdasdaas"))
    print(extractLineData("96,122,13739,6,0,L|187:107,1,75,6|10,1:2|0:0,0:0:0:0:"))
    print()
    print(extractMapData(file))

    # Launch osu!
    osuPath = r"C:\Users\cortn\AppData\Local\osulazer\current\osu!.exe"
    #app = Application("win32").start(osuPath, 15, 5, True)
    time.sleep(10)
    click_position_osu(512/2,384/2)

# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    testing()

import time

import pywinauto
# from pywinauto import Application
import mouseInput
from mouseInput import click_position_osu, make_bezier

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
    # time.sleep(10)
    # click_position_osu(512/2,384/2)
    mouseInput.click_drag_linear(0,0,500,500,time.time(), 5)

def startup():
    file = open("Test/Toby Fox - BIG SHOT (Sylas) [ADVANCED].osu", 'r')
    data = extractMapData(file)


    startTime = time.time()

    return data, startTime


# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    testing()

    data, startTime = startup()


    # Main loop
    print("Starting Loop")
    print("Start Time: " + str(startTime))
    print("Time: " + str(time.time()))
    while True:

        # Popping the object from the queue
        hitObject = data.pop()
        print(hitObject)

        # Time calculations (should prevent drifting)
        objTime = float(hitObject[3]) / 1000
        currentTime = time.time() - startTime

        # Snake is eepy...
        print("Current Time: " + str(currentTime))
        time.sleep((objTime - currentTime))


        x = hitObject[1]
        y = hitObject[2]

        # Various Typing
        if hitObject[0] == 1:
            mouseInput.click_position_osu(x, y)
import pywinauto
import pywinauto.mouse
from screeninfo import get_monitors

#Click a position in screen coordinates
def click_position(x,y):
    pywinauto.mouse.click('left', (x,y))

# Click a position in osu! coordinates
def click_position_osu(x,y):
    #Assume osu! is running fullscreen
    monitor = get_monitors()[0]
    playfieldSize = (round(monitor.height * 0.8 * (4/3)), round(monitor.height * 0.8))
    osuScale = (playfieldSize[0]/512, playfieldSize[1]/384)
    monitorCenter = (monitor.width/2, monitor.height/2)
    playfieldOrgin = (monitorCenter[0] - playfieldSize[0]/2, monitorCenter[1] - playfieldSize[1]/2)
    osuCoordinates = ((playfieldOrgin[0] + x * osuScale[0]), (playfieldOrgin[1] + y * osuScale[1]))
    print(osuCoordinates)
    click_position(int(osuCoordinates[0]), int(osuCoordinates[1]))


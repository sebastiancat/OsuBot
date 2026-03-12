import pywinauto
import pywinauto.mouse
import time
from screeninfo import get_monitors

#Click a position in screen coordinates
def click_position(x,y):
    pywinauto.mouse.click('left', (x,y))

# Click a position in osu! coordinates
def click_position_osu(x,y):
    #Assume osu! is running fullscreen
    osuCoordinates = convert_to_osu_pixels(x,y)
    click_position(int(osuCoordinates[0]), int(osuCoordinates[1]))

def convert_to_osu_pixels (x,y):
    monitor = get_monitors()[0]
    playfieldSize = (round(monitor.height * 0.8 * (4 / 3)), round(monitor.height * 0.8))
    osuScale = (playfieldSize[0] / 512, playfieldSize[1] / 384)
    monitorCenter = (monitor.width / 2, monitor.height / 2)
    playfieldOrgin = (monitorCenter[0] - playfieldSize[0] / 2, monitorCenter[1] - playfieldSize[1] / 2)
    return (playfieldOrgin[0] + x * osuScale[0]), (playfieldOrgin[1] + y * osuScale[1])

def click_drag_linear (startX,startY, endX, endY, startTimeSeconds, timeToCompletionSeconds):
    start = convert_to_osu_pixels(startX,startY)
    end = convert_to_osu_pixels(endX,endY)
    pywinauto.mouse.press('left', start)
    while time.time() - startTimeSeconds  < timeToCompletionSeconds:
        timeElapsed = time.time() - startTimeSeconds
        pywinauto.mouse.move((timeElapsed * start[0] + (1-timeElapsed) * end[0], timeElapsed * start[1] + (1-timeElapsed) * end[1]))

    pywinauto.mouse.release('left')
    return 0

def click_drag_circle (x,y, revolutions, timeToCompletionSeconds):
    return 1

def click_drag_curve (controlPoints, speed):
    curve = make_bezier(controlPoints)
    for thing in range(0,len(controlPoints)):
        print(curve[thing])
    return 1

# Source - https://stackoverflow.com/a/2292690
# Posted by unutbu, modified by community. See post 'Timeline' for change history
# Retrieved 2026-03-12, License - CC BY-SA 4.0

def make_bezier(xys):
    # xys should be a sequence of 2-tuples (Bezier control points)
    n = len(xys)
    combinations = pascal_row(n-1)
    def bezier(ts):
        # This uses the generalized formula for bezier curves
        # http://en.wikipedia.org/wiki/B%C3%A9zier_curve#Generalization
        result = []
        for t in ts:
            tpowers = (t**i for i in range(n))
            upowers = reversed([(1-t)**i for i in range(n)])
            coefs = [c*a*b for c, a, b in zip(combinations, tpowers, upowers)]
            result.append(
                tuple(sum([coef*p for coef, p in zip(coefs, ps)]) for ps in zip(*xys)))
        return result
    return bezier

def pascal_row(n, memo={}):
    # This returns the nth row of Pascal's Triangle
    if n in memo:
        return memo[n]
    result = [1]
    x, numerator = 1, n
    for denominator in range(1, n//2+1):
        # print(numerator,denominator,x)
        x *= numerator
        x /= denominator
        result.append(x)
        numerator -= 1
    if n&1 == 0:
        # n is even
        result.extend(reversed(result[:-1]))
    else:
        result.extend(reversed(result))
    memo[n] = result
    return result
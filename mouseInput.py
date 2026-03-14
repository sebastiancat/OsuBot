import pyautogui
import time
from screeninfo import get_monitors
import math

osuScale = (1,1)
playfieldOrigin = (1,1)
#Click a position in screen coordinates
def mouseSetup():
    monitor = get_monitors()[0]
    playfieldSize = (round(monitor.height * 0.8 * (4 / 3)), round(monitor.height * 0.8))
    global osuScale
    osuScale= (playfieldSize[0] / 512, playfieldSize[1] / 384)
    monitorCenter = (monitor.width / 2, monitor.height / 2)
    global playfieldOrigin
    playfieldOrigin= (monitorCenter[0] - playfieldSize[0] / 2, monitorCenter[1] - playfieldSize[1] / 2)

# Click a position in osu! coordinates
def click_position_osu(x,y):
    #Assume osu! is running fullscreen
    osuCoordinates = convert_from_osu_pixels(x, y)
    pyautogui.moveTo(osuCoordinates[0], osuCoordinates[1])
    pyautogui.click()

# Take an input in osu! pixels and return screen pixels
def convert_from_osu_pixels (x, y):
    return int(playfieldOrigin[0] + x * osuScale[0]), int(playfieldOrigin[1] + y * osuScale[1])

def click_drag_linear (startX,startY, endX, endY, travelRepetitions, startTimeSeconds, timeToCompletionSeconds):
    start = convert_from_osu_pixels(startX, startY)
    end = convert_from_osu_pixels(endX, endY)
    pyautogui.mouseDown(startX,startY)

    while time.time() - startTimeSeconds  < timeToCompletionSeconds:
        timeElapsed = time.time() - startTimeSeconds
        percentComplete = timeElapsed/timeToCompletionSeconds
        pyautogui.moveTo((int(percentComplete* end[0] + (1-percentComplete) * start[0]), int(percentComplete * end[1] + (1-percentComplete) * start[1])))

    pyautogui.mouseUp()
    return 0

def click_drag_circle (p1, p2, p3, travelRepititions, timeToCompleteSeconds):
    # radius, center = circleRadiusAndCenter(p1, p2, p3)
    #
    # distAC = p3 - p1
    # distAB = p2 - p1
    #
    # if distAC[0] > 0:
    #     if distAB[0] > 0:
    #         direction = 1
    #     else:
    #         direction = -1
    # else:
    #     if distAB[0] > 0:
    #         direction = 1
    #     else:
    #         direction = -1
    #
    #
    # angle = 0
    # x = radius * math.cos(angle) + center[0] * direction
    # x = radius * math.sin(angle) + center[1] * direction
    #
    return 1

#Control points as an array
def click_drag_curve (controlPoints, startTime, timeToCompleteSeconds):
    curve = make_bezier(controlPoints)
    pyautogui.moveTo(controlPoints[0])
    pyautogui.mouseDown()
    while time.time() - startTime < timeToCompleteSeconds:
        timeElapsed = time.time() - startTime
        percentComplete = timeElapsed/timeToCompleteSeconds
        targetPosition = curve([percentComplete])
        print("Target: " + str(targetPosition))
        pyautogui.move((int(targetPosition[0][0]), int(targetPosition[0][1])))

    pyautogui.mouseUp()
    return 0

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


def circleRadiusAndCenter(b, c, d):
    temp = c[0]**2 + c[1]**2
    bc = (b[0]**2 + b[1]**2 - temp) / 2
    cd = (temp - d[0]**2 - d[1]**2) / 2
    det = (b[0] - c[0]) * (c[1] - d[1]) - (c[0] - d[0]) * (b[1] - c[1])

    if abs(det) < 1.0e-10:
        return None

    # Center of circle
    cx = (bc*(c[1] - d[1]) - cd*(b[1] - c[1])) / det
    cy = ((b[0] - c[0]) * cd - (c[0] - d[0]) * bc) / det

    radius = ((cx - b[0])**2 + (cy - b[1])**2)**.5

    return radius, (cy, cy)
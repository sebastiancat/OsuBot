import math
import time
import keyboard
import mouseInput
# from mouseInput import click_position_osu, make_bezier, click_drag_linear, click_drag_curve

import levelDataExtractor
from levelDataExtractor import extractLineData, extractMapData

def testing():
    file = open("Test/Toby Fox - BIG SHOT (Sylas) [ADVANCED].osu", 'r')

    # Launch osu!
    # time.sleep(10)
    # click_position_osu(512/2,384/2)
    bezier = mouseInput.make_bezier([(1, 2), (2, 3)])
    #mouseInput.click_drag_linear(0,0,10,10,0,time.time(), 5)

def startup():
    mouseInput.mouseSetup()
    file = open("Test/Testing - Testing (Guest) [Linear curves].osu", 'r')
    global SliderMultiplier
    data, timeData, SliderMultiplier = extractMapData(file)
    # TODO: Properly start (waiting for z needs root access on linux)
    keyboard.wait('z')

    startTime = time.time()

    return data, startTime, timeData

def calculateBezierCurves(curveCoordinatesLocal):
    curvesLocal = [[(0.0, 0.0)]]
    curveIndex = 0
    firstPoint = True
    for i in range(len(curveCoordinatesLocal)):
        if firstPoint:
            curvesLocal[0][0] = (float(curveCoordinatesLocal[i][0]), float(curveCoordinatesLocal[i][1]))
            firstPoint = False
            continue

        if curveCoordinatesLocal[i] == curveCoordinatesLocal[i - 1]:

            curvesLocal.append([(float(curveCoordinatesLocal[i][0]), float(curveCoordinates[i][1]))])
            curveIndex += 1
        else:
            print("Curves Local")
            curvesLocal[curveIndex].append((float(curveCoordinatesLocal[i][0]), float(curveCoordinatesLocal[i][1])))

    print("Local curves" + str(curvesLocal))
    return curvesLocal


def getCurveControlPoints():
    curveCoordinates = []
    curvePairs = hitObject[4][2:].split('|')
    curvePairs.insert(0, str(x) + ":" + str(y))
    for i in range(len(curvePairs)):
        controlX, controlY = curvePairs[i].split(':')
        curveCoordinates.append((int(controlX), int(controlY)))
    return curveCoordinates

if __name__ == '__main__':
    testing()
    SliderMultiplier = 1

    data, startTime, timeData = startup()


    # Main loop
    print("Starting Loop")
    print("Start Time: " + str(startTime))
    print("Time: " + str(time.time()))
    # Intended jank
    timeObject = timeData.pop()

    while True:

        # Popping the object from the queue

        hitObject = data.pop()
        nextHitObject = False
        # print(hitObject)
        nextTimeObject = False
        # print("Next Time Object: " + str(timeObject))

        # Time calculations (should prevent drifting)
        objTime = float(hitObject[3]) / 1000
        timeTime = float(timeObject[0]) / 1000
        currentTime = time.time() - startTime

        # if timeTime > currentTime:
        #
        # Snake is eepy...
        if objTime - currentTime > 0:
            time.sleep((objTime - currentTime))
        #time.sleep(0.5)

        print("Object time " + str(objTime) + ", currentTime " + str(currentTime))
        x = hitObject[1]
        y = hitObject[2]

        # Various Typing
        if hitObject[0] == 1:
            mouseInput.click_position_osu(x, y)
        elif hitObject[0] == 2:
            print(hitObject[4])

            # Retrieve the curve's control points
            curveCoordinates = getCurveControlPoints()

            # TODO: Actual values
            timingSliderMultiplier = 1

            beatLength = timeObject[1]
            sliderLength = float(hitObject[6])

            sliderTime =  sliderLength / (SliderMultiplier * 100 * timingSliderMultiplier) * beatLength / 1000

            if hitObject[4][0] == 'L':
                for x in range(0, len(curveCoordinates) - 1):
                    sliderLength = int(math.sqrt((curveCoordinates[x][0] - curveCoordinates[x+1][0])**2 + (curveCoordinates[x][1]- curveCoordinates[x+1][1])**2))
                    sliderTime = sliderLength / (SliderMultiplier * 100 * timingSliderMultiplier) * beatLength / 1000
                    mouseInput.click_drag_linear(curveCoordinates[x], curveCoordinates[x+1], int(float(hitObject[5])), x==len(curveCoordinates)-2, time.time(), sliderTime)

            elif hitObject[4][0] == 'P':
                mouseInput.click_drag_curve([(curveCoordinates[0][0], curveCoordinates[0][1]), (curveCoordinates[1][0], curveCoordinates[1][1]), (curveCoordinates[2][0], curveCoordinates[2][1])], time.time(), sliderTime)

            elif hitObject[4][0] == 'B':
                curves = calculateBezierCurves(curveCoordinates)
                print("From Curve: " + str(curves))
                for curve in curves:
                    print("Extracted: " + str(curve))
                    startX, startY = curveCoordinates[0]
                    endX, endY = curveCoordinates[1]

                    finalDistance = 0
                    for ctlPt in curveCoordinates[1:]:
                        finalDistance += math.hypot(curveCoordinates[0][0] - curveCoordinates[1][0], curveCoordinates[0][1] - curveCoordinates[1][1])

                    timeToCompletionSeconds = finalDistance / math.hypot(endX - startX, endY - startY) * sliderTime


                    mouseInput.click_drag_curve(curve, time.time(), timeToCompletionSeconds)


                print("Bezier curve")


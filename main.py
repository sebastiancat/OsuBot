import time
import keyboard
import pywinauto
from pywinauto import Application
import mouseInput
from mouseInput import click_position_osu, make_bezier, click_drag_linear, click_drag_curve

import levelDataExtractor
from levelDataExtractor import extractLineData, extractMapData

def testing():
    file = open("Test/Toby Fox - BIG SHOT (Sylas) [ADVANCED].osu", 'r')

    # Launch osu!
    # time.sleep(10)
    # click_position_osu(512/2,384/2)
    bezier = make_bezier([(1,2),(2,3)])
    #mouseInput.click_drag_linear(0,0,10,10,0,time.time(), 5)

def startup():
    mouseInput.mouseSetup()
    file = open("Test/Kry.exe - Rift Walker (Ryuusei Aika) [Easy].osu", 'r')
    data, timeData, SliderMultiplier = extractMapData(file)

    keyboard.wait('z')

    startTime = time.time()

    return data, startTime, timeData

def calculateBezierCurves(curveCoordinatesLocal):
    curvesLocal = [[(0, 0)]]
    curveIndex = 0
    firstPoint = True
    for i in range(len(curveCoordinatesLocal)):
        if firstPoint:
            curvesLocal[0][0] = curveCoordinatesLocal[i]
            firstPoint = False
            continue

        if curveCoordinatesLocal[i] == curveCoordinatesLocal[i - 1]:
            curvesLocal.append([curveCoordinatesLocal[i]])
            curveIndex += 1
        else:
            curvesLocal[curveIndex].append(curveCoordinatesLocal[i])

    #TODO: Convert returns from strings to floats
    return curvesLocal


# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    testing()

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
        # if objTime <= currentTime:
        #     print("Object time " + str(objTime) + ", currentTime " + str(currentTime))
        #     print("How the hell did we get here")
        #     continue

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
            curvePairs = hitObject[4][2:].split('|')
            curvePairs.insert(0, str(x) + ":" + str(y))
            curveCoordinates = []
            for i in range(len(curvePairs)):
                print("Raw control point " + str(curvePairs[i]))
                controlX, controlY = curvePairs[i].split(':')
                curveCoordinates.append((controlX,controlY))


            # curvePairs = hitObject[4][2:]
            # print(curvePairs)
            #
            #
            # curveCoordinates = [(x, y)]
            # seps = levelDataExtractor.findAllOccurrences(curvePairs[1:], "|")
            #
            # This loop didn't seem to be running
            # for i in range(1, len(seps)):
            #     rawControlPoint = curvePairs[seps[i-1]+1:seps[i]]
            #     print("Raw Control Point: " + rawControlPoint)
            #     controlX, controlY = (rawControlPoint.split(":"))
            #     curveCoordinates.append((int(controlX), int(controlY)))

            # TODO: Actual values
            sliderMultiplier = 1
            timingSliderMultiplier = 1
            beatLength = 0.1
            sliderLength = float(hitObject[6])

            sliderTime =  sliderLength / (sliderMultiplier * 100 * timingSliderMultiplier) * beatLength / 1000

            if hitObject[4][0] == 'L':
                print("Linear curve")
                for x in range(0, len(curvePairs) - 1):
                    # Shouldn't the startTime use the actual start time variable?
                    # You mean the one in the hitObject? -Remy
                    click_drag_linear(float(curveCoordinates[x][0]), float(curveCoordinates[x][1]), float(curveCoordinates[x + 1][0]), float(curveCoordinates[x + 1][1]), 0, time.time(), sliderTime)
            elif hitObject[4][0] == 'P':
                print("Circular curve")
            elif hitObject[4][0] == 'B':
                curves = calculateBezierCurves(curveCoordinates)
                print("From Curve: " + str(curves))
                for curve in curves:
                    print("Extracted: " + str(curve))
                    #TODO: Actual values
                    #click_drag_curve(curve, ..., ...)


                print("Bezier curve")


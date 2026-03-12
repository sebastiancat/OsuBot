import collections

# Main Function
def extractMapData(file):
    # Getting the start of the hitobjects
    lines = file.readlines()
    dataStart = getLinePosition(lines, "[HitObjects]")
    timingStart = getLinePosition(lines, "[TimingPoints]")

    # This is stupid.
    SliderMultiplier = float(lines[getLinePosition(lines, "SliderMultiplier:")]["SliderMultiplier:".__len__():])


    hitObjects = collections.deque()
    timeObjects = collections.deque()

    dataEnd = len(lines)
    for linePos in range(dataStart+1, dataEnd):
        hitObject = extractLineData(lines[linePos])
        hitObjects.appendleft(hitObject)

    linePos = timingStart + 1
    while len(lines[linePos]) > 1:
        timeObject = extractTimeData(lines[linePos])
        timeObjects.appendleft(timeObject)
        linePos += 1
    print(SliderMultiplier)
    return hitObjects, timeObjects, SliderMultiplier

# Function to get the line starting with [HitObjects]
def getLinePosition(lines, target):
    # print(lines)
    # Iterating over the lines
    targetFirstLetter = target[0]
    i = 0
    for line in lines:
        if line[0] == targetFirstLetter:
            # print(line)
            if line.__contains__(target):
                return i
        i += 1
    raise ValueError("No HitObjects declaration found!")


# Function to export the important data from a single line to a tuple.
def extractLineData(line):
    i = 0
    sep = findAllOccurrences(line, ',')

    x = int(line[:sep[0]])
    y = int(line[sep[0]+1:sep[1]])
    time = int(line[sep[1]+1:sep[2]])
    bitType = int(line[sep[2]+1:sep[3]])

    # print(bitType)

    # Testing the bitmap


    if bitType & (2**0):
        return 1, x, y, time
    if bitType & 2**1:
        curveData = line[sep[4]+1:sep[5]]
        slides = line[sep[5]+1:sep[6]]
        return 2, x, y, time, curveData, slides
    if bitType & 2**3:
        endTime = line[sep[4]+1:sep[5]]
        return 3, x, y, time, endTime
    raise ValueError("Could not determine object type!")

def extractTimeData(line):
    i = 0
    sep = findAllOccurrences(line, ',')
    print("Line: " +line)

    time = int(line[:sep[0]])
    beatLength = float(line[sep[0]+1:sep[1]])
    return time, beatLength






def findAllOccurrences(string, char):
    # A variable for the position of the commas
    seperatorPositions = []
    stringCopy = string
    # Tracking the progression as we remove areas behind the current focus
    lineProgress = 0
    while True:
        sepPos = stringCopy.find(char)
        if sepPos == -1:
            break
        seperatorPositions.append(lineProgress + sepPos)
        lineProgress += sepPos + 1
        stringCopy = stringCopy[sepPos + 1:]
        # print(stringCopy)
        # print(sepPos)
    return seperatorPositions


def loopUntilChar(string, char):
    returnString = ""
    i = 0
    while string[i] != char:
        returnString += string[i]
        i += 1
    return returnString, i

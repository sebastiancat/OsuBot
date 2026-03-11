import collections

# Main Function
def extractMapData(file):
    # Getting the start of the hitobjects
    lines = file.readlines()
    dataStart = getStartOfHitObjects(lines)


    hitObjects = collections.deque()

    dataEnd = len(lines)
    for linePos in range(dataStart+1, dataEnd):
        hitObject = extractLineData(lines[linePos])
        hitObjects.appendleft(hitObject)
    print(hitObjects)

# Function to get the line starting with [HitObjects]
def getStartOfHitObjects(lines):
    # print(lines)
    # Iterating over the lines
    i = 0
    for line in lines:
        if line[0] == '[':
            # print(line)
            if line.__contains__("[HitObjects]"):
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
    type = int(line[sep[2]+1:sep[3]])

    # print(type)

    # Testing the bitmap
    if type & (2**0):
        return x, y, time
    if type & 2**1:
        print("Slider")
        return "TEST"
    if type & 2**3:
        print("Spinner")
        return "TEST"
    raise ValueError("Could not determine object type!")









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

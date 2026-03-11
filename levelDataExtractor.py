from gc import freeze
from os.path import devnull

# Function to get the line starting with [HitObjects]
def getStartOfHitObjects(file):
    # Opening the file
    lines = file.readlines()
    # print(lines)
    # Iterating over the lines
    i = 0
    for line in lines:
        if line[0] == '[':
            # print(line)
            if line.__contains__("[HitObjects]"):
                return i
        i += 1
    raise ValueError("No HitObjects declaration found in: " + file + "! File is probably misspelled or missing!")

def loopUntilChar(string, char):
    returnString = ""
    i = 0
    while string[i] != char:
        returnString += string[i]
        i += 1
    return returnString, i

# Function to export the important data from a single line to a tuple.
def extractLineData(line):
    i = 0
    sep = findAllOccurrences(line, ',')

    x = int(line[:sep[0]])
    y = int(line[sep[0]+1:sep[1]])
    time = int(line[sep[1]+1:sep[2]])
    type = int(line[sep[2]+1:sep[3]])



    print(type)
    # Testing the bitmap
    if type & (2**0):
        return x, y, time
    elif type & 2**1:
        print("Slider")
    elif type & 2**3:
        print("Spinner")



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
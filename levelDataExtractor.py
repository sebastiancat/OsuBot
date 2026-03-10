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
    raise ValueError("No HitObjects declaration found in: " + filename + "! File is probably misspelled or missing!")
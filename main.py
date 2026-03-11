# This is a sample Python script.

import levelDataExtractor
from levelDataExtractor import extractLineData


# Press Shift+F10 to execute it or replace it with your code.
# Press Double Shift to search everywhere for classes, files, tool windows, actions, and settings.

# A function dedicated to any testing.
def testing():
    file = open("Test/Toby Fox - BIG SHOT (Sylas) [ADVANCED].osu", 'r')
    print(levelDataExtractor.getStartOfHitObjects(file))

    print(extractLineData("100,100,12600,6,1,B|200:200|250:200|250:200|300:150,2,310.123,2|1|2,0:0|0:0|0:2,0:0:0:0:"))


# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    testing()

# See PyCharm help at https://www.jetbrains.com/help/pycharm/

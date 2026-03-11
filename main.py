# This is a sample Python script.

import levelDataExtractor
from levelDataExtractor import extractLineData, extractMapData


# Press Shift+F10 to execute it or replace it with your code.
# Press Double Shift to search everywhere for classes, files, tool windows, actions, and settings.

# A function dedicated to any testing.
def testing():
    file = open("Test/Toby Fox - BIG SHOT (Sylas) [ADVANCED].osu", 'r')
    print(len("asdasdaas"))
    print(extractLineData("96,122,13739,6,0,L|187:107,1,75,6|10,1:2|0:0,0:0:0:0:"))
    print()
    print(extractMapData(file))


# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    testing()

# See PyCharm help at https://www.jetbrains.com/help/pycharm/

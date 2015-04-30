__author__ = 'Jerry', 'Ivy'
import time
import datetime
import copy

from datetime import timedelta

gazeCoordinates = []
puzzleCoordinates = []
staredPictures=[]
clickHistory = []
gazeIndex=0 ;puzzleIndex=0;
# reads the gaze file and store x and y coordinates into the gazeCoordinate variable.
# Does not read the received data.
def readGazeFile():
    gazeFile = open('ReleaseGazeData.csv', 'r')
    for line in gazeFile:
        line = line.split(",")
        # print(type(line))
        if (line.__len__() >= 8 and line[3].isdigit() and line[5].isdigit() and line[2] == " X: "):
            gazeCoordinates.append([datetime.datetime.strptime(line[7], "%Y-%m-%d %H:%M:%S.%f\n"), int(line[3]), int(line[5])])
    return gazeCoordinates


def readPuzzleFile():
    puzzleFile = open('gameStateData.csv', 'r')
    for line in puzzleFile:
        line = line.split(",")
        for i in range(1, len(line)):
            line[i] = line[i].replace(" ", "")
        currentTime = datetime.datetime.strptime(line[0], "%Y-%m-%d %H:%M:%S.%f")
        if (line.__len__() >= 8 and line[4].isdigit() and line[5].isdigit()):
            if (len(puzzleCoordinates) == 0):
                status = [currentTime, [currentTime, int(line[4]), int(line[5]), line[6]]]
            else:
                status = puzzleCoordinates[-1]
                status[0] = currentTime
                pieces = [s[3] for s in status[1:]]
                if line[6] in pieces:
                    i = pieces.index(line[6]) + 1
                    status[i] = [currentTime, int(line[4]), int(line[5]), line[6]]
                else:
                    status.append([currentTime, int(line[4]), int(line[5]), line[6]])
            puzzleCoordinates.append(copy.deepcopy(status))
        elif (line[4] == 'Touch Down'):
            clickHistory.append([line[6], currentTime])
        elif (line[4] == 'Touch Up'):
            for ch in clickHistory:
                if (ch[0] == line[6] and len(ch) == 2):
                    ch.append(currentTime)
        # click history
        elif (line[2][:6] == 'Stage '):
            puzzleCoordinates.append([])
    return puzzleCoordinates


def isStaring(gazeData, puzzleData):
    for puzzle in puzzleData[1:]:
        ###NEED CHANGE. CHANGE 100
        if(abs(gazeData[1]-puzzle[1])<=100 and abs(gazeData[2]-puzzle[2])<=100):
            print(puzzle[3])
            staredPictures.append([gazeData[0],puzzle[1],puzzle[2],puzzle[3]])
            return True
            #return puzzleData[3]
    return False

def findStaring():
    gazeIndex=0
    puzzleIndex=0
    while (gazeIndex<len(gazeCoordinates) and puzzleIndex<len(puzzleCoordinates)):
        if (len(gazeCoordinates)<=0 or len(puzzleCoordinates)<=0 or
                    gazeIndex>=len(gazeCoordinates) or puzzleIndex>=len(puzzleCoordinates)):
            return
        elif(gazeCoordinates[gazeIndex][0]<puzzleCoordinates[puzzleIndex][0]):
            #we need the gaze's time to be later than the time that puzzle shows up/get updated
            gazeIndex+=1
        elif(puzzleIndex<len(puzzleCoordinates)-1 and
                     gazeCoordinates[gazeIndex][0]>puzzleCoordinates[puzzleIndex+1][0]):
            #if the gaze surpases the next timestamp when puzzle got updated, move on to the next puzzle status.
            puzzleIndex+=1
        else:
            isStaring(gazeCoordinates[gazeIndex],puzzleCoordinates[puzzleIndex])
            gazeIndex+=1
    resultFile = open('result.csv', 'w')
    for line in staredPictures:
        resultFile.write(str(line[0])+','+str(line[1])+','+str(line[2])+','+str(line[3])+','+'\n')


readGazeFile()
readPuzzleFile()

findStaring()

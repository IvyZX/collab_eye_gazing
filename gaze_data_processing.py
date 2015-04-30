__author__ = 'Jerry', 'Ivy'
# The goal for this program is to
# 1. Check when people are moving pieces.
# 2. If they are moving pieces, whether they are looking at the pieces they're moving or their partner is moving.
# 3. Input: Gaze data in ReleaseGazeData.csv and puzzle data in gameStateData.csv.
# 4. Output: A csv file that have: time, which pieces they are moving (two pieces), are they staring at their own piece?
# Are they staring at their partner's piece?
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


def isStaring(gazeData, puzzleData, clickData):
    accuracy=50 # Only counts as looking at a piece when the coordinates are within a range of 50
    for puzzle in puzzleData[1:]:
        ###NEED CHANGE. CHANGE 100
        if(puzzle[3]==clickData[3] and abs(gazeData[1]-puzzle[1])<=accuracy and abs(gazeData[2]-puzzle[2])<=accuracy):
            print(puzzle[3])
            staredPictures.append([gazeData[0],clickData[4],clickData[5],clickData[2],clickData[3],True,False])
            return True
        elif(puzzle[3]==clickData[4] and abs(gazeData[1]-puzzle[1])<=accuracy and abs(gazeData[2]-puzzle[2])<=accuracy):
            print(puzzle[3])
            staredPictures.append([gazeData[0],clickData[4],clickData[5],clickData[2],clickData[3],False,True])
            return True
            #return puzzleData[3]
    return False

def findStaring():
    if len(gazeCoordinates)<=0 or len(puzzleCoordinates)<=0 or len(clickHistory)<=0:
        return
    staredPictures.append(["time","A's ID","B's ID","A Clicks","B Clicks", "Looking at A's piece","Looking at B's piece"])
    gazeIndex=0
    puzzleIndex=0
    historyIndex=0
    while (gazeIndex<len(gazeCoordinates) and puzzleIndex<len(puzzleCoordinates) and historyIndex<len(clickHistory)):
        # If anything goes out of range, return.
        if (gazeIndex>=len(gazeCoordinates) or puzzleIndex>=len(puzzleCoordinates) or historyIndex>=len(clickHistory)):
            return
        # move the puzzle coordinates to the time when participants click the puzzles
        elif(puzzleCoordinates[puzzleIndex][0]<clickHistory[historyIndex][0]):
            puzzleIndex+=1
        # move the history index to next click history when participants stopped clicking.
        elif(puzzleCoordinates[puzzleIndex][0]>clickHistory[historyIndex][1]):
            historyIndex+=1
        elif(gazeCoordinates[gazeIndex][0]<puzzleCoordinates[puzzleIndex][0]):
            #we need the gaze's time to be later than the time that puzzle shows up/get updated
            gazeIndex+=1
        elif(puzzleIndex<len(puzzleCoordinates)-1 and
                     gazeCoordinates[gazeIndex][0]>puzzleCoordinates[puzzleIndex+1][0]):
            #if the gaze surpases the next timestamp when puzzle got updated, move on to the next puzzle status.
            puzzleIndex+=1
        else:
            isStaring(gazeCoordinates[gazeIndex],puzzleCoordinates[puzzleIndex],clickHistory[historyIndex])
            gazeIndex+=1
    resultFile = open('result.csv', 'w')
    for line in staredPictures:
        resultFile.write(str(line[0])+','+str(line[1])+','+str(line[2])+','+str(line[3])+','+str(line[4])+','+str(line[5])+','+str(line[6])+'\n')


readGazeFile()
readPuzzleFile()

findStaring()

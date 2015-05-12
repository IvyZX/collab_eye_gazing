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
import re

from datetime import timedelta

# global vars

gazeCoordinates = []
# list of [time, x, y]

puzzleCoordinates = []
# list of [time, [last_move_time, x, y, piece_name] ...]

staredPictures=[]
# list of [time, x, y, piece_time]

clickHistory = []
# list of [start_time, end_time, piece_clicked_by_A, piece_clicked_by_B]


gazeIndex=0 ;puzzleIndex=0;

dateTimeFiles=['041410','041412','041416','041610','041611','042111','042117','043011','043013','043014','050510','050514','050711']

# reads the gaze file and store x and y coordinates into the gazeCoordinate variable.
# Does not read the received data.
def readGazeFile():
    gazeFile = open('0512 data in seperate files\\ReleaseGazeData041410.csv', 'r')
    for line in gazeFile:
        line = line.replace("\n", "")
        line = line.split(",")
        # print(type(line))
        if (line.__len__() >= 8 and line[3].isdigit() and line[5].isdigit() and line[2] == " X: "):
            gazeCoordinates.append([datetime.datetime.strptime(line[7], "%Y-%m-%d %H:%M:%S.%f"), int(line[3]), int(line[5])])
    return gazeCoordinates


def readPuzzleFile():
    puzzleFile = open('0512 data in seperate files\\GameStateData041410.csv', 'r')
    current_clicks = {}
    for line in puzzleFile:
        line = line.split(",")
        for i in range(1, len(line)):
            line[i] = line[i].replace(" ", "")
            line[i] = line[i].replace("\n", "")
        if line.__len__() >= 8:
            if not (line[0] == 'time' or line[0] == ''):
                currentTime = datetime.datetime.strptime(line[0], "%Y-%m-%d %H:%M:%S.%f")
            if ( line[4].isdigit() and line[5].isdigit()):
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
            elif (line[1][:5] == 'Stage'):
                puzzleCoordinates.append([])
            elif (line[4] == 'TouchDown'):
                #print current_clicks
                current_clicks[line[7]] = line[6]
                start_time = currentTime
            elif (line[4] == 'TouchUp'):
                #print current_clicks
                keys = current_clicks.keys()
                if len(keys) >= 2:
                    clickHistory.append([start_time, currentTime, current_clicks[keys[0]], current_clicks[keys[1]],
                                         keys[0], keys[1]])
                current_clicks.pop(line[7])
    return




def isStaring(gazeData, puzzleData, clickData):
    accuracy=55 # Only counts as looking at a piece when the coordinates are within a range of 50
    for puzzle in puzzleData[1:]:
        if(puzzle[3]==clickData[2] and abs(gazeData[1]-puzzle[1])<=accuracy and abs(gazeData[2]-puzzle[2])<=accuracy):
            #print(puzzle[3])
            staredPictures.append([gazeData[0],clickData[4],clickData[5],clickData[2],clickData[3],True,False])
            return True
        elif(puzzle[3]==clickData[3] and abs(gazeData[1]-puzzle[1])<=accuracy and abs(gazeData[2]-puzzle[2])<=accuracy):
            #print(puzzle[3])
            staredPictures.append([gazeData[0],clickData[4],clickData[5],clickData[2],clickData[3],False,True])
            return True
            #return puzzleData[3]
    staredPictures.append([gazeData[0],clickData[4],clickData[5],clickData[2],clickData[3],False,False])
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
    resultFile.close()

    # Write the accuracy data.
    resultFile=open('accuracy.csv','w')
    resultFile.write('A\'s ID,B\'s ID,Puzzle Name,Accuracy\n')
    counter=0
    positives=0
    currentPuzzle=''
    currentAName=''
    currentBName=''
    print staredPictures
    for line in staredPictures[1:]:
        if  (currentAName!=str(line[1]) or currentBName!=str(line[2]) or currentPuzzle!=str(re.match('(\w+\d+)(?:_)',str(line[3])).group(1))):
            if (counter!=0):
                resultFile.write(currentAName+','+currentBName+','+currentPuzzle+','+str(float(positives)/counter)+'\n')
            currentAName=str(line[1])
            currentBName=str(line[2])
            currentPuzzle=str(re.match('(\w+\d*)(?:_)',str(line[3])).group(1))
            print currentPuzzle
            counter=0
            positives=0
        if line[5]==True or line[6]==True:
            positives+=1
        counter+=1
    if (counter!=0):
        resultFile.write(currentAName+','+currentBName+','+currentPuzzle+','+str(float(positives)/counter)+'\n')


readGazeFile()
readPuzzleFile()
#print gazeCoordinates
print puzzleCoordinates
print staredPictures
print clickHistory
findStaring()

# print clickHistory

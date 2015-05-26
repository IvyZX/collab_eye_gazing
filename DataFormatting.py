__author__ = 'Jerry'

# This python script is to convert the Demographic survey, the Condition Orders, and the global data into
# a human-readable data format

import csv
import datetime

# feel free to change these file names
demographic_file_name = 'Subject Demographic Survey 4.29.15.csv'
cond_orders_file_name = 'ConditionOrders.csv'
global_data_file_name = 'globalData.csv'
output_file_name = 'test.csv'

# records the data of these files
demographicData = []
conditionOrderData = []
globalData = []
outputData = []
outputString = 'Subject Pair ID,Pair ID,Participant ID,Condition,Condition Order,Trial,Difficulty,Image Set,' \
               'Image Number,Image ID,Time,Score,Gender Pair,Ethnicity,Age,Gender,English,Spatial Score,Gaze Accuracy,Pronouns'

# Demography file has the following information:
# Subject pair 0->0,Pair ID 1->1, Participant ID 2->2
# Gender Pair 3->12, Gender 4->15, Age 5->14,
# Ethnicity 6->13, English 7->16

with open(demographic_file_name, 'rU')  as demographic_file:
    demographic_reader = csv.reader(demographic_file)
    for line in demographic_reader:
        demographicData.append(line)


# Condition Order File has the following information:
# Pair ID 0->1, Condition 1,2,3: 3,4,5->3,4, Image set order-> 8,10
with open(cond_orders_file_name, 'rU')  as cond_order_file:
    cond_order_reader = csv.reader(cond_order_file)
    for line in cond_order_reader:
        conditionOrderData.append(line)

# global Data file has the following information:
# Image set 1->7, Image Number 2->8, Subject Pair 3->0, Time 0,4->10
# Score 5->11
with open(global_data_file_name, 'rU')  as global_file:
    global_reader = csv.reader(global_file)
    for line in global_reader:
        globalData.append(line)
    for k in range(0, len(globalData)):
        for i in range(1, len(globalData[k])):
            globalData[k][i] = globalData[k][i].replace(' ', '')
        if globalData[k][3] == 'null':
            duration = datetime.datetime.strptime(globalData[k][0],
                                                  " %Y-%m-%d %H:%M:%S.%f") - datetime.datetime.strptime(
                globalData[k - 1][0], " %Y-%m-%d %H:%M:%S.%f")
            if duration <= datetime.timedelta(0, 0, 0, 0, 20):
                globalData[k][3] = globalData[k - 1][3]

    for k in range(len(globalData) - 1, 0, -1):
        if globalData[k][3] == 'null':
            if (datetime.datetime.strptime(globalData[k + 1][0], " %Y-%m-%d %H:%M:%S.%f") - datetime.datetime.strptime(
                    globalData[k][0], " %Y-%m-%d %H:%M:%S.%f")) <= datetime.timedelta(0, 0, 0, 0, 20):
                globalData[k][3] = globalData[k + 1][3]

#print demographicData
#print conditionOrderData
#print globalData

# take the filled datas and summarize them together into the outputData
for i in range(1, len(demographicData), 2):
    for condLine in conditionOrderData:
        if condLine[0] == demographicData[i][1]:
            for j in range(0, 12):
                if j % 4 < 2:
                    difficulty = 'Easy'
                else:
                    difficulty = 'Hard'
                imageSetOrder = [int(condLine[2][0]), int(condLine[2][1]), int(condLine[2][2])]
                imageID = []
                for temp in imageSetOrder:
                    imageID.append(1 + (temp - 1) * 4)
                duration = None
                score = None
                for k in range(0, len(globalData) - 1):
                    if demographicData[i][0] == globalData[k][3] and globalData[k][4] == 'start' and (
                            globalData[k + 1][4] == 'end' or globalData[k + 1][4] == 'FINISHEDTRIAL') and imageSetOrder[
                                j / 4] == int(globalData[k][1]) and j % 4 == int(globalData[k][2]):
                        duration = datetime.datetime.strptime(globalData[k + 1][0],
                                                              " %Y-%m-%d %H:%M:%S.%f") - datetime.datetime.strptime(
                            globalData[k][0], " %Y-%m-%d %H:%M:%S.%f")
                        if duration <= datetime.timedelta(0, 10):
                            duration = None
                        else:
                            score = globalData[k + 1][5]
                outputData.append(
                    [demographicData[i][0], demographicData[i][1], demographicData[i][2], condLine[3 + j / 4],
                     j / 4 + 1, j + 1, difficulty,
                     imageSetOrder[j / 4], j % 4, imageID[j / 4] + j % 4, duration, score, demographicData[i][3],
                     demographicData[i][6], demographicData[i][5], demographicData[i][4], demographicData[i][7]])
                outputData.append([demographicData[i + 1][0], demographicData[i + 1][1], demographicData[i + 1][2],
                                   condLine[3 + j / 4], j / 4 + 1, j + 1, difficulty,
                                   imageSetOrder[j / 4], j % 4, imageID[j / 4] + j % 4, duration, score,
                                   demographicData[i + 1][3], demographicData[i + 1][6], demographicData[i + 1][5],
                                   demographicData[i + 1][4], demographicData[i + 1][7]])

#print outputData

# writhe the outputData into the csv file
with open(output_file_name, 'w')  as output_file:
    output_file.write(outputString + '\n')
    for line in outputData:
        for item in line:
            output_file.write(str(item) + ',')
        output_file.write('\n')
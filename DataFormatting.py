__author__ = 'Jerry'

# This python script is to convert the Demographic survey, the Condition Orders, and the global data into the data
# format that Sarah wants.

import csv

demographic_file_name='Subject Demographic Survey 4.29.15.csv'
cond_orders_file_name='ConditionOrders.csv'
global_data_file_name='globalData.csv'
outputData=[]
outputString=['Subject Pair ID,Pair ID,Participant ID,Condition,Condition Order,Trial,Difficulty,Image Set,Image Number,Image ID,Time,Score,Gender Pair,Ethnicity,Age,Gender,English,Spatial Score,Gaze Accuracy,Pronouns']

# Demography file has the following information:
# Subject pair 0->0,Pair ID 1->1, Participant ID 2->2
# Gender Pair 3->12, Gender 4->15, Age 5->14,
# Ethnicity 6->13, English 7->16

with open (demographic_file_name,'rb')  as demographic_file:
    demographic_reader=csv.reader(demographic_file)
    for line in demographic_reader:

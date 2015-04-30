__author__ = 'Jerry', 'Ivy'
import time
import datetime
import copy
import pygtk
from datetime import timedelta

staredPictures=[]

def readResultFile():
    gazeFile = open('result.csv', 'r')
    for line in gazeFile:
        line = line.split(",")
        # print(type(line))
        if (line.__len__() >= 4 and line[1].isdigit() and line[2].isdigit()):
            staredPictures.append([datetime.datetime.strptime(line[0], "%Y-%m-%d %H:%M:%S.%f"), int(line[1]), int(line[2]),line[3]])
    pass

def replay():
    now=datetime.datetime.now()
    startTime=datetime.datetime.now()
    iterator1=staredPictures[0][0]
    iterator2=staredPictures[0][0]
    x=0;y=0

    for i in range(0,staredPictures.__len__()):
        iterator2=staredPictures[i][0]
        if iterator1==iterator2:
            x=staredPictures[i][1]
            y=staredPictures[i][2]
            print "at " + str(iterator2) + " X= " + str(x) + " Y= "+str(y)
        else:
            time.sleep((iterator2-iterator1).total_seconds())
            iterator1=iterator2
            x=staredPictures[i][1]
            y=staredPictures[i][2]
            print "at " + str(iterator2) + " X= " + str(x) + " Y= "+str(y)


readResultFile()
#print (staredPictures)
replay()
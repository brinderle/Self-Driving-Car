import pandas as pd
import math
import collections
import numpy as np

# function to calculate the distance between two points, each one is a list with two items inside
def distance(p0, p1):
    # need to convert to floats here because the values are stored as strings
    dist = math.sqrt((float(p0[0]) - float(p1[0]))**2 + (float(p0[1]) - float(p1[1]))**2)
    return dist

# this function was taken directly from https://stackoverflow.com/questions/42258637/how-to-know-the-angle-between-two-points
# returns the angle from p1 to p2 in the counterclockwise direction in degrees
# E is 0, N is 90, W is 180, S is 270
def angle_between(p0, p1):
    myradians = math.atan2(float(p1[1]) - float(p0[1]), float(p1[0]) - float(p0[0]))
    mydegrees = math.degrees(myradians)
    # turn negative angles into positive angles so we have consistency
    if mydegrees < 0:
        mydegrees = 360 + mydegrees
    return mydegrees

# loaner laptop path
Data1 = pd.read_csv("C:/Users/student/Documents/Brandon/Self-Driving Project/Data02-24_13-56.csv")
Data2 = pd.read_csv("C:/Users/student/Documents/Brandon/Self-Driving Project/Data02-24_14-35.csv")
Data3 = pd.read_csv("C:/Users/student/Documents/Brandon/Self-Driving Project/Data02-25_13-57.csv")
Data4 = pd.read_csv("C:/Users/student/Documents/Brandon/Self-Driving Project/Data02-25_14-01.csv")
Data5 = pd.read_csv("C:/Users/student/Documents/Brandon/Self-Driving Project/Data02-25_14-29.csv")
Data6 = pd.read_csv("C:/Users/student/Documents/Brandon/Self-Driving Project/Data02-25_16-49.csv")
Data7 = pd.read_csv("C:/Users/student/Documents/Brandon/Self-Driving Project/Data02-25_17-36.csv")
Data8 = pd.read_csv("C:/Users/student/Documents/Brandon/Self-Driving Project/Data02-27_11-23.csv")
Data9 = pd.read_csv("C:/Users/student/Documents/Brandon/Self-Driving Project/Data02-27_16-36.csv")
# normal laptop path
#Data1 = pd.read_csv("C:/Users/student/Documents/CS4630/Self-Driving Project/Data02-25_14-01.csv")

Data = [Data1, Data2, Data3, Data4, Data5, Data6, Data7, Data8, Data9]

# this declares an ordered dictionary that will hold the stops, need order so we can compare the adjacent stops
stops = collections.OrderedDict()

# this is a list of lists of coordinate pairs for the stops, can be used for the database
stopCoordinateList = []

for dataSet in Data:

    DataSubset = dataSet.iloc[:,[1,5,6,7,8,21,22]]
    # maybe add rotation column
    DataSubset.columns = ["sampleNum", "latitude", "longitude", "altitude", "speed", "accelerationX", "accelerationY"]


    # the data points I get back from the low speed and positive acceleration seem good other than parking lots
    # reason for positive acceleration to identify is you have to speed back up after a stop
    for i in range(len(DataSubset)):
        speed = DataSubset.iloc[i,4]
        latitude = DataSubset.iloc[i,1]
        longitude = DataSubset.iloc[i,2]
        accelY = DataSubset.iloc[i,6]
        direction = 0
        minDirection = 0
        maxDirection = 0


        # check if speed is less than 3 m/s and then something about accelerationY
        # also need to allow for one latitude with multiple longitudes, which is why values for dictionary keys are lists
        if speed < 3 and accelY > .1 and latitude not in stops:
            stops[str(latitude)] = [longitude]
            if i > 20:
                direction = angle_between([latitude, longitude], [DataSubset.iloc[i - 20, 1], DataSubset.iloc[i - 20, 2]])
                maxDirection = direction + 22.5;
                minDirection = direction - 22.5;
                if maxDirection > 360:
                    maxDirection -= 360
                if minDirection < 0:
                    minDirection += 360
            # appending minDirection and maxDirection to account for minor changes in direction
            stopCoordinateList.append([latitude,longitude, direction, minDirection, maxDirection])
        elif speed < 3 and accelY > .1 and latitude in stops:
            stops[str(latitude)] = stops[str(latitude)].append(longitude)
            if i > 20:
                direction = angle_between([latitude, longitude], [DataSubset.iloc[i - 20, 1], DataSubset.iloc[i - 20, 2]])
            stopCoordinateList.append([latitude, longitude, direction, minDirection, maxDirection])



    # Calculate the distance between two points, and if the second stop is within a certain distance of the first
    # stop, delete the first stop from the list of stops, should eliminate some of the overlapping stops
    # deleting the first stop out of the two is better because the last stop is most likely to be right at
    # the intersection which is where the stop actually is

    tooClose = [] # will store the indices of stopCoordinateList where the stops are too close together
    for i in range(len(stopCoordinateList) - 1):
        # I did some calculations between points and .00003 looked to be a reasonable cutoff
        p0Coordinates = [stopCoordinateList[i][0], stopCoordinateList[i][1]]
        p1Coordinates = [stopCoordinateList[i+1][0], stopCoordinateList[i+1][1]]
        p0Direction = stopCoordinateList[i][2]
        p1Direction = stopCoordinateList[i+1][2]
        directionDifference = 0

        # set directionDifference appropriately based on which is greater, if close to 0 or 360
        if p1Direction > p0Direction and p1Direction > 315 and p0Direction < 45:
            directionDifference = p0Direction + 360 - p1Direction
        elif p0Direction > p1Direction and p0Direction > 315 and p1Direction < 45:
            directionDifference = p1Direction + 360 - p0Direction
        elif p1Direction > p0Direction:
            directionDifference = p1Direction - p0Direction
        else: # p0Direction > p1Direction
            directionDifference = p0Direction - p1Direction

        # only say they are too close or bad coordinates if they are within this distance and the car was
        # going the same direction, don't want to eliminate points that are close but going different
        # directions like going through different parts of an intersection
        # giving some room for error of 45 degrees in the directionDifference
        if (distance(p0Coordinates, p1Coordinates) < .00005 and directionDifference < 45):
            tooClose.append(i)

    tooCloseLength = len(tooClose)

# delete the stops that are too close together, need to subtract i in here because of previous indeces deleted
for i in range(tooCloseLength):
    del stopCoordinateList[tooClose[i] - i]

# print the information for the remaining stops after deleting the duplicates that were too close
# only printing the coordinates and direction right now, not min or max direction but they are there
for i in range(len(stopCoordinateList)):
    print(stopCoordinateList[i][0], ", ", stopCoordinateList[i][1], ",", stopCoordinateList[i][2], sep="")
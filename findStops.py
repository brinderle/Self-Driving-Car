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
Data1 = pd.read_csv("C:/Users/student/Documents/Brandon/Self-Driving Project/Data02-25_14-01.csv")
# normal laptop path
#Data1 = pd.read_csv("C:/Users/student/Documents/CS4630/Self-Driving Project/Data02-25_14-01.csv")

Data1Subset = Data1.iloc[:,[1,5,6,7,8,21,22]]
# maybe add rotation column
Data1Subset.columns = ["sampleNum", "latitude", "longitude", "altitude", "speed", "accelerationX", "accelerationY"]

# this declares an ordered dictionary that will hold the stops, need order so we can compare the adjacent stops
stops = collections.OrderedDict()

# this is a list of lists of coordinate pairs for the stops, can be used for the database
stopCoordinateList = []


# the data points I get back from the low speed and positive acceleration seem good other than parking lots
# reason for positive acceleration to identify is you have to speed back up after a stop
for i in range(len(Data1Subset)):
    speed = Data1Subset.iloc[i,4]
    latitude = Data1Subset.iloc[i,1]
    longitude = Data1Subset.iloc[i,2]
    accelY = Data1Subset.iloc[i,6]
    direction = 0
    minDirection = 0
    maxDirection = 0

    # prevAccelY is idea to further check if it is a stop by checking if deceleration was occuring an amount of
    # time before the stop, not implemented right now
    # if i > 100:
    #     prevAccelY = Data1Subset.iloc[i-100,6]
    # else:
    #     prevAccelY = 0

    # check if speed is less than 1.5 m/s (3.36 mph) and then something about accelerationY
    # also need to allow for one latitude with multiple longitudes, which is why values for dictionary keys are lists
    if speed < 3 and accelY > .1 and latitude not in stops:
        stops[str(latitude)] = [longitude]
        if i > 20:
            direction = angle_between([latitude, longitude], [Data1Subset.iloc[i - 20, 1], Data1Subset.iloc[i - 20, 2]])
            maxDirection = direction + 22.5;
            minDirection = direction - 22.5;
            if maxDirection > 360:
                maxDirection -= 360
            if minDirection < 0:
                minDirection += 360
        # appending minDirection and maxDirection to account for minor changes in direction
        stopCoordinateList.append([latitude,longitude, minDirection, maxDirection])
    elif speed < 3 and accelY > .1 and latitude in stops:
        stops[str(latitude)] = stops[str(latitude)].append(longitude)
        if i > 20:
            direction = angle_between([latitude, longitude], [Data1Subset.iloc[i - 20, 1], Data1Subset.iloc[i - 20, 2]])
        stopCoordinateList.append([latitude, longitude, minDirection, maxDirection])


# commented this section out when adding stopCoordinateList append above while adding direction
# for i in stops:
#     # this inner loop goes through each item in the list, which is the dictionary value
#     # this allows for one latitude with multiple longitudes to be treated properly
#     for j in range(len(stops[i])):
#         stopCoordinateList.append([i,stops[i][j]])
#         #print(i, ", ", stops[i][j], sep="")

# Calculate the distance between two points, and if the second stop is within a certain distance of the first
# stop, delete the first stop from the list of stops, should eliminate some of the overlapping stops
# deleting the first stop out of the two is better because the last stop is most likely to be right at
# the intersection which is where the stop actually is

tooClose = [] # will store the indices of stopCoordinateList where the stops are too close together
for i in range(len(stopCoordinateList) - 1):
    # I did some calculations between points and .00003 looked to be a reasonable cutoff
    p0Coordinates = [stopCoordinateList[i][0], stopCoordinateList[i][1]]
    p1Coordinates = [stopCoordinateList[i+1][0], stopCoordinateList[i+1][1]]
    # if (distance(stopCoordinateList[i], stopCoordinateList[i+1]) < .00005):
    if (distance(p0Coordinates, p1Coordinates) < .00005):
        tooClose.append(i)

tooCloseLength = len(tooClose)

# delete the stops that are too close together, need to subtract i in here because of previous indeces deleted
for i in range(tooCloseLength):
    del stopCoordinateList[tooClose[i] - i]

# print the information for the remaining stops after deleting the duplicates that were too close
for i in range(len(stopCoordinateList)):
    print(stopCoordinateList[i][0], ", ", stopCoordinateList[i][1], ",", stopCoordinateList[i][2], ",", stopCoordinateList[i][3], sep="")

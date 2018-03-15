import pandas as pd
import math
import collections

# function to calculate the distance between two points, each one is a list with two items inside
def distance(p0, p1):
    # need to convert to floats here because the values are stored as strings
    dist = math.sqrt((float(p0[0]) - float(p1[0]))**2 + (float(p0[1]) - float(p1[1]))**2)
    return dist

Data1 = pd.read_csv("C:/Users/student/Documents/CS4630/Self-Driving Project/Data02-24_14-35.csv")
Data1Subset = Data1.iloc[:,[1,5,6,7,8,21,22]]
# maybe add rotation column
Data1Subset.columns = ["sampleNum", "latitude", "longitude", "altitude", "speed", "accelerationX", "accelerationY"]

# this declares an ordered dictionary that will hold the stops, need order so we can compare the adjacent stops
stops = collections.OrderedDict()


# can't check for 0 speed because cars don't always go to complete stop at stop sign, but they do at lights

# the data points I get back from the low speed and positive acceleration seem good other than parking lots
# reason for positive acceleration to identify is you have to speed back up after a stop
for i in range(len(Data1Subset)):
    speed = Data1Subset.iloc[i,4]
    latitude = Data1Subset.iloc[i,1]
    longitude = Data1Subset.iloc[i,2]
    accelY = Data1Subset.iloc[i,6]

    # prevAccelY is idea to further check if it is a stop by checking if deceleration was occuring an amount of
    # time before the stop, not implemented right now
    # if i > 100:
    #     prevAccelY = Data1Subset.iloc[i-100,6]
    # else:
    #     prevAccelY = 0

    # check if speed is less than 1.5 m/s (3.36 mph) and then something about accelerationY
    # also need to allow for one latitude with multiple longitudes, which is why values for dictionary keys are lists
    if speed < 2 and accelY > .1 and latitude not in stops:
        stops[str(latitude)] = [longitude]
    elif speed < 2 and accelY > .1 and latitude in stops:
        stops[str(latitude)] = stops[str(latitude)].append(longitude)


# this is a list of lists of coordinate pairs for the stops, can be used for the database
stopCoordinateList = []

for i in stops:
    # this inner loop goes through each item in the list, which is the dictionary value
    # this allows for one latitude with multiple longitudes to be treated properly
    for j in range(len(stops[i])):
        stopCoordinateList.append([i,stops[i][j]])
        #print(i, ", ", stops[i][j], sep="")

# Calculate the distance between two points, and if the second stop is within a certain distance of the first
# stop, delete the first stop from the list of stops, should eliminate some of the overlapping stops
# deleting the first stop out of the two is better because the last stop is most likely to be right at
# the intersection which is where the stop actually is

tooClose = [] # will store the indices of stopCoordinateList where the stops are too close together
for i in range(len(stopCoordinateList) - 1):
    # I did some calculations between points and .00003 looked to be a reasonable cutoff
    if (distance(stopCoordinateList[i], stopCoordinateList[i+1]) < .00003):
        tooClose.append(i)

tooCloseLength = len(tooClose)

# delete the stops that are too close together, need to subtract i in here because of previous indeces deleted
for i in range(tooCloseLength):
    del stopCoordinateList[tooClose[i] - i]

# print the remaining stops after deleting the duplicates that were too close
for i in range(len(stopCoordinateList)):
    print(stopCoordinateList[i][0], ", ", stopCoordinateList[i][1], sep="")

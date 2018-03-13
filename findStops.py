import pandas as pd

EvanData1 = pd.read_csv("C:/Users/student/Documents/CS4630/Self-Driving Project/EvanData1.csv")
EvanData1Subset = EvanData1.iloc[:,[1,5,6,7,8,21,22]]
# maybe add rotation column
EvanData1Subset.columns = ["sampleNum", "latitude", "longitude", "altitude", "speed", "accelerationX", "accelerationY"]

stops = {} # this declares a dictionary that will hold the stops

# can't check for 0 speed because cars don't always go to complete stop at stop sign, but they do at lights

# the data points I get back from the low speed and positive acceleration seem good other than parking lots
# reason for positive acceleration to identify is you have to speed back up after a stop
for i in range(len(EvanData1Subset)):
    speed = EvanData1Subset.iloc[i,4]
    latitude = EvanData1Subset.iloc[i,1]
    longitude = EvanData1Subset.iloc[i,2]
    accelY = EvanData1Subset.iloc[i,6]

    # check if speed is less than 1.5 m/s (3.36 mph) and then something about accelerationY
    if speed < 1.5 and accelY > .1 and latitude not in stops:
        stops[str(latitude)] = longitude

for i in stops:
    print(i, ", ", stops[i], sep="")
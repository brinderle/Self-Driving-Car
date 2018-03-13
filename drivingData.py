# TO INSTALL A PACKAGE, YOU MUST FIRST DOWNLOAD IT BY SAYING IN COMMAND PROMPT, "pip3 install package_name"
import numpy as np
import pandas as pd
from numpy import genfromtxt


# This was my way of creating a data frame in numpy
# # skip_header=1 means skip 1 line to get past the header
# # reading the data using genfromtxt typically takes a few seconds, not quick
# my_data = genfromtxt('C:/Users/student/Documents/CS4630/Self-Driving Project/appData1.csv', delimiter=',', skip_header=1)
#
# #subset the data to have only the columns we want
# np_my_data = np.array(my_data[:,[1,5,6,7,8,21,22]])
# print(np_my_data[0,:])

# THIS WAY WAS DONE USING PANDAS RATHER THAN NUMPY
EvanData1 = pd.read_csv("C:/Users/student/Documents/CS4630/Self-Driving Project/EvanData1.csv")
EvanData1Subset = EvanData1.iloc[:,[1,5,6,7,8,21,22]]
# maybe add rotation column
EvanData1Subset.columns = ["sampleNum", "latitude", "longitude", "altitude", "speed", "accelerationX", "accelerationY"]
print(EvanData1Subset.iloc[0:5,:])
# print(EvanData1Subset['speed'].max())
# print(EvanData1Subset['accelerationY'].max())
#
# print(EvanData1Subset.iloc[1,2])

# make a table of values with column 1 as latitude, 2 as longitude, 3 as name for point, all separated by commas
# go to https://www.darrinward.com/lat-long/ and paste in the data to see the points lined up on google maps
mapPoints = pd.DataFrame(columns=('lat','lon','sampleNum'))

for i in range(len(EvanData1Subset)):
    if i % 200 == 0:
        mapPoints = mapPoints.append({'lat':EvanData1Subset.iloc[i,1],'lon':EvanData1Subset.iloc[i,2],'sampleNum':EvanData1Subset.iloc[i,0]}, ignore_index=True)

for i in range(len(mapPoints)):
    print(str(mapPoints.iloc[i,0]) + "," + str(mapPoints.iloc[i,1]) + "," + str(mapPoints.iloc[i,2]))

# https://stackoverflow.com/questions/3518778/how-to-read-csv-into-record-array-in-numpy
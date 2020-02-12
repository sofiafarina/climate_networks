import numpy as np
from scipy.io import loadmat
import pandas as pd
import networkx as nx
import matplotlib.pyplot as plt
import math



def distance(origin, destination):
    lat1, lon1 = origin
    lat2, lon2 = destination
    radius = 6371 # km

    dlat = math.radians(lat2-lat1)
    dlon = math.radians(lon2-lon1)
    a = math.sin(dlat/2) * math.sin(dlat/2) + math.cos(math.radians(lat1)) \
        * math.cos(math.radians(lat2)) * math.sin(dlon/2) * math.sin(dlon/2)
    c = 2 * math.atan2(math.sqrt(np.abs(a)), math.sqrt(np.abs(1-a)))
    d = radius * c

    return d


LAT = 72;
LON = 144;
N = 492;
NP = LAT*LON;

lat_data = loadmat('lat.mat')
ltdata = lat_data['lat']

lon_data = loadmat('lon.mat')
lgdata = lon_data['lon']


coord_list = []

for i in range(0,LAT):
    for j in range(0,LON):
        coord_list.append((ltdata[i][0],lgdata[j][0]))
        
# matrice delle distanze 
        
distanze = np.zeros((NP,NP));

for i in range(0,NP):
    for j in range(0,NP):
        if i != j:
            distanze[i][j] = distance((coord_list[i][0],coord_list[i][1]),(coord_list[j][0],coord_list[j][1]))
        
np.save("distance_matrix_p.npy",distanze)        

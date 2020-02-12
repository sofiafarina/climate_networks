import numpy as np
from scipy.io import loadmat
import pandas as pd
import networkx as nx
import matplotlib.pyplot as plt
import math


# funzioni 

def distance(origin, destination):
    lat1, lon1 = origin
    lat2, lon2 = destination
    radius = 6371 # km

    dlat = math.radians(lat2-lat1)
    dlon = math.radians(lon2-lon1)
    a = math.sin(dlat/2) * math.sin(dlat/2) + math.cos(math.radians(lat1)) \
        * math.cos(math.radians(lat2)) * math.sin(dlon/2) * math.sin(dlon/2)
    c = 2 * math.atan2(math.sqrt(a), math.sqrt(1-a))
    d = radius * c

    return d

# variabili 

LAT = 72;
LON = 144;
N = 492;
tau = 0.65; # threshold, da letteratura


data = loadmat('precip.mat')
pdata = data['precip']

lat_data = loadmat('lat.mat')
ltdata = lat_data['lat']

lon_data = loadmat('lon.mat')
lgdata = lon_data['lon']

# creo la tabella con le colonne che sono le time series dei nodi
print("creating table")

table = pd.DataFrame();

h = 1;
for i in range(1,LON):
    for j in range(1,LAT):
        table[h]= pdata[i,j,:];
        h = h+1;

# rimuovo le colonne con i valori mancanti 
        
table = table.replace(-9.969209968386869e+36,np.NaN)
table = table.dropna(axis = 1)
        
# rimozione di colonne che hanno la flag del dato mancante 
 
ampiezza = 72;       
init_col = 12;
fin_col = init_col+ampiezza; 

NP = table.shape[1];

# dataframe che collega il nome dei nodi alle loro coordinate 

print("creating distance matrix")

coord_list = []

for i in range(1,LAT):
    for j in range(1,LON):
        coord_list.append((ltdata[i][0],lgdata[j][0]))
        
# matrice delle distanze 
        
distanze = np.zeros((NP,NP));

for i in range(1,NP):
    for j in range(1,NP):
        distanze[i][j] = distance((coord_list[i][0],coord_list[i][0]),(coord_list[i][1],coord_list[i][1]))
        #distanze[i][j] = (coord_list[i][0]-coord_list[j][0])+coord_list[i][1]-coord_list[j][1])
        
np.save("dm_p_812.npy",distanze)        



# seleziono un certo numero di anni

sel_range = table.iloc[init_col:fin_col];

# standardizzo le time series 

print("standardizing")

standardized = (sel_range-sel_range.mean())/sel_range.std()

# rimozione delle colonne con nan 

standardized = standardized.interpolate()
SIZE = standardized.shape[1]

# calcolo la correlazione tra le colonne (ovvero tra le ts): MATRICE DI CORRELAZIONE

print("creating correlation matrix")

correlation = standardized.corr(method='pearson') # alternative: pearson, kendall, spearman or callable 

# calcolo la matrice di adiacenza imponendo un threshold
print("creating adjacency matrix")

adjacency = np.zeros((SIZE,SIZE));
for i in range(1,SIZE):
    for j in range(1,SIZE):
        if np.abs(correlation.iloc[i,j]) > tau:
            adjacency[i,j] = 1.;
            print("miao")

np.save("am_p_812.npy",adjacency)

weighted = np.abs(adjacency*distanze) 

# creo il network a partire dalla matrice di adiacenza

print("creating graph")

G = nx.from_numpy_matrix(weighted, parallel_edges=False)
prima = G.number_of_edges()
print(prima)

edge_weights = nx.get_edge_attributes(G,'weight')
G.remove_edges_from((e for e, w in edge_weights.items() if w < 40.))
dopo = G.number_of_edges()
print(dopo)

# rimozione dei link tra due nodi vicini
# fare qualcosa di simile a [node for node,degree in dict(G.degree()).items() if degree > 2]
# e poi rimuovere con remove_edges_from 

# analisi del network

print("calculating degree centrality")

deg_cent = nx.degree_centrality(G)
#bet_cent = nx.betweenness_centrality(G)
#clos_cent = nx.closeness_centrality(G)

np.save("dc_p_412.npy",pd.Series(deg_cent))

# visualizzazione
# plt.figure()
# plt.hist(list(deg_cent.values()))
# plt.show()


final_df = pd.DataFrame(coord_list)
final_df[2] = pd.Series(deg_cent)
#final_df[3] = pd.Series(bet_cent)
#final_df[4] = pd.Series(clos_cent)


        





    

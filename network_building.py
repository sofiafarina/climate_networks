import numpy as np
from scipy.io import loadmat
import pandas as pd
import networkx as nx
import matplotlib.pyplot as plt

# variabili

LAT = 72;
LON = 144;
N = 492;
NP = LAT*LON;
tau = 0.55;


# matrice delle distanze 

print("loading distance matrix")
distanze = np.load("distance_matrix_p.npy")

# lista delle coordinate
print("loading coord list")
coord_list = np.load("coord_list.npy")


# dati sulle precipitazioni 
# creazione delle tabella che ha come colonne le time-series 

print("loading data")
data = loadmat('precip.mat')
pdata = data['precip']

table = pd.DataFrame();

h = 1;
for i in range(0,LON):
    for j in range(0,LAT):
        table[h]= pdata[i,j,:];
        h = h+1;
        
        
# selezione di alcuni anni
        
print("selecting range")  
      
ampiezza = 72;   # sei anni
init_col = 112;
fin_col = init_col+ampiezza; 

sel_range = table.iloc[init_col:fin_col];

# standardizzo le time series 

print("standardizing")

standardized = (sel_range-sel_range.mean())/sel_range.std()
standardized = standardized.interpolate()
SIZE = standardized.shape[1]

correlation = standardized.corr(method='pearson') # alternative: pearson, kendall, spearman or callable 

# calcolo la matrice di adiacenza imponendo un threshold

print("computing adjacency matrix")

adjacency = np.zeros((SIZE,SIZE));
for i in range(1,SIZE):
    for j in range(1,SIZE):
        if np.abs(correlation.iloc[i,j]) > tau:
            adjacency[i,j] = 1.;

#np.save("am_p_85_412.npy",adjacency)

weighted = np.abs(adjacency*distanze) 
#%%
np.save("adj_112.npy", weighted)

# creazione del network

print("creating graph")

G = nx.from_numpy_matrix(weighted, parallel_edges=False)
prima = G.number_of_edges()
print(prima)

edge_weights = nx.get_edge_attributes(G,'weight')
G.remove_edges_from((e for e, w in edge_weights.items() if w < 800.))
G.remove_edges_from((e for e, w in edge_weights.items() if w > 20000.))
dopo = G.number_of_edges()
print(dopo)

# network analysis

print("computing degree centrality")

deg_cent = nx.degree_centrality(G)
#bet_cent = nx.betweenness_centrality(G)
#clos_cent = nx.closeness_centrality(G)

array_dc = pd.Series(deg_cent)
array_dc.to_csv("deg_cent_p_112")


final_df = pd.DataFrame(coord_list)
final_df[2] = pd.Series(deg_cent)
#final_df[3] = pd.Series(bet_cent)
#final_df[4] = pd.Series(clos_cent)


final_df.to_csv("finaldf_p_112")  

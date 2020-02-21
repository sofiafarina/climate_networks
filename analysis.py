import numpy as np
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
import networkx as nx

# Periodi: (A) da 12, (B) da 112, (C) da 212, (D) da 312, (E) da 400


adjacency = np.load("Desktop/adj_12.npy")

print("creating graph")
G = nx.from_numpy_matrix(adjacency, parallel_edges=False)
prima = G.number_of_edges()

print("distance cut-off")
edge_weights = nx.get_edge_attributes(G,'weight')
G.remove_edges_from((e for e, w in edge_weights.items() if w < 800.))
G.remove_edges_from((e for e, w in edge_weights.items() if w > 20000.))
dopo = G.number_of_edges()

#%%
# selection of connected components 
S = [G.subgraph(c).copy() for c in nx.connected_components(G)]
largest_connected = S[1] # assumo siano ordinati, è giusto?

#%%

print("computing degree histogram")
deg_histo = nx.degree_histogram(G)
# Returns a list of the frequency of each degree value.

plt.hist(deg_histo, bins =100, range = (0,50))
plt.title("degree histogram (E)")

#%%

print("computing density")
density = nx.density(G)
print("density is", density)

#%%

print("computing diameter")
diameter = nx.diameter(largest_connected)
print("diameter is", diameter)
#long long 

#%%
print("computing the average clustering")
avg_clust = nx.average_clustering(G)
print("average clustering is", avg_clust)
# un poco lungo (dalle 11.32 alle 11.38)

#%%

print("computing laplacian spectrum")
lap_spec = nx.laplacian_spectrum(G, weight = 'weight')
plt.plot(lap_spec)
plt.title("laplacian spectrum (E)")
# prendere i primi autovalori e vedere la loro molteplicità
# non è troppo lento nel calcolo

#%%

print("computing centrality measures")
deg_cent = nx.degree_centrality(G)
plt.hist(pd.Series(deg_cent), bins = 50)
plt.title("degree centrality (E)")
# non è lento

#%%

print("computing betwenness measures")
bet_cent = nx.betweenness_centrality(G)
# molto lungo

#%%

print("computing closeness measures")
clos_cent = nx.closeness_centrality(G)

#%%

print("computing avg shst path length")
avg_s_path = nx.average_shortest_path_length(G)

#%%
r = ['A','B','C','D','E']
dst = [0.03070465907372277,0.0272638272617172, 0.036226356899325615, 0.03430904850624072, 0.03699926434424521]
plt.ylim(0.01,0.05)
plt.plot(r,dst)
plt.title("Density variation")

#%%
r = ['A','B','C','D','E']
avgcl = [ 0.3987558317924219 ,0.3827655402340547, 0.4163728385629933,  0.41910714676578453, 0.41157384408015824]
plt.ylim(0.3,0.5)
plt.plot(r,avgcl)
plt.title("Average clustering variation")

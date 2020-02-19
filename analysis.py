import numpy as np
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
import networkx as nx


adjacency = np.load("adj_12.npy")

print("creating graph")
G = nx.from_numpy_matrix(adjacency, parallel_edges=False)
prima = G.number_of_edges()

print("distance cut-off")
edge_weights = nx.get_edge_attributes(G,'weight')
G.remove_edges_from((e for e, w in edge_weights.items() if w < 800.))
G.remove_edges_from((e for e, w in edge_weights.items() if w > 20000.))
dopo = G.number_of_edges()

#%%

print("computing degree histogram")
deg_histo = nx.degree_histogram(G)
# Returns a list of the frequency of each degree value.

plt.hist(deg_histo, bins =100, range = (0,50))
plt.show()

#%%

print("computing density")
density = nx.density(G)
print("density is", density)

#%%

print("computing diameter")
diameter = nx.diameter(G)
print("diameter is", diameter)
# NetworkXError: Found infinite path length because the graph is not connected

#%%
print("computing the average clustering")
avg_clust = nx.average_clustering(G)
print("average clustering is", avg_clust)
# lungo

#%%

print("computing laplacian spectrum")
lap_spec = nx.laplacian_spectrum(G, weight = 'weight')
plt.plot(lap_spec)
# prendere i primi autovalori e vedere la loro molteplicità
# non è troppo lento nel calcolo

#%%

print("computing centrality measures")
deg_cent = nx.degree_centrality(G)
plt.hist(pd.Series(deg_cent), bins = 50)
plt.title("degree centrality")
# non è lento

#%%

print("computing betwenness measures")
bet_cent = nx.betweenness_centrality(G)

#%%

print("computing closeness measures")
clos_cent = nx.closeness_centrality(G)

#%%

print("computing avg shst path length")
avg_s_path = nx.average_shortest_path_length(G)


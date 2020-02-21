import numpy as np
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
import csv

# Periodi: (A) da 12, (B) da 112, (C) da 212, (D) da 312, (E) da 400

def label_race (row):
    if row['lat'] >= 66.0 :
        return 'north pole'
    if row['lat'] <= -66.0 :
        return 'south pole'
    if np.abs(row['lat']) < 23.5:
        return 'tropics'
    return 'other'



#data_A = pd.read_csv("finaldf_p_75_212")
#data_B = pd.read_csv("finaldf_p_75_312")

data_A = pd.read_csv("Desktop/finaldf_p_12")
data_B = pd.read_csv("Desktop/finaldf_p_112")
data_C = pd.read_csv("Desktop/finaldf_p_212")
data_D = pd.read_csv("Desktop/finaldf_p_312")
data_E = pd.read_csv("Desktop/finaldf_p_400")


degcent = pd.DataFrame();
degcent["lat"] = data_A["0"]
degcent["lon"] = data_A["1"]
degcent["A"] = data_A["2"]
degcent["B"] = data_B["2"]
degcent["C"] = data_C["2"]
degcent["D"] = data_D["2"]
degcent["E"] = data_E["2"]

#degcent["area (p)"] = np.where(np.abs(degcent['lat']) >=66, 'poles', 'no')
#degcent["area (t)"] = np.where(np.abs(degcent['lat']) <=23.5, 'tropics', 'no')

degcent["area"] = degcent.apply (lambda row: label_race(row), axis=1)

pdata = pd.DataFrame()

pdata["A"]=degcent["A"]
pdata["B"]=degcent["B"]
pdata["C"]=degcent["C"]
pdata["D"]=degcent["D"]
pdata["E"]=degcent["E"]
pdata["area"]=degcent["area"]



#%%
# =============================================================================
 
sns.set(style="whitegrid")
g = sns.relplot(x="A",y="B", hue = "area (p)", data = degcent)
g.fig.suptitle("degree centrality, (B) vs (C)")
h = sns.relplot(x="A",y="B", hue = "area (t)", data = degcent)
h.fig.suptitle("degree centrality, (B) vs (C)")
#%%
i = sns.pairplot(pdata, hue = "area")
i.fig.suptitle("degree centrality,  comparison")
i.savefig('comparison_dc.png')
 
# =============================================================================

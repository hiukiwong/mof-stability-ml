import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
from scipy.spatial import distance
from refdata.metal_set import metal_symbols

df = pd.read_table('RASPA_Output/IRMOF-1.xyz', skiprows=2, delim_whitespace=True, names=['atom', 'x','y','z'])
centroid=[np.mean(df['x'].tolist(), axis=0), np.mean(df['y'].tolist(), axis=0), np.mean(df['z'].tolist(), axis=0)]

df['xyz']= df[['x','y','z']].values.tolist()

df['distance']=df['xyz'].apply(lambda row: distance.euclidean(centroid, row))
df1=df.loc[df['atom'].isin(metal_symbols)]
df.index+=1
df[df['distance']==df1['distance'].min()]

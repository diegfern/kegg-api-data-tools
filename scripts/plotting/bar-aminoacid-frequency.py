import pandas as pd
import sys
import matplotlib.pyplot as plt

data_path = sys.argv[1]
export_path = sys.argv[2]
id_column = sys.argv[3]

residues = ['A','C','D','E','F','G','H','I','K','L','M','N','P','Q','R','S','T','V','W','Y']

dataframe_sequences = pd.read_csv(f"{data_path}/sequences.csv")
dataframe_aminoacids = pd.read_csv(f"{data_path}/aminoacids.csv")

df = pd.merge(dataframe_sequences, dataframe_aminoacids, on=id_column)

colors = ['#044cf3','#04e8f3','#f304c0','#f32e04','#f3a604','#c9f304','#51f304']
fig = plt.figure(figsize=(10, 5))
plt.title(f"Frecuencia aminoacidica", fontsize='18')
plt.xlabel("Aminoacidos canonicos")
plt.ylabel("Cantidad")

for i in range(1,8):
    ec_p = df.loc[df['enzyme_code'].str.startswith(str(i) + '.')]
    #plt.bar(residues, ec_p[residues].sum(), width=0.4, color=colors[i-1])
    plt.scatter(residues, ec_p[residues].sum(), color=colors[i-1], marker="x")

plt.legend(labels=['EC: 1','EC: 2','EC: 3','EC: 4','EC: 5','EC: 6','EC: 7'], loc='best')
plt.savefig(f"{export_path}aminoacid-frequency.png", transparent=True)


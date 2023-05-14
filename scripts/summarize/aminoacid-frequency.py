import pandas as pd
import sys

data_path = sys.argv[1]
export_path = sys.argv[2]
sequence_column = sys.argv[3]
id_column = sys.argv[4]


residues = ['A','C','D','E','F','G','H','I','K','L','M','N','P','Q','R','S','T','V','W','Y']

print("Loading data")
dataframe = pd.read_csv(f"{data_path}")

#dataframe = dataframe.drop(columns=['enzyme_code','organism','sequence_id','sequence_description'])

print("Processing data")
data = []
for idx, row in dataframe.iterrows():
    aminoacid_frequency = []
    for residue in residues:
        aminoacid_frequency.append(row[sequence_column].count(residue))
    data.append(aminoacid_frequency)

print("Saving data")
df_export = pd.DataFrame(data, columns=residues)
df_export[id_column] = dataframe[id_column]
df_export.to_csv(f"{export_path}aminoacids.csv", index=False)
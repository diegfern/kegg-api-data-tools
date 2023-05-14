from tqdm import tqdm
import pandas as pd
from scripts.summarize import summarytools
import sys
residues = ['A','C','D','E','F','G','H','I','K','L','M','N','P','Q','R','S','T','V','W','Y']
data_path = sys.argv[1]
base_name = sys.argv[2]
seq_col = sys.argv[3]
export_path = sys.argv[4]

dataset_sequences = pd.read_csv(f"{data_path}{base_name}.csv")
df_export = pd.DataFrame(columns=['id','response','seq'])

index_list = []
for idx, row in tqdm(dataset_sequences.iterrows(), desc=f"Cleaning invalid aminoacids"):
    if not all(c in residues for c in row[seq_col]):
        index_list.append(idx)
dataset_sequences.iloc[index_list].to_csv(f"{export_path}removed.csv", index=False)

dataset_sequences = dataset_sequences.drop(index_list)

tmp_data = summarytools.process_data(dataset_sequences)
df_count = pd.DataFrame(tmp_data, columns=['enzyme_code', 'primary', 'secondary', 'terciary'])

print("Saving Data")
dataset_sequences.to_csv(f"{export_path}{base_name}.csv", index=False)
df_count.to_csv(f"{export_path}summary.csv", index=False)
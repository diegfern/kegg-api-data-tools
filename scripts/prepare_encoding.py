# Get sampled data. Requires sampling/extract-balanced-data.py execution
# TODO Ver si sigue funcionando para ec terciarios
import pandas as pd
import sys
from tqdm import tqdm

residues = ['A','C','D','E','F','G','H','I','K','L','M','N','P','Q','R','S','T','V','W','Y']
data_path = sys.argv[1]
base_name = sys.argv[2]
export_path = sys.argv[3]
# To change the possible responses based in:
# 1: Primary
# 2: Secondary
# 3: Terciary
ec = sys.argv[4]

dataset = pd.read_csv(f"{data_path}{base_name}.csv")
summary_df = pd.read_csv(f"{data_path}summary.csv")

data_export = []
last_row = 0
for idx, row in tqdm(dataset.iterrows(), desc="Processing rows for encoding"):
    if not all(c in residues for c in row['sequence_aa']):
        print(f'Data is not cleaned, must run clean-invalid-aminoacids.py')
        exit(-1)

    enzyme_code = ".".join(row['enzyme_code'].split(".")[:int(ec)]) + ".-"
    summary_row = summary_df[summary_df['enzyme_code'].str.startswith(enzyme_code)].index.values[0]
    data_export.append([f"{row['organism']}:{row['sequence_id']}",summary_row,row['sequence_aa']])

print("Saving into dataframe")
df_export = pd.DataFrame(data_export, columns=['id','response','seq'])
df_export.to_csv(f"{export_path}data_for_nlp.csv", index=False)

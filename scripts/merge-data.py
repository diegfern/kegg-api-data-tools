import sys
from tqdm import tqdm
import pandas as pd
#from scripts.summarize import summarytools
import re

data_path = sys.argv[1]
base_name = sys.argv[2]
export_path = sys.argv[3]
# 1: True, 0: False
clean_invalid = int(sys.argv[4])

dataset_sequences = pd.DataFrame()

for i in tqdm(range(0,9),desc="Loading gene data"):
    df_tmp = pd.read_csv(f"{data_path}{base_name}{i}.csv")
    dataset_sequences = pd.concat([dataset_sequences, df_tmp], ignore_index=True)

if clean_invalid:
    pattern = re.compile("[A-Za-z]+")
    for idx, seq in tqdm(dataset_sequences.iterrows(), desc="Cleaning invalid char (not in A-Z)"):
        # Creo que no es necesario validar...
        # Simplemente se puede reemplazar y me ahorro una comprobacion sin cambios.
        if pattern.fullmatch(seq['sequence_aa']) is None:
            dataset_sequences.at[idx, 'sequence_aa'] = re.sub("[^A-Z]+", '', seq['sequence_aa'])


#FALTA ORDENAR POR EC
print("Sorting Dataframe")
dataset_sequences = dataset_sequences.sort_values(by=['enzyme_code','organism'])

#tmp_data = summarytools.process_data(dataset_sequences)
#df_count = pd.DataFrame(tmp_data, columns=['enzyme_code', 'primary', 'secondary', 'terciary'])

print("Saving Data")
dataset_sequences.to_csv(f"{export_path}{base_name}.csv", index=False)
#df_count.to_csv(f"{export_path}summary.csv", index=False)

# Este algoritmo no requiere preparing_encoding.py
from tqdm import tqdm
import pandas as pd
import math
import sys
import os

data_path = sys.argv[1]
export_path = sys.argv[2]
base_name= sys.argv[3]
total_samples = sys.argv[4]
samples_by_ec = math.ceil(int(total_samples)/7)

print("Loading data")
dataset_sequences = pd.read_csv(f"{data_path}{base_name}.csv")
dataset_sequences = dataset_sequences.drop(columns=['sequence_description'])
dataset_sampled = pd.DataFrame(columns=['index','enzyme_code','organism','sequence_id','sequence_aa','response'])

#Add index column
dataset_sequences.insert(0, 'index', list(range(len(dataset_sequences))))

for i in tqdm(range(1,8), desc="Sampling data"):
    ec_p = dataset_sequences.loc[dataset_sequences['enzyme_code'].str.startswith(str(i) + '.')]
    ec_p = ec_p.sample(n=samples_by_ec)
    ec_p['response'] = i - 1
    dataset_sampled = pd.concat([dataset_sampled, ec_p])

dataset_sampled = dataset_sampled.sort_values(by=['index'])

if not os.path.exists(export_path):
    os.makedirs(export_path)

dataset_sampled.to_csv(f"{export_path}{base_name}.csv", index=False)

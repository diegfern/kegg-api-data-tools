import pandas as pd
from scripts.summarize import summarytools
import sys

data_path = sys.argv[1]
base_name = sys.argv[2]
seq_col = sys.argv[3]
export_path = sys.argv[4]

print("Loading data")
dataset_sequences = pd.read_csv(f"{data_path}{base_name}.csv")
dataset_sequences['len'] = dataset_sequences[seq_col].str.len()

q1 = dataset_sequences.len.quantile(0.25)
q3 = dataset_sequences.len.quantile(0.75)

print(f"Filtering data between sequence length {q1} and {q3}")
dataset_sequences = dataset_sequences.loc[(dataset_sequences['len'] <= q3) & (dataset_sequences['len'] >= q1)]

dataset_sequences = dataset_sequences.drop(columns=['len'])

export_data = summarytools.process_data(dataset_sequences)
df_summary_export = pd.DataFrame(export_data, columns=['enzyme_code','primary','secondary','terciary'])

print("Saving data")
dataset_sequences.to_csv(f"{export_path}{base_name}1.csv", index=False)
df_summary_export.to_csv(f"{export_path}summary.csv", index=False)

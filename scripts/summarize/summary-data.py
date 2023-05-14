# Este metodo carga los 8 archivos y los guarda en memoria,
# LUego guarda versiones spliteadas de estas, el metodo ocupa mucha RAM.
# Este es especifico para genes 0, 7
import sys
import pandas as pd
import summarytools

file_path = sys.argv[1]
column_name = sys.argv[2]
export_path = sys.argv[3]

dataset_sequences = pd.read_csv(file_path)
dataset_sequences = dataset_sequences[column_name]

export_data = summarytools.process_data(dataset_sequences)

df_export = pd.DataFrame(export_data, columns=[column_name,'primary','secondary','terciary','quaternary'])
df_export.to_csv(f"{export_path}summary.csv", index=False)
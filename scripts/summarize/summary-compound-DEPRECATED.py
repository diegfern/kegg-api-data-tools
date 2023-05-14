# TODO ARRELGAR ANTES DE UTILIZAR
# Se cambio ../../data-summary/compound.csv a data-compount/summary.csv
import pandas as pd
import summarytools

# Esto puede ser generalizado
dataset_compound = pd.read_csv(f"../../data-compound/compound.csv")

export_data = summarytools.process_data(dataset_compound)

df_export = pd.DataFrame(export_data, columns=['enzyme_code','primary','secondary','terciary'])
df_export.to_csv("../../data-summary/summary.csv", index=False)
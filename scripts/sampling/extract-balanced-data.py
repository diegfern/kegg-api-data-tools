# Por alguna razon guarda 2 veces, uno con el otal y otro con el balanceado
# TODO Cambiar linea 18. Se cambiaron de lugar las cosas
import pandas as pd
from tqdm import tqdm
from scripts.summarize import summarytools
import sys


data_path = sys.argv[1]
export_path = sys.argv[2]
max_samples = sys.argv[3]

dataset_sequences = pd.read_csv(f"{data_path}genes.csv")
df_count = pd.read_csv(f"{data_path}summary.csv")
nsamples_list = []
# ESto por si agregue algo
#df_count = df_count[:317]
samples_by_p = int(max_samples)/7

for p in range(1,8):
    if sys.argv[2]:
        ec_p = df_count.loc[df_count['enzyme_code'].str.startswith(str(p)).fillna(False)]
        ec_p = ec_p[ec_p['terciary'] != '']
    else:
        ec_p = df_count.loc[df_count['enzyme_code'].str.startswith(str(p)).fillna(False)]
        ec_p = ec_p[ec_p['terciary'].notna()]
    nsamples = 0

    samples_by_t = int(samples_by_p/len(ec_p))

    for i, row in ec_p.iterrows():
        if row['terciary'] >= samples_by_t:
            nsamples_list.append([row['enzyme_code'], samples_by_t])
            nsamples+=samples_by_t
        else:
            nsamples_list.append([row['enzyme_code'], row['terciary']])
            nsamples+=row['terciary']

    # Que pasa si nsamples < samples_by_p, habria que distribuir los samples faltantes
    # En el resto de numeros ec.
    while nsamples < samples_by_p:
        for i, row in ec_p.iterrows():
            if row['terciary'] < samples_by_t:
                continue
            if nsamples <= samples_by_p:
                for j in range(len(nsamples_list)):
                    if nsamples_list[j][0] == row['enzyme_code']:
                        nsamples_list[j][1] += 1
                        break
                nsamples += 1
            else:
                break

    #print(nsamples,len(ec_p),samples_by_t, samples_by_p)
    # Imprimo la info de cual es el numero ec sin suficientes datos.
    '''
    for row in nsamples_list:
        if row[0].startswith(f"{p}.") and row[1] < samples_by_t:
            print(row)
    '''

df_export = pd.DataFrame(columns=['enzyme_code','organism','sequence_id','sequence_description'])
# La forma mas lenta de hacerlo...
for row in tqdm(nsamples_list,desc=f"Getting random samples"):
    ec_p = dataset_sequences.loc[dataset_sequences['enzyme_code'].str.startswith(row[0][:-1])]
    df_export = pd.concat([df_export, ec_p.sample(n=int(row[1]))])

df_export = df_export.sort_values(by=['enzyme_code','organism','sequence_id'])

export_data = summarytools.process_data(df_export)

df_summary_export = pd.DataFrame(export_data, columns=['enzyme_code','primary','secondary','terciary'])
df_summary_export.to_csv(f"{export_path}summary.csv", index=False)
df_export.to_csv(f"{export_path}genes.csv", index=False)

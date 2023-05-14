import sys
from os import listdir
from os.path import isfile, join
import re
import json
import pandas as pd
import matplotlib.pyplot as plt

# TODO Falta saber que es scale y todo eso

models = ['bepler', 'esm', 'plus_rnn', 'prottrans']

data_path = sys.argv[1]
iterations = int(sys.argv[2])
scale_options = int(sys.argv[3])

cnn_architectures = [f for f in listdir(data_path) if not isfile(join(data_path, f))]

cnn_architectures = [f for f in cnn_architectures if ("CNN" or "cnn") in f]

results_json = []
for architecture in cnn_architectures:
    folders = [f for f in listdir(f"{data_path}{architecture}/protein/") if not isfile(join(data_path, f))]

    for folder in folders:
        # Models iteration
        for m in models:
            #print(f"Opening: {data_path}{architecture}/protein/{folder}/{m}_architecture_{architecture[-1]}.json")
            try:
                with open(f"{data_path}{architecture}/protein/{folder}/{m}_architecture_{architecture[-1]}.json", "r") as f:
                        tmp = json.load(f)
                        if 'accuracy' not in tmp['train_metrics']:
                            continue
                        results_json.append(tmp)
            except json.decoder.JSONDecodeError:
                #print(f"JSONDecodeError in {data_path}{architecture}/protein/{folder}/{m}_architecture_{architecture[-1]}.json\nOmitting...")
                continue
            except FileNotFoundError:
                continue
        for g in range(8):
            #print(f"Opening: {data_path}{architecture}/protein/{folder}/{m}_architecture_{architecture[-1]}.json")
            try:
                with open(f"{data_path}{architecture}/protein/{folder}/group{g}_architecture_{architecture[-1]}.json", "r") as f:
                        tmp = json.load(f)
                        if 'accuracy' not in tmp['train_metrics']:
                            continue
                        results_json.append(tmp)
            except json.decoder.JSONDecodeError:
                #print(f"JSONDecodeError in {data_path}{architecture}/protein/{folder}/{m}_architecture_{architecture[-1]}.json\nOmitting...")
                continue
            except FileNotFoundError:
                continue

df = pd.DataFrame()

for idx, json in enumerate(results_json):
    results_json[idx].pop('labels')
    train_metrics = results_json[idx].pop('train_metrics')
    test_metrics = results_json[idx].pop('test_metrics')
    train_metrics.pop('mcc')
    train_metrics.pop('confusion_matrix')
    test_metrics.pop('mcc')
    test_metrics.pop('confusion_matrix')
    test_metrics.pop('roc_auc_score')
    #print(results_json[0])
    #print(train_metrics)
    tmp_df = pd.concat(
        [
            pd.DataFrame(results_json[idx], index=[idx]),
            pd.DataFrame(train_metrics, index=[idx]).add_prefix('train_'),
            pd.DataFrame(test_metrics, index=[idx]).add_prefix('test_')
         ], axis=1
    )
    df = pd.concat([tmp_df, df], axis=0)

print(df)

algorythms = df.arquitecture.unique()
df = df.drop(columns=['trainable_params', 'non_trainable_params','total_time',
                      'dataset', 'encoding', 'epochs'])

df = df.groupby('arquitecture').mean()

algorythms = [a[:8] + '...' if len(a) > 8 else a for a in algorythms]

colors = ['#fafa6e', '#b5e877', '#77d183', '#3fb78d', '#009c8f', '#007f86', '#1c6373', '#2a4858']

fig, axs = plt.subplots(3, 3, figsize=(15, 15))
fig.suptitle("Resultados CNN", fontsize='24')
fig.text(0.5, 0.04, 'Arquitectura', ha='center', va='center', fontsize=16)
fig.text(0.06, 0.5, 'Desempeno', ha='center', va='center', rotation='vertical', fontsize=16)
fig.subplots_adjust(left=0.1, bottom=0.1, right=0.9, top=0.9, wspace=0.4, hspace=0.4)


column = 0
for y in range(3):
    for x in range(3):
        if column < len(df.columns):
            minimun = min(df[df.columns[column]])
            maximun = max(df[df.columns[column]])
            minimun = minimun - 0.01 if minimun >= 0.01 else 0
            maximun = maximun + 0.01

            axs[y, x].bar(algorythms, df[df.columns[column]], color=colors)
            axs[y, x].set_title(df.columns[column], fontsize='12')
            axs[y, x].set_ylim(bottom=minimun, top=maximun)
            for tick in axs[y, x].get_xticklabels():
                tick.set_size(9)
                tick.set_rotation(0)
            column += 1
        else:
            axs[y, x].remove()

fig.savefig(f"{data_path}grafico.png")
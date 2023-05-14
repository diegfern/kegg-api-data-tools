import sys
from os import listdir, makedirs, scandir
from os.path import isfile, join, exists
import re
import json

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

# TODO Falta saber que es scale y todo eso

models = ['bepler', 'esm', 'fasttext', 'glove','plus_rnn', 'prottrans']

data_path = sys.argv[1]

cnn_architectures = [f for f in listdir(data_path) if not isfile(join(data_path, f))]
cnn_architectures = [f for f in cnn_architectures if ("CNN" or "cnn") in f]
cnn_architectures.sort()

results_json = []
# Creo que podria listar todos los archivos y ya y me ahorro todos estos for...
# Extract results DL
for architecture in cnn_architectures:
    for scale in [0,1]:
        for m in models:
            try:
                with open(f"{data_path}{architecture}/results_{m}_{scale}.json", "r") as f:
                    tmp = json.load(f)
                    tmp['scaled'] = scale
                    tmp['category'] = "plm"
                    results_json.append(tmp)
            except FileNotFoundError:
                continue
        for g in range(8):
            for fft in ("", "FFT_"):
                try:
                    with open(
                            f"{data_path}{architecture}/group{g}_{fft}scale_{scale}.json", 
                            "r"
                            ) as f:
                        tmp = json.load(f)
                        tmp['scaled'] = scale
                        tmp['encoding'] = f"Group_{g}"
                        tmp['category'] = ''.join(x for x in fft if x.isalpha()).lower()
                        results_json.append(tmp)
                except FileNotFoundError:
                    continue

df_cnn = pd.DataFrame()

for idx, json in enumerate(results_json):
    for column in ['labels', 'total_time', 'dataset', 'epochs']:
        results_json[idx].pop(column)
    train_metrics = results_json[idx].pop('train_metrics')
    test_metrics = results_json[idx].pop('test_metrics')
    train_metrics.pop('mcc')
    train_metrics.pop('confusion_matrix')
    test_metrics.pop('mcc')
    test_metrics.pop('confusion_matrix')
    test_metrics.pop('roc_auc_score')

    tmp_df = pd.concat(
        [
            pd.DataFrame(results_json[idx], index=[idx]),
            pd.DataFrame(train_metrics, index=[idx]).add_prefix('train_'),
            pd.DataFrame(test_metrics, index=[idx]).add_prefix('test_')
         ], axis=1
    )
    df_cnn = pd.concat([tmp_df, df_cnn], axis=0)

df_cnn = df_cnn.sort_values(by=["arquitecture","encoding", "scaled"])

algorithms = df_cnn.arquitecture.unique()

# Extract results ML
df_ml = pd.DataFrame()

for scale in [0, 1]:
    for m in models:
        try:
            tmp = pd.read_csv(f"{data_path}results_ML/{m}_{scale}.csv")
            tmp['encoding'] = m
            tmp['category'] = "plm"
            df_ml = pd.concat([df_ml, tmp], axis=0)
        except FileExistsError:
            continue
    for g in range(8):
        for fft in ("", "FFT_"):
            try:
                tmp = pd.read_csv(f"{data_path}results_ML/group{g}_{fft}scale_{scale}.csv")
                tmp['encoding'] = f"Group_{g}"
                tmp['category'] = ''.join(x for x in fft if x.isalpha()).lower()
                df_ml = pd.concat([df_ml, tmp], axis=0)
            except FileNotFoundError:
                continue


df_ml = df_ml.drop(columns=['fit_time', 'score_time'])
df_ml.rename(columns = {
    'is_scale':'scaled', 
    'train_precision_weighted':'train_precision',
    'train_recall_weighted':'train_recall',
    'train_f1_weighted':'train_f1_score'
    }, inplace=True)
df_cnn.rename(columns = {'arquitecture':'description'}, inplace=True)

df_merged = pd.concat([df_cnn, df_ml])

# df_merged.to_csv(f"{data_path}/training_results.csv", index=False)


if not exists(f"{data_path}/plot/"):
    makedirs(f"{data_path}/plot/")


colors = ['indianred', 'goldenrod', 'yellowgreen', 'skyblue', 'dodgerblue', 'darkviolet', 'hotpink']
# Plot 1
fig, axs = plt.subplots(2, 2, figsize=(8, 8))
fig.suptitle("Resulados Machine Learning Clásico y Deep Learning", fontsize='18')

metrics = ['accuracy','recall','precision','f1_score']
idx = 0
for y in range(2):
    for x in range(2):
        bp = axs[y, x].boxplot(df_merged[[f'train_{metrics[idx]}',f'test_{metrics[idx]}']], notch=True, patch_artist=True)
        axs[y, x].set_ylabel(metrics[idx], rotation=90)
        axs[y, x].set_xticks([1,2],["train","test"])
        for patch, color in zip(bp['boxes'], colors[:2]):
            patch.set_facecolor(color)

        for median in bp['medians']:
            median.set(color ='black', linewidth = 1)
        idx+=1

fig.savefig(f"{data_path}/plot/general-comparison.png")

# Plot 2
fig, axs = plt.subplots(2, 2, figsize=(9, 9))
fig.suptitle("Metricas de rendimiento agrupadas\n por estrategia de codificacion", fontsize='18')

df_normal = df_merged.loc[df_merged.category == ""]
df_fft = df_merged.loc[df_merged.category == "fft"]
df_plm = df_merged.loc[df_merged.category == "plm"]

idx = 0
for y in range(2):
    for x in range(2):
        bp = axs[y, x].boxplot([df_normal[f'train_{metrics[idx]}'], 
            df_fft[f'train_{metrics[idx]}'], 
            df_plm[f'train_{metrics[idx]}'],
            df_normal[f'test_{metrics[idx]}'],
            df_fft[f'test_{metrics[idx]}'], 
            df_plm[f'test_{metrics[idx]}'], 
            ], notch=True, patch_artist=True)
        axs[y, x].set_ylabel(metrics[idx], rotation=90)
        axs[y, x].set_xticks([1,2,3,4,5,6],["properties_train","fft_train","plm_train","properties_test","fft_test","plm_test"], rotation=45)
        for patch, color in zip(bp['boxes'], colors[:3] + colors[:3]):
            patch.set_facecolor(color)

        for median in bp['medians']:
            median.set(color ='black', linewidth = 1)
        idx+=1

fig.savefig(f"{data_path}/plot/comparison-by-category.png")

# Plot 3
fig, axs = plt.subplots(2, 2, figsize=(11, 11))
fig.suptitle("", fontsize='18')

i = 0
for y in range(2):
    for x in range(2):
        j = 1
        bars = []
        axs[y, x].tick_params(axis='x', which='both', bottom=False, labelbottom=False)
        for m in models:
            bars.append(axs[y, x].bar(j,df_plm.loc[df_plm.encoding == m][f"train_{metrics[i]}"].mean(),color=colors[j-1]))
            axs[y, x].vlines(
                    j, 
                    df_plm.loc[df_plm.encoding == m][f"train_{metrics[i]}"].max(), 
                    df_plm.loc[df_plm.encoding == m][f"train_{metrics[i]}"].min(), 
                    color='black')
            j+=1
        axs[y, x].set_ylabel(metrics[i], rotation=90)
        axs[y, x].legend(bars,models)
        i+=1

fig.savefig(f"{data_path}/plot/comparison-by-encoding.png")

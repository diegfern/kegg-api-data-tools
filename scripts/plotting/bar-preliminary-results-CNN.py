import sys
from os import listdir
from os.path import isfile, join
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
for architecture in cnn_architectures:
    # Models iteration
    for m in models:
        for scale in [0,1]:
            try:
                with open(f"{data_path}{architecture}/results_{m}_{scale}.json", "r") as f:
                        tmp = json.load(f)
                        tmp['scaled'] = scale
                        results_json.append(tmp)
            except FileNotFoundError:
                continue


df = pd.DataFrame()

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
    df = pd.concat([tmp_df, df], axis=0)

df = df.sort_values(by=["arquitecture","encoding", "scaled"])

algorythms = df.arquitecture.unique()

df_plot = df
df_plot = df_plot.drop(columns=['arquitecture', 'trainable_params', 'non_trainable_params', 'encoding', 'scaled'], errors="ignore")


fig, axs = plt.subplots(2, 4, figsize=(22, 11))
fig.suptitle("Resultados entrenamiento con CNN", fontsize='32')
fig.text(0.5, 0.04, 'Score', ha='center', va='center', fontsize=24)
fig.text(0.06, 0.5, 'Cantidad', ha='center', va='center', rotation='vertical', fontsize=24)
fig.subplots_adjust(left=0.1, bottom=0.1, right=0.9, top=0.9, wspace=0.4, hspace=0.4)


column = 0
for y in range(2):
    for x in range(4):
        if column < len(df_plot.columns):
            axs[y, x].hist(df_plot[df_plot.columns[column]], bins=7,color='skyblue', ec='gray', lw=1)
            axs[y, x].set_title(df_plot.columns[column], fontsize='12')
            column += 1
        else:
            axs[y, x].remove()

#fig.savefig(f"{data_path}/grafico.png")

df_plot2 = pd.DataFrame()
df_plot2['overfitting_rate_accuracy'] = 1-(df_plot['train_accuracy']*df_plot['test_accuracy'])
df_plot2['overfitting_rate_recall'] = 1-(df_plot['train_recall']*df_plot['test_recall'])
df_plot2['overfitting_rate_precision'] = 1-(df_plot['train_precision']*df_plot['test_precision'])
df_plot2['overfitting_rate_f1_score'] = 1-(df_plot['train_f1_score']*df_plot['test_f1_score'])

fig, axs = plt.subplots(1,4, figsize=(24, 8))
fig.suptitle("Resultados entrenamiento con CNN (overfitting)", fontsize='28')
fig.text(0.5, 0.04, 'Overfitting Rate', ha='center', va='center', fontsize=20)
fig.text(0.06, 0.5, 'Cantidad', ha='center', va='center', rotation='vertical', fontsize=20)
fig.subplots_adjust(left=0.1, bottom=0.1, right=0.9, top=0.9, wspace=0.4, hspace=0.4)

column = 0
for x in range(4):
    if column < len(df_plot2.columns):
        axs[x].hist(df_plot2[df_plot2.columns[column]], bins=7, color='skyblue', ec='gray', lw=1)
        axs[x].set_title(df_plot2.columns[column], fontsize='12')
        column += 1
    else:
        axs[x].remove()

#fig.show()
fig.savefig(f"{data_path}/grafico_overfitting.png")



df = pd.concat([df, df_plot2], axis=1)
selected_percent= np.quantile(df_plot2['overfitting_rate_accuracy'], 0.05)


df_filter_accuracy = df.loc[df['overfitting_rate_accuracy'] <= selected_percent]
df_filter_recall = df.loc[df['overfitting_rate_recall'] <= selected_percent]
df_filter_precision = df.loc[df['overfitting_rate_precision'] <= selected_percent]
df_filter_f1_score = df.loc[df['overfitting_rate_f1_score'] <= selected_percent]

export_df = pd.concat([df_filter_accuracy,df_filter_precision, df_filter_recall, df_filter_f1_score]).drop_duplicates().reset_index(drop=True)

#export_df.to_csv(f"{data_path}/the_best_of_the_best.csv")
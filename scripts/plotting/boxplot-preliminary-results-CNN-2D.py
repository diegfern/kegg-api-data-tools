import sys
from os import listdir, makedirs, scandir
from os.path import isfile, join, exists
import re
import json

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

data_path = sys.argv[1]

cnn_architectures = [f for f in listdir(data_path) if not isfile(join(data_path, f))]
cnn_architectures = [f for f in cnn_architectures if ("CNN" or "cnn") in f]
cnn_architectures.sort()

sizes = [256, 512]

results_json = []

for architecture in cnn_architectures:
    for sc in [0,1]:
        for s in sizes:
            try:
                with open(f"{data_path}{architecture}/results_size-{s}_scale-{sc}_task-classification.json", "r") as f:
                    tmp = json.load(f)
                    tmp['scaled'] = sc
                    results_json.append(tmp)
            except FileNotFoundError:
                continue

df_cnn = pd.DataFrame()

for idx, json in enumerate(results_json):
    for column in ['labels', 'total_time', 'trainable_params', 'non_trainable_params', 'epochs']:
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


algorithms = df_cnn.arquitecture.unique()
df_cnn = df_cnn.sort_values(by=["arquitecture", "dataset", "scaled"])
df_cnn['name'] = df_cnn["arquitecture"] + "-" + df_cnn['dataset'] + "-" + df_cnn['scaled'].astype(str)
df_cnn = df_cnn.drop(columns=['arquitecture', 'dataset', 'scaled'])

if not exists(f"{data_path}/plot/"):
    makedirs(f"{data_path}/plot/")

colors = ['indianred', 'goldenrod', 'yellowgreen', 'skyblue', 'dodgerblue', 'darkviolet', 'hotpink']
# Plot 1
fig, axs = plt.subplots(2, 2, figsize=(10,10))

metrics = ['accuracy','recall','precision','f1_score']
idx = 0
for x in range(2):
    for y in range(2):
        # QUe solucion mas mala XD
        train_col = 'train_' + metrics[idx]
        test_col = 'test_' + metrics[idx]
        train = pd.DataFrame()
        train['name'] = df_cnn['name']
        train['metrics'] = df_cnn[train_col]
        train['type'] = 'train'
        test = pd.DataFrame()
        test['name'] = df_cnn['name']
        test['metrics'] = df_cnn[test_col]
        test['type'] = 'test'
        tmp = pd.concat([train, test], ignore_index=True)

        sns.set_palette("deep")
        sns.barplot(ax=axs[y, x] , data=tmp, x='metrics', y='name', hue='type')
        axs[y, x].set(xlabel=metrics[idx],ylabel="")
        # pd. f. hate seaborn
        '''
        for patch, color in zip(bp['boxes'], colors[:2]):
            patch.set_facecolor(color)

        for median in bp['medians']:
            median.set(color ='black', linewidth = 1)
        '''
        idx+=1

fig.savefig(f"{data_path}/plot/general-comparison-CNN-2D.png", bbox_inches="tight")

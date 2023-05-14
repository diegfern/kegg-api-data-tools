import pandas as pd
import sys
from os import listdir
from os.path import isfile, join
import re
import matplotlib.pyplot as plt
import numpy as np
from colour import Color

models = ['bepler', 'esm', 'plus_rnn', 'prottrans']

data_path = sys.argv[1]
iterations = int(sys.argv[2])
scale_options = int(sys.argv[3])

folders = [f for f in listdir(data_path) if not isfile(join(data_path, f))]
#folders = [re.sub('^results_','', f) for f in folders]

#cnn_architecture = [f for f in folders if ("CNN" or "cnn") in f]

df = pd.DataFrame()
for folder in folders:
    for i in range(iterations):
        for o in range(scale_options):
            # Models iteration
            for m in models:
                print(f"Opening: {data_path}{folder}/{m}_iteration_{i}_scale_option_{o}_balance_0.csv")
                tmp = pd.read_csv(f"{data_path}{folder}/{m}_iteration_{i}_scale_option_{o}_balance_0.csv")
                if not 'test_accuracy' in tmp:
                    continue
                #tmp.insert(1, 'folder', folder)
                #tmp.insert(2, 'encoding', m)
                df = pd.concat([df, tmp], ignore_index=True)


            # Group iteration
            for g in range(8):
                print(f"Opening: {data_path}{folder}/group{g}_iteration_{i}_scale_option_{o}_balance_0.csv")
                tmp = pd.read_csv(f"{data_path}{folder}/group{g}_iteration_{i}_scale_option_{o}_balance_0.csv")
                if not 'test_accuracy' in tmp:
                    continue
                #tmp.insert(1, 'folder', folder)
                #tmp.insert(2, 'encoding', f"group{g}")
                df = pd.concat([df, tmp], ignore_index=True)

algorythms = df.description.unique()
df = df.drop(columns=['iteration', 'is_scale', 'is_unbalance'])
df = df.groupby('description').mean()

algorythms = [a[:8] + '...' if len(a) > 8 else a for a in algorythms]

colors = ['#fafa6e', '#b5e877', '#77d183', '#3fb78d', '#009c8f', '#007f86', '#1c6373', '#2a4858']

fig, axs = plt.subplots(3, 4, figsize=(15, 15))
fig.suptitle("Resultados Machine Learning Clasico", fontsize='24')
fig.text(0.5, 0.04, 'Algoritmo', ha='center', va='center', fontsize=16)
fig.text(0.06, 0.5, 'Desempeno', ha='center', va='center', rotation='vertical', fontsize=16)
fig.subplots_adjust(left=0.1, bottom=0.1, right=0.9, top=0.9, wspace=0.4, hspace=0.4)


column = 0
for y in range(3):
    for x in range(4):
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
                tick.set_rotation(90)
            column += 1
        else:
            axs[y, x].remove()
fig.savefig(f"{data_path}grafico.png")
import sys
from matplotlib import pyplot as plt
import pandas as pd
import numpy as np

data_path = sys.argv[1]

results = pd.read_csv(f"{data_path}results.csv")
results = results.drop(columns=["min_ec","max_ec"])
results = results.sort_values(by=["test_size","data"])

normal = results.loc[~results['data'].str.contains("FFT")].reset_index()
fft = results.loc[results['data'].str.contains("FFT")].reset_index()

test_size_20 = normal.loc[normal['test_size'] == 20]
test_size_30 = normal.loc[normal['test_size'] == 30]
test_size_40 = normal.loc[normal['test_size'] == 40]

labels = ['Group 0','Group 1','Group 2','Group 3','Group 4','Group 5','Group 6','Group 7']

x = np.arange(len(labels))
width = 0.20

fig, ax = plt.subplots()

rects1 = ax.bar(x-width, test_size_20['avg'], width, label='80:20')
rects2 = ax.bar(x, test_size_30['avg'], width, label='70:30')
rects3 = ax.bar(x+width, test_size_40['avg'], width, label='60:40')

ax.set_ylabel('Accuracy')
ax.set_title('Random Forest para clasificacion del primer nivel')
ax.set_xticks(x, labels)
ax.legend()

fig.tight_layout()

plt.savefig(f"./rf.png", transparent=True)
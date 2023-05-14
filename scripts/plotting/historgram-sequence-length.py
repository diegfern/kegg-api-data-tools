import pandas as pd
from matplotlib import pyplot as plt
import numpy as np
from statistics import mean, median
import sys

# Read summary data, e.g. '../../data-summary/summary.csv
data_path = sys.argv[1]
export_path = sys.argv[2]

dataframe = pd.read_csv(f"{data_path}")

dataframe = dataframe.drop(columns=['enzyme_code','organism','sequence_id','sequence_description'], errors='ignore')
#dataframe = dataframe.drop(columns=['Unnamed: 0', 'response', 'enzyme_code','organism','sequence_id'])
dataframe['len'] = dataframe['sequence_aa'].str.len()
#dataframe =  dataframe.loc[(dataframe['len'] <= 1000) & (dataframe['len'] >= 50)]
#print(len(dataframe))


print(f"Min: {min(dataframe['len'])}\n"
      f"Max: {max(dataframe['len'])}\n"
      f"Mean: {mean(dataframe['len'])}\n"
      f"Q1: {dataframe.len.quantile(0.25)}\n"
      f"Q2 (median): {dataframe.len.quantile(0.5)}\n"
      f"Q3: {dataframe.len.quantile(0.75)}")
bins = 40
fig, ax = plt.subplots(figsize=(16, 10))
ax.hist(dataframe['len'], density=False, bins=bins)
for rect in ax.patches:
    height = rect.get_height()
    ax.annotate(f'{int(height)}', xy=(rect.get_x()+rect.get_width()/2, height),
                xytext=(0, 5), textcoords='offset points', ha='center', va='bottom')
plt.title("Largo de secuencias de sequences.csv")
plt.xlabel("Largo")
plt.ylabel("Cantidad")
#plt.show()
plt.savefig(f"{export_path}histogram.png", transparent=True)
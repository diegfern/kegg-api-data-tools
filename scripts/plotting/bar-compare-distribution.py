import pandas as pd
from matplotlib import pyplot as plt
import numpy as np
import math
import sys
from colour import Color

#Compares the distributtion between the sampled data and the original data.

# Read summary data, e.g. '../../data-summary/summary.csv
data_path = sys.argv[1]
compare_path = sys.argv[2]
export_path = sys.argv[3]
dataframe = pd.read_csv(f"{data_path}summary.csv")
dataframe2 = pd.read_csv(f"{compare_path}summary.csv")

outer_colors = ['#044cf3','#04e8f3','#f304c0','#f32e04','#f3a604','#c9f304','#51f304']

dataframe = dataframe[dataframe['primary'].notna()].reset_index()
dataframe2 = dataframe2[dataframe2['primary'].notna()].reset_index()
dataframe = dataframe.drop(columns=['secondary','terciary', 'index','enzyme_code'])
dataframe2 = dataframe2.drop(columns=['secondary','terciary', 'index','enzyme_code'])

ec_p = []

for i in range(7):
    ec_p.append([(dataframe['primary'][i] * 100.) / dataframe['primary'].sum(),
    (dataframe2['primary'][i] * 100.) / dataframe2['primary'].sum()])

tmp = [0.0,0.0]
plt.title("Comparacion de distribuciones por numero EC de primer nivel")

for i in range(7):
    plt.bar(['data','data sampled'], ec_p[i],
            0.5,
            bottom=tmp,
            color=outer_colors[i]
            )
    tmp[0] = tmp[0] + ec_p[i][0]
    tmp[1] = tmp[1] + ec_p[i][1]

plt.legend(labels=['EC: 1','EC: 2','EC: 3','EC: 4','EC: 5','EC: 6','EC: 7'], loc='best')
plt.savefig(f"{export_path}comparison.png", transparent=True)


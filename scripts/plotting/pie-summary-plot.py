import pandas as pd
from matplotlib import pyplot as plt
from matplotlib import colors
import numpy as np
import math
import sys
from colour import Color
import os

# Read summary data, e.g. '../../data-summary/summary.csv
data_path = sys.argv[1]
export_path = sys.argv[2]
dataframe = pd.read_csv(f"{data_path}summary.csv")

ec_p = dataframe[dataframe['primary'].notna()]
ec_s = dataframe[dataframe['secondary'].notna()]
ec_t = dataframe[dataframe['terciary'].notna()]

fig = plt.figure()
#plt.title("Cantidad de secuencias por numero EC de primer nivel")

#outer_colors = ['#044cf3','#04e8f3','#f304c0','#f32e04','#f3a604','#c9f304','#51f304']
outer_colors = [colors.to_hex('royalblue'),
                colors.to_hex('deepskyblue'),
                colors.to_hex('fuchsia'),
                colors.to_hex('tomato'),
                colors.to_hex('gold'),
                colors.to_hex('greenyellow'),
                colors.to_hex('mediumspringgreen')
                ]
plt.pie(ec_p['primary'],
        startangle=90,
        counterclock=False,
        autopct='%1.0f%%',
        colors=outer_colors,
        wedgeprops = {
                "edgecolor" : "#2e2e2e",
                'linewidth': 0.4,
                'antialiased': True
        }
        )

labels = [f"{row['enzyme_code']} {int(row['primary'])}" for idx, row in ec_p.iterrows()]
plt.legend(labels=labels, bbox_to_anchor=(0.05, -0.15), loc='lower right')

if not os.path.exists(export_path):
    os.makedirs(export_path)

plt.savefig(f"{export_path}pie_general.png", transparent=True, bbox_inches='tight')

hex_colors = [
    ["#ecf1ff","#02236e"],
    ["#ecfeff","#02696e"],
    ["#ffecfb","#f304c0"],
    ["#ffefec","#6e1502"],
    ["#fff9ec","#6e4b02"],
    ["#fbffec","#5b6e02"],
    ["#f2ffec","#256e02"]
]

for i in range(1,8):
    ec_s_by_p = ec_s[ec_s['enzyme_code'].str.startswith(f"{i}.")]

    fig = plt.figure(figsize=(10,7))
    plt.title(f"Secuencias del segundo nivel para EC: {i}", fontsize='18')
    y_pos = []
    threshold = 15
    for idx, s in enumerate(ec_s_by_p['secondary']):
        y_pos.append((idx*2)+(0.5*idx))
        if len(ec_s_by_p) > threshold:
            plt.text(y_pos[idx]-1, s, str(f"{round(100. * s / ec_s_by_p['secondary'].sum(),2)} %"), fontsize=8, rotation='60')
        else:
            plt.text(y_pos[idx]-1, s, str(f"{round(100. * s / ec_s_by_p['secondary'].sum(), 2)} %"), fontsize=8)

    plt.bar(y_pos,ec_s_by_p['secondary'],2, color=outer_colors[i-1])
    plt.xticks(y_pos, [row['enzyme_code'][2:-4] for idx, row in ec_s_by_p.iterrows()])
    plt.xlabel("Segundo nivel")
    plt.ylabel("Cantidad de secuencias")

    #Plot con Pie
    '''
    plt.pie(ec_s_by_p['secondary'],
            startangle=90,
            counterclock=False,
            colors=[color.get_hex() for color in inner_colors[(i*2)-2] + inner_colors[(i*2)-1][1:]],
            wedgeprops={
                "edgecolor": "#2e2e2e",
                'linewidth': 0.4,
                'antialiased': True
            }
            )
    percent = 100.*ec_s_by_p['secondary']/ec_s_by_p['secondary'].sum()
    labels_s = ["{} {} - {} %".format(row['enzyme_code'][:-4], int(row['secondary']), round(percent[idx],2)) for idx, row in ec_s_by_p.iterrows()]
    plt.legend(labels=labels_s, bbox_to_anchor=(0.95, 1))
    '''

    fig.savefig(f"{export_path}bar_ec{i}.png", transparent=True, bbox_inches='tight')
    max_plots = len(ec_s_by_p)

    size = math.ceil(math.sqrt(max_plots))
    figure, axis = plt.subplots(size, size, figsize=(20,14))
    figure.suptitle(f"Distribuciones en el tercer nivel para EC: {i}", fontsize=36)
    x = 0
    y = 0

    for j in range(max_plots):
        tmp_df = ec_t[ec_t['enzyme_code'].str.startswith(
            ec_s_by_p['enzyme_code'].iloc[j][:4]
        )]
        color_list = list(Color( hex_colors[i-1][0] ).range_to(Color( hex_colors[i-1][1] ),len(tmp_df)))
        plt_color = [color.get_hex() for color in color_list]
        axis[y, x].pie(tmp_df['terciary'],
                        startangle=90,
                        counterclock=False,
                        colors = plt_color,
                        wedgeprops = {
                            "edgecolor": "#2e2e2e",
                            'linewidth': 0.4,
                            'antialiased': True
                        }
                       )
        axis[y, x].legend(labels=tmp_df['enzyme_code'], bbox_to_anchor=(1.65,0.5), loc='center right')
        x+=1
        if x % size == 0:
            y+=1
            x=0
    while x < size and y < size:
        figure.delaxes(axis[y][x])
        x+=1
        if x % size == 0:
            y+=1
            x=0

    plt.savefig(f"{export_path}pie_ec{i}_subplot.png", transparent=True, bbox_inches='tight')

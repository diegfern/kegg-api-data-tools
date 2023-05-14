import pandas as pd
from matplotlib import pyplot as plt
from matplotlib import colors
import sys

#../../data-filtered/sequences.csv
data_path = sys.argv[1]
#../../data-filtered/plot/
export_path = sys.argv[2]

dataframe = pd.read_csv(data_path, encoding="ISO-8859-1")

#dataframe = dataframe.drop(columns=['enzyme_code','organism','sequence_id','sequence_description'])
dataframe['len'] = dataframe['sequence_aa'].str.len()


data = []
for i in range(1,8):
    ec_p = dataframe.loc[dataframe['enzyme_code'].str.startswith(str(i) + '.')]
    data.append(ec_p['len'])

bp = plt.boxplot(data, notch=True, patch_artist=True)

#colors = ['#044cf3','#04e8f3','#f304c0','#f32e04','#f3a604','#c9f304','#51f304']
colors = [colors.to_hex('royalblue'),
                colors.to_hex('deepskyblue'),
                colors.to_hex('fuchsia'),
                colors.to_hex('tomato'),
                colors.to_hex('gold'),
                colors.to_hex('greenyellow'),
                colors.to_hex('mediumspringgreen')
                ]

for patch, color in zip(bp['boxes'], colors):
      patch.set_facecolor(color)

for median in bp['medians']:
    median.set(color ='black',
               linewidth = 1)

plt.xlabel("EC primer nivel")
plt.ylabel("Largo de secuencia", )
plt.savefig(f"{export_path}boxplot.png", transparent=True)

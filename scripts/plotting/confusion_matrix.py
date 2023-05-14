import json
import pandas as pd
import sys
import seaborn as sn
import matplotlib.pyplot as plt

# Execution example
# python 3 confusion_matrix.py ~/Desktop/results/ CNN_B esm 0 ~/Desktop/results/plot/

data_path = sys.argv[1]
architecture = sys.argv[2]
encoding = sys.argv[3]
scale = int(sys.argv[4])
export_path = sys.argv[5]

results_json = []
with open(f"{data_path}results_{architecture}/results_{encoding}_{scale}.json", "r") as f:
    results_json = json.load(f)

train_cm = results_json.pop('train_metrics').pop('confusion_matrix')
test_cm = results_json.pop('test_metrics').pop('confusion_matrix')

df_train = pd.DataFrame(train_cm, index=[i for i in [
    "Oxidoreductases", 
    "Tranfersaes", 
    "Hydrolases",
    "Lyases", 
    "Isomerases", 
    "Ligases", 
    "Translocases"
    ]], columns=[i for i in [ 
    "Oxidoreductases", 
    "Tranfersaes", 
    "Hydrolases",
    "Lyases", 
    "Isomerases", 
    "Ligases", 
    "Translocases"
    ]])
plt.figure(figsize=(10,7))
sn.heatmap(df_train, annot=True, cmap=sn.light_palette("seagreen", as_cmap=True))
plt.savefig(f"{export_path}heatmap_{architecture}_{encoding}_{scale}.png")


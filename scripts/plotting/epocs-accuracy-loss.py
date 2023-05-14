import matplotlib.pyplot as plt
import sys
import json
# Execution example
# 

data_path = sys.argv[1]
architecture = sys.argv[2]
encoding = sys.argv[3]
scale = int(sys.argv[4])
export_path = sys.argv[5]

results_json = []
with open(f"{data_path}{architecture}/{encoding}_scale_{scale}.json", "r") as f:
    results_json = json.load(f)

accuracy_history = results_json.pop('accuracy_history')
loss_history = results_json.pop('loss_history')

plt.plot(range(len(accuracy_history)), accuracy_history, label='Training Accuracy')
plt.plot(range(len(loss_history)), loss_history, label="Training Loss")
plt.savefig(f"{export_path}epochs_{architecture}_{encoding}_{scale}.png")


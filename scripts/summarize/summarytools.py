import pandas as pd
from tqdm import tqdm

tmp_data = []

def process_data(dataset: pd.DataFrame) -> list:
    ec_primary(dataset)
    return tmp_data

def ec_primary(dataset: pd.DataFrame):
    global tmp_data
    p = 1
    while True:
        ec_p = dataset.loc[dataset.str.startswith(str(p))]
        if len(ec_p) > 0:
            tmp_data.append([f"{p}.-.-.-",len(ec_p),'','',''])
            ec_secondary(ec_p, p)
            p += 1
        else:
            break
    return tmp_data

def ec_secondary(dataset: pd.DataFrame, p: int):
    global tmp_data
    secondary_list = dataset.str.split('.', n=2).str.get(1).unique()
    for s in tqdm(secondary_list,desc=f"Processing EC:{p}.-.-.-"):
        ec_s = dataset.loc[dataset.str.startswith(f"{str(p)}.{str(s)}.")]
        if len(ec_s) > 0:
            tmp_data.append([f"{p}.{s}.-.-",'',len(ec_s),'',''])
            ec_terciary(ec_s, p, s)

def ec_terciary(dataset: pd.DataFrame, p: int, s: int):
    global tmp_data
    terciary_list = dataset.str.split('.', n=3).str.get(2).unique()
    for t in terciary_list:
        ec_t = dataset.loc[dataset.str.startswith(f"{str(p)}.{str(s)}.{str(t)}.")]
        if len(ec_t) > 0:
            tmp_data.append([f"{p}.{s}.{t}.-",'','',len(ec_t),''])
            ec_quaternary(ec_t, p, s, t)

def ec_quaternary(dataset: pd.DataFrame, p: int, s: int, t: int):
    global tmp_data
    quaternary_list = dataset.str.split('.').str.get(-1).unique()
    for q in quaternary_list:
        ec_q = dataset.loc[dataset == f"{str(p)}.{str(s)}.{str(t)}.{str(q)}"]
        if len(ec_q) > 0:
            tmp_data.append([f"{p}.{s}.{t}.{q}",'','','',len(ec_q)])
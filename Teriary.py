#!/usr/bin/env python
# coding: utf-8



import pandas as pd
import os
import copy
from functools import wraps,partial
base_dir = os.getcwd()
t = "HBOND,VDW,PICATION,IONIC,SSBOND,PIPISTACK"
l = "MC_MC,MC_SC,SC_MC,SC_SC"
item_key= []
item_key1=[]#
dic_moudle = {"filename":""}
dic_moudle1 = {"filename":""}
for i in t.split(","):
    for j in l.split(","):
        dic_moudle[f"{i}:{j}"]=0
        item_key.append(f"{i}:{j}")

for i in t.split(","):
    dic_moudle1[f"{i}"]=0
    item_key1.append(f"{i}")

def scan(func=None, *, path=None):
    if func is None:
        return partial(scan, path=path)
    @wraps(func)
    def wrapper(path):
        ls_dir = os.listdir(path)
        for file_name in ls_dir:
            file_path = os.path.join(path,file_name)
            if os.path.isfile(file_path):
                if file_name.startswith("satpdb") and file_name.endswith(".txt"):
                    func(file_path)
            elif os.path.isdir(file_path):
                wrapper(file_path)
    return wrapper


out_list=[]   #输出考虑主链侧链的情况
out_list1=[]  #输出不考虑主链侧链的情况
@scan
def satpdb2csv(file_path):
    dic_one = copy.deepcopy(dic_moudle)
    dic_one1 = copy.deepcopy(dic_moudle1)
    with open(file_path,'r') as f:
        lines = f.readlines()
    dic_one["filename"]=os.path.basename(file_path)
    dic_one1["filename"]=os.path.basename(file_path)
    for i in lines:
        for key in item_key:
            if key in i:
                dic_one[key] += 1 
        for key in item_key1:
            if key in i:
                dic_one1[key] += 1  
    out_list.append(dic_one)
    out_list1.append(dic_one1)

satpdb2csv(base_dir)

obj = pd.DataFrame(out_list)
obj.to_csv(f"satpdb2csv.csv") 
obj1 = pd.DataFrame(out_list1)
obj1.to_csv(f"satpdb2csv_no.csv") 





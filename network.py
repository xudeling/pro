#!/usr/bin/env python
# coding: utf-8
import os
import numpy as np
import networkx as nx
import pandas as pd
import matplotlib.pyplot as plt

base_dir = os.path.dirname(os.path.abspath(__file__)) 
from functools import wraps, partial


def scan(func=None, *, path=None):
    if func is None:
        return partial(scan, path=path)

    @wraps(func)
    def wrapper(path):
        ls_dir = os.listdir(path)
        for file_name in ls_dir:
            file_path = os.path.join(path, file_name)
            if os.path.isfile(file_path):
                func(file_path)
            elif os.path.isdir(file_path):
                wrapper(file_path)

    return wrapper


def open_txt(path):
    with open(path, "r")as f:
        l = f.readlines()
    if len(l) == 1:
        return -1
    return l[1:]


def return_nodes(path):
    # 提取所有节点
    one = []
    content = open_txt(path)
    for oneline in content:
        oneline_list = oneline.split("\t")  
        node1 = oneline_list[0]  
        node2 = oneline_list[2]  
        one.append([node1, node2])
    return one


total_out_dic = {}
max_degree_dic = {}  # {'PHE':[23,11,5],'ALU':[12,5,8]...}
sec_max_degree_dic={}
max_closeness_centrality_dic = {}
max_between_centrality_dic={}
@scan
def Process(path):
    nodes = return_nodes(path)
    G = nx.Graph()  
    FileName = os.path.basename(path)
    G.add_edges_from(nodes)
    MG = nx.MultiGraph()  
    MG.add_edges_from(nodes)

    degree_dict = dict(MG.degree)  
    # print(degree_dict)
    closeness_centrality_dict = nx.closeness_centrality(G)  
    between_centrality_dict = nx.betweenness_centrality(G)  
    dic_calc = {} 
    for key in degree_dict:
        name = key.split(':')[3] 
        if name not in dic_calc: 
            dic_calc[name] = {'degree': [], 'closeness_centrality': [], 'betweenness_centrality': []}
        dic_calc[name]['degree'].append(degree_dict[key])
        dic_calc[name]['closeness_centrality'].append(closeness_centrality_dict[key])
        dic_calc[name]['betweenness_centrality'].append(between_centrality_dict[key])

    out_list = []  
    columns = ["node_name", "avg_degree", "avg_closeness_centrality", "avg_between_centrality"]

    for name in dic_calc:
        length = len(dic_calc[name]['degree'])  
        normal_length = len(dic_calc)  
        avg_digree = sum(dic_calc[name]['degree']) / length
        avg_closeness_centrality = sum(dic_calc[name]['closeness_centrality']) / length
        avg_between_centrality = sum(dic_calc[name]['betweenness_centrality']) / length
        one = [name, avg_digree / normal_length, avg_closeness_centrality / normal_length,
               avg_between_centrality / normal_length]

        out_list.append(one)
        del (one)
    print(out_list)
    ar = np.array(out_list)  
    # print(ar)
    columns0 = ar[:, 0]  
    columns1 = ar[:, 1] 
    columns2 = ar[:, 2]  
    columns3 = ar[:, 3] 
    index_array1 = columns1.argsort()[::-1]
    try:
        sec_index=index_array1[1]
    except Exception as e:
        sec_index=False
    max_columns1 = max(columns1) 
    max_columns2 = max(columns2)  
    max_columns3 = max(columns3) 
    max_columns1_index = (columns1.tolist()).index(max_columns1) 
    max_columns2_index = (columns2.tolist()).index(max_columns2) 
    max_columns3_index = (columns3.tolist()).index(max_columns3)  
    name1 = columns0[max_columns1_index] 


    if name1 not in max_degree_dic:
        max_degree_dic[name1] = [1,0]   
    else:
        max_degree_dic[name1][0]+= 1


    if sec_index != False:
        sec_name1 = columns0[sec_index]
        if sec_name1 not in max_degree_dic:  
            max_degree_dic[sec_name1]=[0,1]
        else:
            if len(max_degree_dic[sec_name1])<2: 
                max_degree_dic[sec_name1].append(1)
            else:
                max_degree_dic[sec_name1][1]+= 1  

    name2 = columns0[max_columns2_index]  
    #sec_name2=columns0[]
    if name2 not in max_closeness_centrality_dic:
        max_closeness_centrality_dic[name2] = 1
    else:
        max_closeness_centrality_dic[name2] += 1

    name3 = columns0[max_columns3_index]  
    if name3 not in max_between_centrality_dic:
        max_between_centrality_dic[name3] = 1
    else:
        max_between_centrality_dic[name3] += 1


    total_out_dic[os.path.basename(path)] = out_list
    df = pd.DataFrame(columns=columns, data=out_list)
    basename = FileName.replace(".txt", "2020wwwnetwork_avg_normal.csv") 
    out_path = os.path.join(base_dir, "2020wwwnetwork_Avg_Normal_result")  
    if not os.path.exists(out_path):
        os.makedirs(out_path)
    obj_path = os.path.join(out_path, basename)
    df.to_csv(obj_path, encoding='utf-8')
#max_degree_list.append(max_degree_dic[name1])

if __name__ == '__main__':
    Process(r'E:\研究生文献\我的课题2020\整理的数据\三级结构PDB\统计主链侧链中氢键范德华等作用力\results-antiCancer-pdbobj_txt\a\b')

    # print(max_degree_dic)
    df1 = pd.DataFrame.from_dict(columns=['max_degree','sec_degree'],data=max_degree_dic,orient='index') 
    df2 = pd.DataFrame(columns=['name', 'closeness_centrality'], data=list(max_closeness_centrality_dic.items()))
    df3 = pd.DataFrame(columns=['name', 'between_centrality'], data=list(max_between_centrality_dic.items()))
    basename1 = "total_max_degree_result2.csv"
    basename2 = "total_max_closeness_centrality_result2.csv"
    basename3 = "total_max_between_centrality_result2.csv"
    out_path = os.path.join(base_dir, "total_max_degree_result2")  
    if not os.path.exists(out_path):  
        os.makedirs(out_path)
    obj_path = os.path.join(out_path, basename1)
    df1.to_csv(obj_path, encoding='utf-8')
    obj_path = os.path.join(out_path, basename2)
    df2.to_csv(obj_path, encoding='utf-8')
    obj_path = os.path.join(out_path, basename3)
    df3.to_csv(obj_path, encoding='utf-8')

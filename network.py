#!/usr/bin/env python
# coding: utf-8
import os
import numpy as np
import networkx as nx
import pandas as pd
import matplotlib.pyplot as plt

base_dir = os.path.dirname(os.path.abspath(__file__))  # 获取当前目录
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
        oneline_list = oneline.split("\t")  # 以空格作为切分
        node1 = oneline_list[0]  # 取第一个残基节点
        node2 = oneline_list[2]  # 取第二个残基节点
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
    G = nx.Graph()  # 用来统计接近中心性和介数中心性（重复的边只计算一次）
    FileName = os.path.basename(path)
    G.add_edges_from(nodes)
    MG = nx.MultiGraph()  # 多重图，用来统计度数（重复的边也计算）
    MG.add_edges_from(nodes)

    degree_dict = dict(MG.degree)  # 度 返回的是一个字典
    # print(degree_dict)
    closeness_centrality_dict = nx.closeness_centrality(G)  # 接近中心度，返回的是一个字典
    between_centrality_dict = nx.betweenness_centrality(G)  # 介数中心性，返回的是一个字典
    dic_calc = {}  # 字典里面嵌套字典dic_calc={'PHE':{'degree':[2，1，3],'closeness_centrality':[6，2，3],'betweenness_centrality':[3，2，4]}，'LEU':{'degree':[]...}
    for key in degree_dict:
        name = key.split(':')[3]  # 以冒号作为切分，取第三个冒号和第四个冒号之间的残基
        if name not in dic_calc:  # 如果残基不存在，就创建一个残基列表
            dic_calc[name] = {'degree': [], 'closeness_centrality': [], 'betweenness_centrality': []}
        # 如果残基存在，把残基对应的度数、接近中心性、介数中心性添加进来
        dic_calc[name]['degree'].append(degree_dict[key])
        dic_calc[name]['closeness_centrality'].append(closeness_centrality_dict[key])
        dic_calc[name]['betweenness_centrality'].append(between_centrality_dict[key])

    out_list = []  # 存放归一化之后的数据
    # 标题
    columns = ["node_name", "avg_degree", "avg_closeness_centrality", "avg_between_centrality"]

    for name in dic_calc:
        length = len(dic_calc[name]['degree'])  # 同一个残基 出现次数
        normal_length = len(dic_calc)  # 归一化节点个数
        avg_digree = sum(dic_calc[name]['degree']) / length
        avg_closeness_centrality = sum(dic_calc[name]['closeness_centrality']) / length
        avg_between_centrality = sum(dic_calc[name]['betweenness_centrality']) / length
        # 计算归一化之后的数据
        one = [name, avg_digree / normal_length, avg_closeness_centrality / normal_length,
               avg_between_centrality / normal_length]

        out_list.append(one)
        del (one)
    print(out_list)
    ar = np.array(out_list)  # 直接提取某一列会报错，需要将list形式的outlist转化为数组形式的ar
    # print(ar)
    columns0 = ar[:, 0]  # 提取out_list的第1列数据
    columns1 = ar[:, 1]  # 提取out_list的第2数据
    columns2 = ar[:, 2]  # 提取out_list的第3数据
    columns3 = ar[:, 3]  # 提取out_list的第4数据
    index_array1 = columns1.argsort()[::-1]
    try:
        sec_index=index_array1[1]
    except Exception as e:
        sec_index=False
    max_columns1 = max(columns1)  # 第一列（度数）的最大值
    max_columns2 = max(columns2)  # 第二列（接近中心性）的最大值
    max_columns3 = max(columns3)  # 第三列（介数中心性）的最大值
    max_columns1_index = (columns1.tolist()).index(max_columns1)  # 获取度数最大值的索引,tolist()把numpy里面数组转化为python中的list
    max_columns2_index = (columns2.tolist()).index(max_columns2)  #获取接近中心性最大值的索引
    max_columns3_index = (columns3.tolist()).index(max_columns3)  #获取介数中心性最大值的索引
    name1 = columns0[max_columns1_index]  # 获取度数最大值对应的残基


    if name1 not in max_degree_dic:
        max_degree_dic[name1] = [1,0]    #没有次大，最大第一次在字典max_degree_dic中出现
    else:
        max_degree_dic[name1][0]+= 1


    if sec_index != False:
        sec_name1 = columns0[sec_index]
        if sec_name1 not in max_degree_dic:   #没有最大,，次大第一次在字典max_degree_dic中出现
            max_degree_dic[sec_name1]=[0,1]
        else:
            if len(max_degree_dic[sec_name1])<2: #列表长度小于2表示有最大，次大第一次出现
                max_degree_dic[sec_name1].append(1)
            else:
                max_degree_dic[sec_name1][1]+= 1  #否则有最大，次大出现过了

    name2 = columns0[max_columns2_index]  # 获取接近中心性最大值对应的残基
    #sec_name2=columns0[]
    if name2 not in max_closeness_centrality_dic:
        max_closeness_centrality_dic[name2] = 1
    else:
        max_closeness_centrality_dic[name2] += 1

    name3 = columns0[max_columns3_index]  # 获取介数中心性最大值对应的残基
    if name3 not in max_between_centrality_dic:
        max_between_centrality_dic[name3] = 1
    else:
        max_between_centrality_dic[name3] += 1


    total_out_dic[os.path.basename(path)] = out_list
    df = pd.DataFrame(columns=columns, data=out_list)
    basename = FileName.replace(".txt", "2020wwwnetwork_avg_normal.csv")  # 输出单个文件名
    out_path = os.path.join(base_dir, "2020wwwnetwork_Avg_Normal_result")  # 修改这个是输出目录
    if not os.path.exists(out_path):  # 如果目录不存在则创建新目录
        os.makedirs(out_path)
    obj_path = os.path.join(out_path, basename)
    df.to_csv(obj_path, encoding='utf-8')
#max_degree_list.append(max_degree_dic[name1])

if __name__ == '__main__':
    Process(r'E:\研究生文献\我的课题2020\整理的数据\三级结构PDB\统计主链侧链中氢键范德华等作用力\results-antiCancer-pdbobj_txt\a\b')

    # print(max_degree_dic)
    df1 = pd.DataFrame.from_dict(columns=['max_degree','sec_degree'],data=max_degree_dic,orient='index')  #orient是把字典转置
    df2 = pd.DataFrame(columns=['name', 'closeness_centrality'], data=list(max_closeness_centrality_dic.items()))
    df3 = pd.DataFrame(columns=['name', 'between_centrality'], data=list(max_between_centrality_dic.items()))
    basename1 = "total_max_degree_result2.csv"
    basename2 = "total_max_closeness_centrality_result2.csv"
    basename3 = "total_max_between_centrality_result2.csv"
    out_path = os.path.join(base_dir, "total_max_degree_result2")  # 修改这个是输出目录
    if not os.path.exists(out_path):  # 如果目录不存在则创建新目录
        os.makedirs(out_path)
    obj_path = os.path.join(out_path, basename1)
    df1.to_csv(obj_path, encoding='utf-8')
    obj_path = os.path.join(out_path, basename2)
    df2.to_csv(obj_path, encoding='utf-8')
    obj_path = os.path.join(out_path, basename3)
    df3.to_csv(obj_path, encoding='utf-8')

    print(111)
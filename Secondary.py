
import os
import csv
from functools import wraps,partial

import pandas as pd
base_dir = os.path.abspath('.')
csv_path=os.path.join(base_dir,'csv')
total_to_csv_list=[]
#么有就创建一
if os.path.exists(csv_path) is False:
    os.makedirs(csv_path)
def scan(func=None, *, path=None):
    if func is None:
        return partial(scan, path=path)
    @wraps(func)
    def wrapper(path):
        ls_dir = os.listdir(path)
        for file_name in ls_dir:
            file_path = os.path.join(path,file_name)
            if os.path.isfile(file_path):
                # if file_name.split('.')[-1] == 'xml':
                # '''在这里判断是否是xml文件'''
                func(file_path)
            elif os.path.isdir(file_path):
                wrapper(file_path)
    return wrapper

file_path = os.path.join(base_dir,"5860e713-ab4a-4b1e-9f66-d7903de5089e.dssp")
@scan
def read_dssp(file_path):
    if file_path.endswith(".dssp"):
        total_one=['', 0, 0, 0, 0, 0, 0, 0, 0]#'filename','H','G',"I",'E','B',"T","S","C"
        filename = os.path.basename(file_path)
        total_one[0]=filename #文件名
        """读取dssp文件生成列表"""
        to_csv_list=[]
        onerows=[]
        with open(file_path,'r')as f:
            i = 1#行数
            j = 1#列数
            for oneline in f.readlines():
                if(i>=29):#行数大于29才是想要的数据
                    for column in oneline[1:]:#对每一行中的所有数据进行筛选 只提取第13列 的AA 和16列的structure
                        if(j==13):#13就是AA对应的那一列
                            a=column
                            onerows=[]
                            onerows.append(a)
                        if(j==16):#16就是Structure的第一列
                            # if column !=' ':#如果structure不为空格则添加 该方案暂时不执行需确认
                            b=column
                            onerows.append(b)
                            print(b,type(b))
                            to_csv_list.append(onerows)
                            del onerows
                        j+=1
                    j=1#一行结束需要重新计数
                i+=1
# 前面是基本文件提取工作
        dic_structure={} #说明dic_struceure是处理structure这一列中元素个数的问题 类似于dic_structure['H']=3
        for one in to_csv_list:
            if one[1]==' ':#如果是空格则不统计个数
                if dic_structure.get(one[1]):#如果已经有这个元素了那么久直接计数值加一
                    dic_structure[one[1]] += 1
                else:
                    dic_structure[one[1]] = 1#不存在则创建一个1
            if one[1]=='H':
                total_one[1] += 1 #H
            elif one[1] == 'G':
                total_one[2] += 1 #G
            elif one[1] == 'I':
                total_one[3] += 1 #I
            elif one[1] == 'E':
                total_one[4] += 1 #E
            elif one[1] == 'B':
                total_one[5] += 1 #B
            elif one[1] == 'T':
                total_one[6] += 1 #T
            elif one[1] == 'S':
                total_one[7] += 1 #S
            elif one[1] == 'C':
                total_one[8] += 1 #C

        dic_aa={}#处理AA STRUCTURE 精密性
        for one in to_csv_list:
            #print(dic_aa.get(one[0]))
            if dic_aa.get(one[0]) is None:
                dic_aa[one[0]]={}#创建AA字典
            if dic_aa[one[0]].get(one[1]):
                dic_aa[one[0]][one[1]]+=1
            else:
                dic_aa[one[0]][one[1]]=1
        columns_key = ['AA', 'STRUCTURE',"占比例", "联系紧密性"]
#第三列
        struct_ = sorted(dic_structure.items(),key=lambda x:x[1],reverse=True)#由大到小比例排序

        #@Todo 需要添加一步就是删除' '

        # if struct_[0][0]!=' ':
        #     pos=0
        #     total_one.append(struct_[0][0])
        # else:
        #     pos=1#如果第一个为''那么第二个就是要统计的数据直接指定位置
        #     total_one.append(struct_[1][0])
        # print(total_one)

        j=0
        # sum=0
        for i in range(len(struct_)):
            # if struct_[i][0]!=' ':
                # sum+=struct_[i][1]
            to_csv_list[i].append(struct_[i])
            j=i+1

        # total_one.append(struct_[pos][1]/sum)
        #求比例
        # for i in range(1,len(total_one)):
        #     sum += total_one[i]
        # # total_one[9]=sum#这里只是做一个测试 后期需要删除sum
        # for i in range(1,len(total_one)):
        #     total_one[i]=total_one[i]/sum

        total_to_csv_list.append(total_one)
        del total_one

        for i in range(len(to_csv_list)-len(struct_)):
            to_csv_list[j].append('')
            j+=1

        j=0
# #第四列
#         for i in dic_aa:
#             a = sorted(dic_aa[i].items(),key=lambda x:x[1],reverse=True)[0]#字典排序 从大到小
#             to_csv_list[j].append((i,a))
#             j+=1
#         dataFrame = pd.DataFrame(data=to_csv_list, index=None, columns=columns_key)


#         filename=os.path.join(csv_path, filename)
#         with open(f"{filename}-gbk.csv", "w", encoding="gbk",newline='') as f:
#                 dataFrame.to_csv(f, index=None)
#         with open(f"{filename}-utf8.csv", "w", encoding="UTF-8",newline='') as f:
#                 dataFrame.to_csv(f, index=None)

if __name__ == '__main__':
    read_dssp(base_dir)


    filename = 'total'
    columns_key=['filename','H','G',"I",'E','B',"T","S","C"]
    dataFrame = pd.DataFrame(data=total_to_csv_list, index=None, columns=columns_key)
    with open(f"{filename}-gbk.csv", "w", encoding="gbk", newline='') as f:
        dataFrame.to_csv(f, index=None)
    with open(f"{filename}-utf8.csv", "w", encoding="UTF-8", newline='') as f:
        dataFrame.to_csv(f, index=None)
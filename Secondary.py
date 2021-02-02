import os
import csv
from functools import wraps,partial
import pandas as pd
base_dir = os.path.abspath('.')
csv_path=os.path.join(base_dir,'csv')
total_to_csv_list=[]
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
        total_one[0]=filename 
        to_csv_list=[]
        onerows=[]
        with open(file_path,'r')as f:
            i = 1
            j = 1
            for oneline in f.readlines():
                if(i>=29):
                    for column in oneline[1:]:
                        if(j==13):
                            a=column
                            onerows=[]
                            onerows.append(a)
                        if(j==16):
                            # if column !=' ':
                            b=column
                            onerows.append(b)
                            print(b,type(b))
                            to_csv_list.append(onerows)
                            del onerows
                        j+=1
                    j=1
                i+=1

        dic_structure={} 
        for one in to_csv_list:
            if one[1]==' ':
                if dic_structure.get(one[1]):
                    dic_structure[one[1]] += 1
                else:
                    dic_structure[one[1]] = 1
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

        dic_aa={}
        for one in to_csv_list:
            #print(dic_aa.get(one[0]))
            if dic_aa.get(one[0]) is None:
                dic_aa[one[0]]={}
            if dic_aa[one[0]].get(one[1]):
                dic_aa[one[0]][one[1]]+=1
            else:
                dic_aa[one[0]][one[1]]=1
        columns_key = ['AA', 'STRUCTURE',"占比例", "联系紧密性"]
        struct_ = sorted(dic_structure.items(),key=lambda x:x[1],reverse=True)

        j=0
        # sum=0
        for i in range(len(struct_)):
            # if struct_[i][0]!=' ':
                # sum+=struct_[i][1]
            to_csv_list[i].append(struct_[i])
            j=i+1

        # total_one.append(struct_[pos][1]/sum)
        # for i in range(1,len(total_one)):
        #     sum += total_one[i]
        # # total_one[9]=sum
        # for i in range(1,len(total_one)):
        #     total_one[i]=total_one[i]/sum

        total_to_csv_list.append(total_one)
        del total_one

        for i in range(len(to_csv_list)-len(struct_)):
            to_csv_list[j].append('')
            j+=1

        j=0

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
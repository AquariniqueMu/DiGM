'''
Description: 调用gravity类的主函数
Author: Junwen Yang
Date: 2022-06-26 23:08:21
LastEditTime: 2023-03-05 15:07:34
LastEditors: Junwen Yang
'''

import numpy as np
import networkx as nx
import math
import pandas as pd
# import cross_intensity_matrix as cim
import matplotlib.pyplot as plt        
import graph_create as gc
import kshell as ksh
import gravity as grv
import os
from openpyxl import load_workbook
# import inspect
import tools_func as tf
# import mfim
# import methods
import baseline as bl
import time
from alive_progress import alive_bar




'''
Description: 调用edgelist文件的便捷工具
Author: Junwen Yang
Date: 2022-06-26 23:08:21
LastEditTime: 2022-10-13 15:06:16
LastEditors: Junwen Yang
'''

class network_edgelist():
    s  = "stormofswords"
    m  = "MesselShale_foodweb"
    n  = "netscience"
    o  = "out"
    c  = "cora"
    e  = "email"
    j  = "Jazz"
    g115 = 'gre_115'
    g185 = 'gre_185'
    g343 = 'gre_343'
    g512 = 'gre_512'
    g1107 = 'gre_1107'
    c8 = 'cage8'
    c9 = 'cage9'
    bit = 'bitcoinalpha'
    ca = 'Cattle–cattle dominances'
    mo = 'moreno_health'
    wiki = 'Wiki-Vote'
    twir = 'twitterreferendum'
    email = 'email-Eu-core'
    



'''
Description: 运行函数，用于计算单个网络的中心性分数和排名，并写入表格
Author: Junwen Yang
Date: 2022-06-26 23:08:21
LastEditTime: 2022-10-13 15:06:16
LastEditors: Junwen Yang
'''

def run(graph, file_name):
    # 为当前网络创建文件夹
    path = f"./{graph}"
    if not os.path.exists(path):
        os.mkdir(path)

    # 调用 graph_create 生成网络
    graph_class = gc.graph_create('./data/'+graph)
    G = graph_class.G
    A = graph_class.A
    # print(G.edges(data=True))

    # 所有的计算结果都以 {node: score} 的形式写入字典
    scores = {}
    rank_list = {}
    durations = {}
    # 计算中心性方法的分数
    methods = ["DiGM", "GMM", "GGC", "KSGC", "DC", "CC", "ODC", "KS","LGC"]
    with alive_bar(len(methods),title='Centrality Calculation...',bar='blocks') as bar:
        for centrality in methods:
            print(f"--------------------------{graph}: {centrality}----------------------------")
            start = time.perf_counter()
            score = calculate_centrality(G, centrality) # 计算中心性分数
            rank = get_rank_list(score) # 计算中心性排名
            rank_list[centrality] = rank    # 将排名写入字典
            scores[centrality] = score  # 将分数写入字典
            end = time.perf_counter()   
            duration = end - start    # 计算运行时间
            print(f"Duration: {duration}s")
            durations[centrality] = duration
            bar()

    # 将原始结果数据写入.xlsx文件
    df = pd.DataFrame.from_dict(scores)
    with pd.ExcelWriter(file_name[0], mode='a', engine="openpyxl") as writer:
        df.to_excel(writer, sheet_name=graph)


    # 根据分数 dict 生成排名 list
    df_rank = pd.DataFrame(rank_list, index=scores.keys(), columns=[])
    with pd.ExcelWriter(file_name[1], mode='a', engine="openpyxl") as writer:
        df_rank.to_excel(writer, sheet_name=graph)

    # 将计算时间写入 .xlsx 文件
    time_df = pd.DataFrame({"Duration": list(durations.values())})
    with pd.ExcelWriter(file_name[2], mode='a', engine="openpyxl") as writer:
        time_df.to_excel(writer, sheet_name=graph)

def calculate_centrality(G, centrality):
    if centrality == "DiGM":
        switch_mass, switch_co, switch_dist = "density", "cc", "calc"
        score = grv.gravity_model(G, switch_mass, switch_co, switch_dist).centrality
    elif centrality == "DC":
        score = nx.degree_centrality(G)
    elif centrality == "CC":
        score = nx.closeness_centrality(G.reverse())
    elif centrality == "ODC":
        score = nx.out_degree_centrality(G)
    elif centrality == "KS":
        score = ksh.kshell(G)
    elif centrality == "GMM":
        score = bl.GMM(G)
    elif centrality == "GGC":
        score = bl.GGC(G)
    elif centrality == "KSGC":
        score = bl.KSGC(G)
    elif centrality == "LGC":
        score = bl.LGC(G)

 
    return score

def get_rank_list(score_dict):
    score_sorted = dict(sorted(score_dict.items(), key = lambda x:x[1], reverse = True))
    return score_sorted.keys()

    
    
import datetime


def main():
    '''
    Description: 主函数，用于调整模型结构、文件名、测试网络数量
    '''
    now = datetime.datetime.now()
    date_string = now.strftime('%m-%d_%H-%M')
    # 储存节点分数的文件名
    filepath = "./results/centrality/"
    file_name = filepath+'all_centrality_score'+date_string+'.xlsx'
    # 储存节点排名的文件名 
    rank_file_name = filepath+'all_centrality_rank'+date_string+'.xlsx'
    time_file_name = filepath+'all_centrality_time'+date_string+'.xlsx'
    file_name_list = [file_name, rank_file_name, time_file_name]
    # 生成两个空的.xlsx表格文件
    df = pd.DataFrame() 
    df.to_excel(file_name_list[0])
    df.to_excel(file_name_list[1])
    df.to_excel(file_name_list[2])


    # -----------------------------------------------------调节网络数量，调用run()进行计算-------------------------------------
    for graph_name in [
        network_edgelist.s,
        network_edgelist.m,
        network_edgelist.bit,
        network_edgelist.ca,
        network_edgelist.mo
        ]:
        print("\n========================================Running network "+graph_name+"========================================\n")
        run(graph_name, file_name_list)

    # ---------------------------------------------------结束写入---------------------------------------------------------------

    
if __name__=='__main__':
    main()
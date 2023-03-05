'''
Description: 调用gravity类的主函数
Author: Junwen Yang
Date: 2022-06-26 23:08:21
LastEditTime: 2023-03-05 11:52:29
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



'''
Description: 运行函数，用于计算单个网络的中心性分数和排名，并写入表格
Author: Junwen Yang
Date: 2022-06-26 23:08:21
LastEditTime: 2022-10-13 15:06:16
LastEditors: Junwen Yang
'''

def run(graph, file_name, xlsx, xlsx_rank, xlsx_time):
    # 为当前网络创建文件夹
    path = f"./{graph}"
    if not os.path.exists(path):
        os.mkdir(path)

    # 调用 graph_create 生成网络
    graph_class = gc.graph_create(graph)
    G = graph_class.G
    A = graph_class.A
    print(G.edges(data=True))

    # 所有的计算结果都以 {node: score} 的形式写入字典
    scores = {}
    durations = {}
    # 计算中心性方法的分数
    for centrality in ["DiGM", "GMM", "GGC", "KSGC", "DC", "CC", "ODC", "KS"]:
        print(f"--------------------------{graph}: {centrality}----------------------------")
        start = time.perf_counter()
        score = calculate_centrality(G, centrality)
        scores[centrality] = score
        end = time.perf_counter()
        duration = end - start
        # print(f"Duration: {durations}")
        durations[centrality] = duration

    # 将原始结果数据写入.xlsx文件
    df = pd.DataFrame.from_dict(scores)
    df.to_excel(xlsx, sheet_name=graph)

    # 根据分数 dict 生成排名 list
    score_list = list(scores.values())
    rank_list = get_rank_list(score_list)
    df_rank = pd.DataFrame(rank_list, index=scores.keys(), columns=["Rank"])
    df_rank.to_excel(xlsx_rank, sheet_name=graph)

    # 将计算时间写入 .xlsx 文件
    time_df = pd.DataFrame({"Duration": list(durations.values())})
    time_df.to_excel(xlsx_time, sheet_name=graph)

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
    elif centrality == "iWVR":
        score = bl.improved_wvoterank(G)
    elif centrality == "WPR":
        score = bl.weighted_pagerank(G)
    return score

def get_rank_list(score_list):
    rank_list = [sorted(score_list, reverse=True).index(score)+1 for score in score_list]
    return rank_list

    
    
    


def main():
    '''
    Description: 主函数，用于调整模型结构、文件名、测试网络数量
    '''
    # -----------------------------------------------------调节模型所采用的指标----------------------------------------------------
   
    
    # -----------------------------------------------------文件读写前置处理--------------------------------------------------------
    # 储存节点分数的文件名
    filepath = "2022-11-13"
    if not os.path.exists(filepath):
        os.mkdir(filepath)
    method = 'R-ks'
    file_name = filepath+'/'+'DiGM-1113-score'+method
    # 储存节点排名的文件名
    rank_file_name = filepath+'/'+'DiGM-1113-rank'+method
    time_file_name = filepath+'/'+'DiGM-1113-time'+method
    # 生成两个空的.xlsx表格文件
    df = pd.DataFrame() 
    df.to_excel(file_name+'.xlsx')
    df.to_excel(rank_file_name+'.xlsx')
    df.to_excel(time_file_name+'.xlsx')
    # 准备两个写入表格用的ExcelWriter类
    xlsx = pd.ExcelWriter(file_name+'.xlsx')
    xlsx_rank = pd.ExcelWriter(rank_file_name+'.xlsx')
    xlsx_time = pd.ExcelWriter(time_file_name+'.xlsx')

    # -----------------------------------------------------调节网络数量，调用run()进行计算-------------------------------------
    for graph_name in [
        network_edgelist.s,
        network_edgelist.m,
        network_edgelist.bit,
        network_edgelist.ca,
        network_edgelist.mo
        ]:
        print("\n========================================Running network "+graph_name+"========================================\n")
        run(graph_name, file_name, xlsx, xlsx_rank,xlsx_time)

    # ---------------------------------------------------结束写入---------------------------------------------------------------
    xlsx.close()
    xlsx_rank.close()
    xlsx_time.close()
    
    
if __name__=='__main__':
    main()
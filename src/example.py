'''
Description: 
Author: Junwen Yang
Date: 2023-02-13 11:09:48
LastEditTime: 2023-03-05 19:11:20
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

def build_graph():
    # 初始化网络
    G = nx.DiGraph()

    # 添加18个节点
    for i in range(1,18,1):
        G.add_node(i)

    # 添加节点之间的有向边
    # for i in range(17):
    #     for j in range(i + 1, 18):
    #         G.add_edge(i, j)

    # G.add_edge(1,2)
    # G.add_edge(1,3)
    # G.add_edge(1,4)
    # G.add_edge(1,5)
    # G.add_edge(1,6)

    # TODO:其他方法的识别结果，特别是ODC 
    # TODO：1到3节点的连边反向
    G.add_edges_from([(1,2),(3,1),(1,4),(1,5)])
    G.add_edges_from([(2,6),(2,7),(2,8)])
    G.add_edges_from([(3,13)])
    G.add_edges_from([(4,10),(4,11),(4,12)])
    G.add_edges_from([(5,9)])
    G.add_edges_from([(7,14),(7,15)])
    G.add_edges_from([(9,16)])
    G.add_edges_from([(11,17)])
    G.add_edges_from([(12,18)])
    G.add_edges_from([(14,13),(8,9),(16,4),(13,4)])

    return G



# print(DiGM)

def run(graph, file_name):
    # 为当前网络创建文件夹
    
    G = build_graph()
    
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
    df_rank = pd.DataFrame(rank_list, columns=methods)
    with pd.ExcelWriter(file_name[1], mode='a', engine="openpyxl") as writer:
        df_rank.to_excel(writer, sheet_name=graph)

    # 将计算时间写入 .xlsx 文件
    time_df = pd.DataFrame({"Duration": list(durations.values())}, index=list(durations.keys()))
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
    filepath = "./results/example/"
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
    for graph_name in ['example']:
        print("\n========================================Running network "+"========================================\n")
        run(graph_name, file_name_list)

    # ---------------------------------------------------结束写入---------------------------------------------------------------

    
if __name__=='__main__':
    main()
'''
Description: 调用gravity类的主函数
Author: Junwen Yang
Date: 2022-06-26 23:08:21
LastEditTime: 2023-02-09 22:10:02
LastEditors: Junwen Yang
'''

import numpy as np
import networkx as nx
import math
import pandas as pd
import cross_intensity_matrix as cim
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
    twi = 'twitter'
    twir = 'twitterreferendum'
    wiki = 'Wiki-Vote'



'''
Description: 运行函数，用于计算单个网络的中心性分数和排名，并写入表格
Author: Junwen Yang
Date: 2022-06-26 23:08:21
LastEditTime: 2022-10-13 15:06:16
LastEditors: Junwen Yang
'''

def run(graph, file_name, xlsx, xlsx_rank,xlsx_time):
    
    # -----------------------------------------------------为当前网络创建文件夹-----------------------------------------------------
    path = "./"+graph
    if not os.path.exists(path):
        os.mkdir(path)
    
    # -----------------------------------------------------调用graph_create生成网络------------------------------------------------
    graph_class = gc.graph_create(graph)
    G = graph_class.G
    A = graph_class.A
    
    # -----------------------------------------------------计算所有中心性方法的分数-------------------------------------------------
    # 所有的计算结果都以 {node: score} 的形式写入字典


    print('--------------------------'+graph+': DiGM----------------------------')
    start = time.perf_counter()
    switch_mass = 'density'
    switch_co = 'cc'
    switch_dist = 'calc'
    DiGM_1 = grv.gravity_model(A, G, graph,switch_mass,switch_co,switch_dist).centrality
    # DiGM_1 = bl.improved_wvoterank(G)
    # DiGM_1 = bl.weighted_PageRank(G.reverse())
    # DiGM_1 = nx.closeness_centrality(G.reverse())
    # DiGM_1 = tf.digm_pagerank_scipy(G.reverse(),init_score=list(DiGM_1.values()),alpha=0.85,max_iter=600000)
    # print(list(DiGM_1.values()))
    end = time.perf_counter()
    duration_DiGM_1 = end - start
    
    
    # -----------------------------------------------------将原始结果数据写入.xlsx文件---------------------------------------------
    df_digm = pd.DataFrame.from_dict(DiGM_1,orient='index',columns=['DiGM'])
    df_digm.to_excel(xlsx,sheet_name = graph)
    # -----------------------------------------------------根据分数dict生成排名list------------------------------------------------

    
    
    score_list = [DiGM_1]
    df_duration = pd.DataFrame(columns=['DiGM'])
    df_duration.loc[0] = [duration_DiGM_1]
    print(df_duration)
    df_duration.to_excel(xlsx_time,sheet_name=graph)
    
    df_rank = pd.DataFrame()
    # 对字典进行排序并获取排序后的 keys ，即分数降序排列后的节点id，并以Dataframe形式写入.xlsx文件
    for i in range(len(score_list)):
        dict_sorted = dict(sorted(score_list[i].items(), key = lambda x:x[1], reverse = True))
        rank_list = dict_sorted.keys()
        df_item = pd.DataFrame(rank_list, columns=['DiGM'])
        df_rank = pd.concat([df_rank, df_item], axis = 1)
    df_rank.to_excel(xlsx_rank, sheet_name=graph)
    
    
    


def main():
    '''
    Description: 主函数，用于调整模型结构、文件名、测试网络数量
    '''
    # -----------------------------------------------------调节模型所采用的指标----------------------------------------------------
    
    
    # -----------------------------------------------------文件读写前置处理--------------------------------------------------------
    # 储存节点分数的文件名
    filepath = "2023-02-09"
    if not os.path.exists(filepath):
        os.mkdir(filepath)
    method = ''
    file_name = filepath+'/'+'-score'+method
    # 储存节点排名的文件名
    rank_file_name = filepath+'/'+'-rank'+method
    time_file_name = filepath+'/'+'-time'+method
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
        network_edgelist.mo
        # network_edgelist.twir,
        # network_edgelist.wiki
        ]:
        print("\n========================================Running network "+graph_name+"========================================\n")
        run(graph_name, file_name, xlsx, xlsx_rank,xlsx_time)

    # ---------------------------------------------------结束写入---------------------------------------------------------------
    xlsx.close()
    xlsx_rank.close()
    xlsx_time.close()
    
    
if __name__=='__main__':
    main()
'''
Description: 调用gravity类的主函数
Author: Junwen Yang
Date: 2022-06-26 23:08:21
LastEditTime: 2023-02-26 18:41:01
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
    phy = 'physicians'
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
    print(G.edges(data=True))

    
    # -----------------------------------------------------计算所有中心性方法的分数-------------------------------------------------
    # 所有的计算结果都以 {node: score} 的形式写入字典


    print('--------------------------'+graph+': DiGM----------------------------')
    start = time.perf_counter()
    switch_mass = 'density'
    switch_co = 'cc'
    switch_dist = 'calc'
    DiGM = grv.gravity_model(A, G, graph,switch_mass,switch_co,switch_dist).centrality
    end = time.perf_counter()
    duration_DiGM = end - start
    print('--------------------------'+graph+': DC----------------------------')
    start = time.perf_counter()
    DC = nx.degree_centrality(G)
    end = time.perf_counter()
    duration_DC = end - start
    # print('--------------------------'+graph+': BC----------------------------')
    # start = time.perf_counter()
    # BC = nx.betweenness_centrality(G)
    # end = time.perf_counter()
    # duration_BC = end - start
    print('--------------------------'+graph+': CC----------------------------')
    start = time.perf_counter()
    CC = nx.closeness_centrality(G.reverse())
    end = time.perf_counter()
    duration_CC = end - start
    print('--------------------------'+graph+': ODC----------------------------')
    start = time.perf_counter()
    ODC = nx.out_degree_centrality(G)
    end = time.perf_counter()
    duration_ODC = end - start
    print('--------------------------'+graph+': K-shell----------------------------')
    start = time.perf_counter()
    KS = ksh.kshell(G)
    end = time.perf_counter()
    duration_KS = end - start
    start = time.perf_counter()
    # print('--------------------------'+graph+': GM----------------------------')
    # start = time.perf_counter()
    # GM = bl.GM(G)
    # end = time.perf_counter()
    # duration_GM = end - start
    # print('--------------------------'+graph+': KGM----------------------------')
    # start = time.perf_counter()
    # KGM = bl.KGM(G)
    # end = time.perf_counter()
    # duration_KGM = end - start
    print('--------------------------'+graph+': GMM----------------------------')
    start = time.perf_counter()
    GMM = bl.GMM(G)
    end = time.perf_counter()
    duration_GMM = end - start
    print('--------------------------'+graph+': GGC----------------------------')
    start = time.perf_counter()
    GGC = bl.GGC(G)
    end = time.perf_counter()
    duration_GGC = end - start
    print('--------------------------'+graph+': KSGC----------------------------')
    start = time.perf_counter()
    KSGC = bl.KSGC(G)
    end = time.perf_counter()
    duration_KSGC = end - start
    # print('--------------------------'+graph+': EffG----------------------------')
    # start = time.perf_counter()
    # EFFG = bl.EffG(G,graph)
    # end = time.perf_counter()
    # duration_EFFG = end - start

    # -----------------------------------------------------将原始结果数据写入.xlsx文件---------------------------------------------
    df_digm = pd.DataFrame.from_dict(DiGM,orient='index',columns=['DiGM'])
    df_DC = pd.DataFrame.from_dict(DC,orient='index',columns=['DC'])
    # df_BC = pd.DataFrame.from_dict(BC,orient='index',columns=['BC'])
    df_CC = pd.DataFrame.from_dict(CC,orient='index',columns=['CC'])
    df_ODC = pd.DataFrame.from_dict(ODC,orient='index',columns=['ODC'])
    df_KS = pd.DataFrame.from_dict(KS,orient='index',columns=['KShell'])
    # df_GM = pd.DataFrame.from_dict(GM,orient='index',columns=['GM'])
    # df_KGM = pd.DataFrame.from_dict(KGM,orient='index',columns=['KGM'])
    df_GMM = pd.DataFrame.from_dict(GMM,orient='index',columns=['GMM'])
    df_GGC = pd.DataFrame.from_dict(GGC,orient='index',columns=['GGC'])
    df_KSGC = pd.DataFrame.from_dict(KSGC,orient='index',columns=['KSGC'])
    # df_EFFG = pd.DataFrame.from_dict(EFFG,orient='index',columns=['EFFG'])


    # 合并所有DataFrame数据并写入文件
    df = pd.concat([df_digm,df_GMM,df_GGC,df_KSGC,df_DC, df_CC, df_ODC, df_KS], axis = 1)
    df.to_excel(xlsx,sheet_name = graph)
    
    
    
    # -----------------------------------------------------根据分数dict生成排名list------------------------------------------------
    score_list = [DiGM,GMM,GGC,KSGC,DC,  CC, ODC, KS]
    df_duration = pd.DataFrame(columns=['DiGM','GMM','GGC','KSGC','DC','CC','ODC','KS'])
    df_duration.loc[0] = [duration_DiGM, duration_GMM,duration_GGC,duration_KSGC,duration_DC, duration_CC,duration_ODC, duration_KS]
    print(df_duration)
    df_duration.to_excel(xlsx_time,sheet_name=graph)
    
    df_rank = pd.DataFrame()
    # 对字典进行排序并获取排序后的 keys ，即分数降序排列后的节点id，并以Dataframe形式写入.xlsx文件
    for i in range(len(score_list)):
        dict_sorted = dict(sorted(score_list[i].items(), key = lambda x:x[1], reverse = True))
        rank_list = dict_sorted.keys()
        df_item = pd.DataFrame(rank_list, columns=tf.var_name_to_str(score_list[i]))
        df_rank = pd.concat([df_rank, df_item], axis = 1)
    df_rank.to_excel(xlsx_rank, sheet_name=graph)
    
    
    
    
    
    

'''
Description: 主函数，用于调整模型结构、文件名、测试网络数量
Author: Junwen Yang
Date: 2022-06-26 23:08:21
LastEditTime: 2022-10-13 15:06:16
LastEditors: Junwen Yang
'''

def main():
    
    # -----------------------------------------------------调节模型所采用的指标----------------------------------------------------
    
    
    # -----------------------------------------------------文件读写前置处理--------------------------------------------------------
    # 储存节点分数的文件名
    
    file_name = 'DiGM-0223-score'
    # 储存节点排名的文件名
    rank_file_name = 'DiGM-0223-rank'
    time_file_name = 'DiGM-0223-time'
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
        'film_trust'
        # network_edgelist.s,
        # network_edgelist.m,
        # network_edgelist.bit,
        # network_edgelist.mo,
        # network_edgelist.twi,
        # network_edgelist.twir
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
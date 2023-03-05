import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
import datetime
from alive_progress import alive_bar

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


def rank_distri_func(score_list):
    score_list = sorted(score_list, reverse=True)
    rank_distri = []
    temp_rank = score_list[0]
    cnt = 1
    for i in range(len(score_list)-1):
        if score_list[i+1] == temp_rank:
            cnt += 1
        else:
            rank_distri.append(cnt)
            cnt = 1
            temp_rank = score_list[i+1]
    return rank_distri    


def ccdf_func(rank_list, node_num):
    num = len(rank_list)
    ccdf = [(node_num - sum(rank_list[0:i])) / node_num for i in range(1, num+1)]
    return ccdf


def read_excel_file(graph, filename,methods):
    result = pd.read_excel(f'./results/centrality/{filename}.xlsx', sheet_name=graph)
    # methods = ["DiGM", "GMM", "GGC", "KSGC", "DC", "CC", "ODC", "KS","LGC"] 
    centrality = [list(result[d]) for d in methods]
    return centrality

def get_rank_list(centrality, methods):
    return [rank_distri_func(centrality[i]) for i in range(len(methods))]

def get_ccdf_list(rank_list, node_num):
    ccdf_list = []
    length = 0
    for item in rank_list:
        res = ccdf_func(item, node_num)
        if len(res) > length:
            length = len(res)
        ccdf_list.append(res)
    return ccdf_list, length

def run_ccdf(graph,filename,methods):
    
    # 根据节点分数计算每个排名上有多少个节点
    
    centrality = read_excel_file(graph, filename, methods)

    # 设置之后数据合并以及画图的顺序和颜色
    color_list = ['lightcoral', 'darkkhaki', 'gold', 'mediumpurple', 'royalblue', 'rebeccapurple', 'black', 'red', 'darkorange', 'green', 'blue']

    # 将数据转化并合成到一个dataframe里
    df_score = pd.DataFrame(centrality).T
    df_score.columns = methods
    print(df_score)

    rank_list = get_rank_list(centrality, methods)

    # 根据节点分布数据计算CCDF数据
    node_num = len(df_score)
    ccdf_list, length = get_ccdf_list(rank_list, node_num)
    for i in range(len(ccdf_list)):
        while(len(ccdf_list[i]) < int(length*1.1)):
            ccdf_list[i].append(0)
    
    
    df_ccdf = pd.DataFrame(ccdf_list).T
    df_ccdf.columns = methods
    # df_ccdf.to_excel('./results/CCDF/'+'CCDF_'+date_string+'.xlsx')
    # print(df_ccdf)
    return df_ccdf

# graph = 'MesselShale_foodweb'
filepath = './results/CCDF/'
filename = 'all_centrality_score03-05_15-19'
now = datetime.datetime.now()
date_string = now.strftime('%m-%d_%H-%M')

methods = ["DiGM", "GMM", "GGC", "KSGC", "DC", "CC", "ODC", "KS","LGC"]

network_list = [
        network_edgelist.m,
        network_edgelist.mo,
        network_edgelist.bit,
        network_edgelist.wiki,
        network_edgelist.twir
        ]



df = pd.DataFrame()
df.to_excel(filepath+'CCDF_'+date_string+'.xlsx')
with alive_bar(len(network_list), title='CCDF Calculation...', bar='blocks') as bar:
    for graph in network_list:
        df = run_ccdf(graph, filename, methods)
        with pd.ExcelWriter(filepath+'CCDF_'+date_string+'.xlsx', mode='a', engine="openpyxl") as writer:
            df.to_excel(writer, sheet_name=graph)   
        bar()
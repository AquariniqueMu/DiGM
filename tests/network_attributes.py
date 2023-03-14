'''
Description: 
Author: Junwen Yang
Date: 2023-03-05 18:53:29
LastEditTime: 2023-03-05 19:00:26
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


import networkx as nx
import pandas as pd

networks = [network_edgelist.m,network_edgelist.mo,network_edgelist.bit,network_edgelist.wiki,network_edgelist.twir,network_edgelist.email]

df = pd.DataFrame()

for net in networks:
    # 构建有向网络
    G = nx.read_weighted_edgelist('./data/'+net+'.edgelist', create_using=nx.DiGraph)

    # 计算网络性质
    avg_degree = sum(dict(G.degree()).values()) / len(G)
    max_out_degree = max(dict(G.out_degree()).values())
    min_out_degree = min(dict(G.out_degree()).values())
    max_in_degree = max(dict(G.in_degree()).values())
    min_in_degree = min(dict(G.in_degree()).values())
    avg_clustering_coefficient = nx.average_clustering(G)
    # avg_shortest_path_length = nx.average_shortest_path_length(G)

    # 输出结果
    print("Average Degree: ", avg_degree)
    print("Maximum Out-Degree: ", max_out_degree)
    print("Minimum Out-Degree: ", min_out_degree)
    print("Maximum In-Degree: ", max_in_degree)
    print("Minimum In-Degree: ", min_in_degree)
    print("Average Clustering Coefficient: ", avg_clustering_coefficient)
    # print("Average Shortest Path Length: ", avg_shortest_path_length)
    
    df[net] = [avg_degree,max_out_degree,min_out_degree,max_in_degree,min_in_degree,avg_clustering_coefficient]
df.index = ['Average Degree','Maximum Out-Degree','Minimum Out-Degree','Maximum In-Degree','Minimum In-Degree','Average Clustering Coefficient']
print(df)
df.to_excel('network_attributes.xlsx')
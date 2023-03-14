'''
Description: 
Author: Junwen Yang
Date: 2023-03-05 18:28:20
LastEditTime: 2023-03-05 19:20:41
LastEditors: Junwen Yang
'''


def jaccard_similarity_coefficient(list1, list2):
    """
    计算节点u和节点v之间的Jaccard相似性系数

    :param G: 一个 NetworkX 图对象
    :param u: 节点 u
    :param v: 节点 v
    :return: Jaccard相似性系数
    """
    
    # 计算交集和并集的大小
    intersection_size = len(list1.intersection(list2))
    union_size = len(list1.union(list2))
    # 计算Jaccard相似性系数
    jaccard_coefficient = intersection_size / union_size
    return jaccard_coefficient

import pandas as pd


standard_rank = pd.read_excel('./results/SIR_standard//standard_series_03-05_14-55.xlsx')['rank']

networks = ['MesselShale_foodweb','bitcoinalpha','moreno_health']

df = pd.DataFrame(columns=['network','method','jaccard'])

for net in networks:
    centrality_rank = pd.read_excel('./results/centrality/all_centrality_rank03-05_15-19.xlsx',sheet_name=net)
    cen = centrality_rank[:int(len(standard_rank)*0.05)]
    stan = standard_rank[:len(cen)]
    for col in cen.drop(columns=['Unnamed: 0'],axis=1):
        print(net, col ,jaccard_similarity_coefficient(set(cen[col]), set(stan)))
        df = df.append({'network':net,'method':col,'jaccard':jaccard_similarity_coefficient(set(cen[col]), set(stan))},ignore_index=True)
print(df)
df.to_excel('./results/jaccord/jaccard_2.xlsx')
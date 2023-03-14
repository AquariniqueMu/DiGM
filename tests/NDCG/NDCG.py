'''
Description: 
Author: Junwen Yang
Date: 2023-03-05 15:26:13
LastEditTime: 2023-03-05 19:18:08
LastEditors: Junwen Yang
'''
import numpy as np

def ndcg_at_k(r, k):
    """计算NDCG@k"""
    r = np.asfarray(r)[:k]
    dcg = np.sum(r / np.log2(np.arange(2, r.size + 2)))
    idcg = np.sum(np.ones_like(r) / np.log2(np.arange(2, r.size + 2)))
    return dcg / idcg

def ndcg_at_ks(r, k_set):
    """计算一组k值下的NDCG"""
    dcgs = []
    for k in k_set:
        dcgs.append(ndcg_at_k(r, k))
    return dcgs

import pandas as pd


standard_rank = pd.read_excel('./results/SIR_standard//standard_series_03-05_14-55.xlsx')['rank']

networks = ['MesselShale_foodweb','bitcoinalpha','moreno_health']

df = pd.DataFrame(columns=['network','method','NDCG'])

for net in networks:
    centrality_rank = pd.read_excel('./results/centrality/all_centrality_rank03-05_15-19.xlsx',sheet_name=net)
    cen = centrality_rank[:int(len(standard_rank)*0.05)]
    stan = standard_rank[:len(cen)]
    for col in cen.drop(columns=['Unnamed: 0'],axis=1):
        print(net, col ,ndcg_at_ks(set(cen[col]), set(stan)))
        df = df.append({'network':net,'method':col,'jaccard':ndcg_at_ks(cen[col], stan)},ignore_index=True)
print(df)
df.to_excel('./results/NDCG/jaccard_1.xlsx')
'''
Description: 
Author: Junwen Yang
Date: 2023-03-05 15:26:13
LastEditTime: 2023-03-05 15:26:18
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
'''
Description: 一些gravity.py中可能用到的工具函数
Author: Junwen Yang
Date: 2022-09-06 20:50:41
LastEditTime: 2023-01-13 17:43:40
LastEditors: Junwen Yang
'''

import networkx as nx
import numpy as np 
import math
import pandas as pd
from scipy.io import loadmat
import inspect
import graph_create as gc
import scipy.sparse as sp

def AVERAGE_DISTANCE(G):
    """
    计算网络中的平均最短路径长度
    """
    TOTAL_PATH_LENGTH = list()
    for node in G.nodes():
        SHORTEST_DIST = nx.single_source_shortest_path_length(G, node)
        for value in SHORTEST_DIST.values():
            TOTAL_PATH_LENGTH.append(value)

    return sum(TOTAL_PATH_LENGTH) / len(TOTAL_PATH_LENGTH)




# --------------------------------------约束系数------------------------------
def mutual_weight(G, u, v):
    # weight1.keys=[u,v]
    # weight2.keys=[v,u]
    # 计算节点u到v和节点v到u的权重和，没有连边权重默认为0
    if v in G[u]:
        a_uv=G.get_edge_data(u,v).values()
        a_uv1=float([i for i in a_uv][0])
       # a_uv=float([i for i in G.get_edge_data(u,v).values()])   
       # weight1["[u,v]"]=a_uv
       # weight1.values=a_uv
    else:
        a_uv1=0
    if u in G[v]:
        a_vu=G.get_edge_data(v,u).values()
        a_vu1=float([i for i in a_vu][0])
      #  a_vu=float([i for i in G.get_edge_data(v,u).values()])   
       # weight2.values=a_vu
    else:
        a_vu1=0
    return a_uv1+a_vu1

def normalized_mutual_weight(G, u, v, norm=sum):
    """
    权重归一化, 节点u的某一邻居权重/节点u的所有的邻居节点权重和
    """
    scale = norm(mutual_weight(G, u, w) for w in set(nx.all_neighbors(G, u)))
    return 0 if scale == 0 else mutual_weight(G, u, v) / scale


def local_constraint(G, u, v):
    nmw = normalized_mutual_weight
    direct = nmw(G, u, v)
    indirect = sum(
        nmw(G, u, w) * nmw(G, w, v)
        for w in set(nx.all_neighbors(G, u))
        )
    return (direct + indirect) ** 2

def constraint(G, nodes=None):
    if nodes is None:
        nodes = G

    constraint = [np.exp(sum(
        local_constraint(G, v, n) for n in set(nx.all_neighbors(G, v))
    ))  if len(G[v]) != 0 else math.inf for v in nodes ]
    # print("cons: %d"%v)
    # np.save('./'+graph+'/'+graph+'-constraint.npy', constraint)
    return constraint
    
    
# --------------------------------------局部信息熵------------------------------
def run_single_node_entropy(A,node):
    sum_out_weight = sum(A[node,:])
    if sum_out_weight != 0:
        prob_out_weight = [a / sum_out_weight if a != 0 else 0 for a in A[node,:]]
        return np.exp(sum([-1 * a * np.log2(a) if a != 0 else 0 for a in prob_out_weight]))
    else:
        return np.exp(-1)

def run_all_nodes_entropy(G,A):
    entropy_all_nodes = [run_single_node_entropy(A, node) for node in G.nodes]
    return entropy_all_nodes
    


# --------------------------------------有效距离------------------------------
def efficient_dist_replace(A,weight_sum):
    a = [[math.inf if A[i][j] == 0  else 1-math.log(A[i][j]/weight_sum[i]) for j in range(len(A))]for i in range(len(A)) ]
    return a

def efficient_dist(A):
    weight_sum = list()
    for i in range(len(A)):
        weight_sum.append(sum(A[i,:]))
    print(weight_sum)
    dist_matrix = efficient_dist_replace(A, weight_sum)
    return dist_matrix


# ---------------------------------------寻找多阶邻居--------------------------
def neighbor_search_3_step(G, node, step):
    nodes = list(nx.nodes(G))
    neighbor_one_step = []
    
    
    for node in list(nx.neighbors(G, node)):  # find 1_th neighbors
        neighbor_one_step.append(node)

    if step == 1:
        return neighbor_one_step

    neighbor_two_step = []
    for one_step_node in neighbor_one_step:
        for two_step_node in list(nx.neighbors(G, one_step_node)):  # find 2_th neighbors
            neighbor_two_step.append(two_step_node)
    neighbor_two_step = list(set(neighbor_two_step) - set(neighbor_one_step))
    if node in neighbor_two_step:
        neighbor_two_step.remove(node)

    if step == 2:
        return neighbor_one_step, neighbor_two_step

    neighbor_three_step = []
    for two_step_node in neighbor_two_step:
        for three_step_node in nx.neighbors(G, two_step_node):
            neighbor_three_step.append(three_step_node)
    neighbor_three_step = list(set(neighbor_three_step) - set(neighbor_two_step) - set(neighbor_one_step))
    if node in neighbor_three_step:
        neighbor_three_step.remove(node)
    
    if step == 3:
        return neighbor_one_step, neighbor_two_step,neighbor_three_step


def neighbor_search(G, node, step):
    nodes = list(nx.nodes(G))
    all_neighbors = []
    
    neighbor_one_step = []
    for node in list(nx.neighbors(G, node)):  # find 1_th neighbors
        neighbor_one_step.append(node)
    all_neighbors.append(neighbor_one_step)
    
    if step == 1:
        return [neighbor_one_step]

    else:
        for loop_step in range(1,step):
            neighbor_loop_step = []
            for X_step_node in all_neighbors[loop_step - 1]:
                for next_step_node in list(nx.neighbors(G, X_step_node)):  # find 2_th neighbors
                    neighbor_loop_step.append(next_step_node)
            for i in range(loop_step):
                neighbor_loop_step = list(set(neighbor_loop_step) - set(all_neighbors[i]))
            if node in neighbor_loop_step:
                neighbor_loop_step.remove(node)
            all_neighbors.append(neighbor_loop_step)

        return all_neighbors

# ---------------------------------------从.mat文件读取网络--------------------------
# def create_from_mat_file(self, path):


# ---------------------------------------变量名转字符串--------------------------
def var_name_to_str(var):
    callers_loval_vars = inspect.currentframe().f_back.f_locals.items()
    return [var_name for var_name, var_val in callers_loval_vars if var_val is var]



# ---------------------------------------可达矩阵计算--------------------------
def reachable_matrix(G):
    """
    计算网络可达矩阵的方法:
        输入networkx定义的图, 通过 
        (A+I)^(K-1) != (A+I)^(K) = (A+I)^(K+1) = R
        的形式, 迭代得出图的可达矩阵. 表示每个节点最远可以达到的节点分布
    """
    IDT_MAT = sp.csr_matrix(np.identity(nx.number_of_nodes(G)))
    ADJ_MAT = nx.adjacency_matrix(G)
    ADJ_MAT[ADJ_MAT != 0] = 1
    SP_A = sp.csr_matrix(ADJ_MAT)
    LAST_REA_MAT = INIT_REA_MAT = SP_A + IDT_MAT
    # print(INIT_REA_MAT)
   
    while(1):
        RES_REA_MAT =LAST_REA_MAT @ INIT_REA_MAT
        RES_REA_MAT[RES_REA_MAT != 0] = 1
        NUM_ITEMS_DIFFER = (RES_REA_MAT != LAST_REA_MAT).nnz
        if NUM_ITEMS_DIFFER == 0:
            return RES_REA_MAT
        else:
            print(NUM_ITEMS_DIFFER)
            LAST_REA_MAT = RES_REA_MAT
            
            
    
    
    
    # print(A)


    
'''
Author: AquarniqueMu 237795826@qq.com
Date: 2022-07-12 09:31:23
LastEditors: Junwen Yang
LastEditTime: 2023-02-09 19:16:20
Description: 
'''
import numpy as np
import networkx as nx
import math
import pandas as pd
import os
from scipy.io import loadmat

class graph_create():
    
    def __init__(self, graph_name):
        self.graph = graph_name
        self.G = nx.DiGraph()
        self.create()
        
    def create(self):
        graph = self.graph
        path = "./"+graph
        if not os.path.exists(path):
            os.mkdir(path)

        G1= nx.read_weighted_edgelist(self.graph+".edgelist",create_using=nx.DiGraph)
        # if 0 not in G1.nodes():
        #     G1.add_node(0)
        G1.remove_edges_from(nx.selfloop_edges(G1))
        
        # 针对physicians
        for e in G1.edges():
            G1.add_edge(e[0],e[1],weight=1)
            # G[e[0]][e[1]]['weight'] = 1
        
        # print(G1.edges(data=True))
        
        A1 = np.array(nx.adjacency_matrix(G1).todense())
        edgelist = []
        for item in G1.edges.data():
            a = (int(float(item[0])), int(float(item[1])), float(item[2]['weight']))
            
            edgelist.append(a)
        #节点顺序
        node_list = [int(float(i)) for i in G1.nodes()]
        node_list.sort()
        #重建，其实G1和G的网络一致，只是G.node()展示的顺序从小到大，新邻接矩阵A1标号和G1.nodes()相同
        
        self.G.add_nodes_from(node_list)
        
        self.G.add_weighted_edges_from(edgelist)
        # self.A = np.array(nx.adj_matrix(self.G).todense())
        self.A = np.array(nx.adjacency_matrix(self.G).todense())
        a_=np.where(self.A>0,1,0)
        
    def create_from_scipy_matrix(self, path):
        mat = loadmat(path)
        data = mat['Problem']
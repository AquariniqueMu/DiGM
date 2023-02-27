'''
Description: 
Author: Junwen Yang
Date: 2022-07-12 09:39:17
LastEditTime: 2023-02-09 21:14:55
LastEditors: Junwen Yang
'''

import numpy as np
import networkx as nx
import math
import pandas as pd
import kshell as ks
# import localdim as ld
import tools_func as tf
import ismf
import klayer as kl
from alive_progress import alive_bar
class gravity_model():
    
    def __init__(self, A, G, graph, switch_mass,switch_co,switch_dist):
        self.A = A
        self.G = G
        # self.W = W
        self.graph = graph
        self.size = len(A)
        # self.mass = dict()
        self.centrality = dict()
        self.run(switch_mass,switch_co,switch_dist)


    def gravity_formula(mass_sub, mass_obj, dist):
        return (mass_sub * mass_obj) / dist**2
    
    def normalized(dict):
        max_value = max(dict.values())
        min_value = min(dict.values())
        for key in dict.keys():
            dict[key] = (dict[key] - min_value) / (max_value - min_value)
        return dict
    
    def mass(self,switch):
        # k壳作质量
        if switch == 'kshell':
            self.mass_source = ks.kshell(self.G)
            self.mass_target = ks.kshell(self.G)
            
        elif switch == 'cluster_kshell':
            self.mass_source =  1   
            
        elif switch == 'reachable':
            REA_MAT = tf.reachable_matrix(self.G)
            REA_MAT = np.array(REA_MAT.todense()) 
            clu = nx.clustering(self.G)
            self.mass_source = dict()
            self.mass_target = dict()
            # cons = nx.constraint(self.G)
            for node in self.G.nodes():
                self.mass_source[node] = sum(REA_MAT[node,:]) 
                self.mass_target[node] = sum(REA_MAT[:,node])* math.exp(-clu[node]) 
            # print(self.mass_source)
            # self.mass_target = self.mass_source
            
    
        
        elif switch == 'degree':
            self.mass_source = [a[1] for a in self.G.out_degree()]
            # self.mass_target = [a[1] for a in self.G.in_degree()]
            self.mass_target = self.mass_source
            
        elif switch == 'inf_entropy':
            out_entropy = tf.run_all_nodes_entropy(self.G, self.A) 
            out_degree = [a[1] for a in self.G.out_degree()]
            self.mass_source = np.multiply(out_entropy,out_degree)

            A_trans = np.transpose(self.A)
            in_entropy = tf.run_all_nodes_entropy(self.G, A_trans)
            in_degree = [a[1] for a in self.G.in_degree()]
            self.mass_target = np.multiply(in_entropy,in_degree)
            
            
        elif switch == 'klayer':
            self.mass_source = kl.k_layer(self.G)
            G_copy = self.G.copy()
            self.mass_target = kl.k_layer(G_copy.reverse())

        elif switch == 'reatimesdegree':
            
            out = [a[1] for a in self.G.out_degree()]
            in_degree = [a[1] for a in self.G.in_degree()]
            # clu = nx.clustering(self.G)
            self.mass_source = dict()
            self.mass_target = dict()
            
            # REA_MAT = tf.reachable_matrix(self.G)
            # REA_MAT = np.array(REA_MAT.todense()) 
            # REA_col = dict()
            # REA_row = dict()
            # # cons = nx.constraint(self.G)
            # for node in self.G.nodes():
            #     REA_row[node] = sum(REA_MAT[node,:])
            #     REA_col[node] = sum(REA_MAT[:,node])
            
            # REA_col = gravity_model.normalized(REA_col)
            # REA_row = gravity_model.normalized(REA_row)
            if_in_degree_exist = [0 if i == 0 else 1 for i in in_degree]
            
            cc = nx.closeness_centrality(self.G.reverse())
            
            for node in self.G.nodes():
                self.mass_source[node] = cc[node] * out[node] * if_in_degree_exist[node]
                self.mass_target[node] = cc[node] * out[node]
                
        elif switch == 'cc':
            
            out = [a[1] for a in self.G.out_degree()]
            in_degree = [a[1] for a in self.G.in_degree()]
            # clu = nx.clustering(self.G)
            self.mass_source = dict()
            self.mass_target = dict()
            
            # REA_MAT = tf.reachable_matrix(self.G)
            # REA_MAT = np.array(REA_MAT.todense()) 
            # REA_col = dict()
            # REA_row = dict()
            # # cons = nx.constraint(self.G)
            # for node in self.G.nodes():
            #     REA_row[node] = sum(REA_MAT[node,:])
            #     REA_col[node] = sum(REA_MAT[:,node])
            
            # REA_col = gravity_model.normalized(REA_col)
            # REA_row = gravity_model.normalized(REA_row)
            if_in_degree_exist = [0 if i == 0 else 1 for i in in_degree]
            
            cc = nx.closeness_centrality(self.G.reverse())
            
            for node in self.G.nodes():
                self.mass_source[node] = cc[node] * out[node] * if_in_degree_exist[node]
                self.mass_target[node] = cc[node] * out[node]
        # np.save('./'+self.graph+'/'+self.graph+'-mass.npy', self.mass) # 注意带上后缀名
        # self.mass = np.load('./'+self.graph+'/'+self.graph+'-mass.npy').item()
    
        elif switch == 'density':
            self.mass_source = dict.fromkeys(self.G.nodes(), 0)
            self.mass_target = dict.fromkeys(self.G.nodes(), 0)
            # out = [a[1] for a in self.G.out_degree()]
            AVER_DIST = tf.AVERAGE_DISTANCE(self.G)
            INT_AVER_DIST = int(AVER_DIST / 2 + 0.5)
            # INT_AVER_DIST = 2
            DICT_NEIGHBOR = dict()
            for node in self.G.nodes():
                DICT_NEIGHBOR[node] = tf.neighbor_search(self.G, node, INT_AVER_DIST)
            print('Mass Calculation start...')
            with alive_bar(len(self.G.nodes())) as bar:
                for node in self.G.nodes():
                    for i in range(INT_AVER_DIST):
                        self.mass_source[node] += sum([self.G.out_degree(target)/(i+1) for target in DICT_NEIGHBOR[node][i]])
                    self.mass_source[node] *= self.G.out_degree(node)
                    bar()
            # self.mass_source = [a/sum(self.mass_source.values()) for a in self.mass_source.values()]
            # self.mass_source = [math.exp(a) for a in self.mass_source]
            # for index,value in self.mass_source.items():
            #     self.mass_source[index] = math.exp(value/sum(self.mass_source.values()))
            self.mass_target = self.mass_source
    
       
    def distance(self,switch_dist):
        '''
        input: 邻接矩阵
        return: 最短距离矩阵
        '''
        # self.size = len(A)
        
        
        
        
        if switch_dist == 'calc':
        
            # self.dist = [[math.inf if self.A[i][j] == 0  else 1 for j in range(self.size)]for i in range(self.size) ]
            
            self.dist = tf.efficient_dist(self.A)
            # print(self.dist)
            for k in range(self.size):
                for i in range(self.size):
                    for j in range(self.size):
                        if self.dist[i][j] > self.dist[i][k] + self.dist[k][j]:
                            self.dist[i][j] = self.dist[i][k] + self.dist[k][j]
                            # paths[i][j] = paths[i][k]
                    # np.savetxt('out最短距离矩阵第'+str(i)+'行.txt', a, fmt='%f',delimiter='\t')
                if(k % 100 == 0):
                    print("Floyd process: %d"%k)
            print(self.dist)
            np.savetxt('./'+self.graph+'/'+self.graph+'最短距离矩阵.txt', self.dist, fmt='%f',delimiter='\t')
            
        elif switch_dist == 'txt':
            self.dist = np.loadtxt('./'+self.graph+'/'+self.graph+'最短距离矩阵.txt',dtype=float,delimiter='\t')
        
    def coefficient_func(self,switch_co):
        if switch_co == 'local_dim':
            1
            # self.coefficient = [a+1 for a in ld.run_local_dim(self.G,self.L)]
            # self.coefficient = 1
        elif switch_co == 'ism':
            ism_dict = ismf.ism_res(self.G, self.A, len(self.A))
            self.coefficient = [ism_dict['%d'%(node+1)] for node in self.G.nodes()]
            co_max = max(self.coefficient)
            self.coefficient = [1+a/co_max for a in self.coefficient]
            # print(ism_list)
            
        elif switch_co == 'kshell':
            self.coefficient = dict()
            kshell_list = ks.kshell(self.G)
            differ = max(kshell_list) - min(kshell_list)
            MIN = min(list(kshell_list.values()))
            for node in self.G.nodes():
                self.coefficient[node] = 1 + ( kshell_list[node] - MIN ) / differ
            
        elif switch_co == 'no_other':
            self.coefficient = [1]*len(self.G.nodes())         


        elif switch_co == 'reachable':
            REA_MAT = tf.reachable_matrix(self.G)
            REA_MAT = np.array(REA_MAT.todense()) 
            self.coefficient = dict()

            for node in self.G.nodes():
                self.coefficient[node] = sum(REA_MAT[node,:])
            
            NORM_BASE = sum(self.coefficient.values())
            for node in self.G.nodes():
                self.coefficient[node] =  1 + (self.coefficient[node] / NORM_BASE)
                
        elif switch_co == 'klayer':
            self.coefficient = dict()
            klayer_list = kl.k_layer(self.G)
            MAX = max(list(klayer_list.values()))
            for node in self.G:
                self.coefficient[node] = 1 + (klayer_list[node] / MAX)
                
        elif switch_co == 'rea':
            REA_MAT = tf.reachable_matrix(self.G)
            REA_MAT = np.array(REA_MAT.todense()) 
            REA_col = dict()
            REA_row = dict()
            REA_NUMERIC = dict()
            # cons = nx.constraint(self.G)
            for node in self.G.nodes():
                # REA_row[node] = sum(REA_MAT[node,:])
                # REA_col[node] = sum(REA_MAT[:,node])
                REA_NUMERIC[node] = sum(REA_MAT[node,:]) * sum(REA_MAT[:,node])
                
            
        elif switch_co == 'cc':
            # self.coefficient = dict()
            cc = nx.closeness_centrality(self.G.reverse())
            # for node in self.G.nodes():
            #     self.coefficient[node] = cc[node]
            
            
            # REA_col = gravity_model.normalized(REA_col)
            # REA_row = gravity_model.normalized(REA_row)
            
            self.coefficient = dict()
            self.coefficient = gravity_model.normalized(cc)
            
            
        elif switch_co == 'cc cons':
            cc = nx.closeness_centrality(self.G.reverse())
            cons = nx.clustering(self.G)
            
            self.coefficient = dict()
            for node in self.G.nodes():
                self.coefficient[node] = cc[node] * cons[node]
            
            self.coefficient = gravity_model.normalized(self.coefficient)
            
            
            
    
    def cut_off_radius(self):
        self.cutoff_radius = 1

    
    
    # b = gravity_formula(1,1,2)
    
    
    
    def centrality_calc(self):
        
        self.centrality = dict.fromkeys(self.G.nodes(), 0)
        AVER_DIST = tf.AVERAGE_DISTANCE(self.G)
        # print(AVER_DIST)
        
        # 计算网络的平均路径长度, 取一半并四舍五入, 为截断半径
        AVER_DIST = tf.AVERAGE_DISTANCE(self.G)
        INT_AVER_DIST = int(AVER_DIST / 2 + 0.5)
        AVER_DIST = int(AVER_DIST + 0.5)
        
        
        # INT_AVER_DIST = 2
        if AVER_DIST <= 6:
            AVER_DIST = 6
        DICT_NEIGHBOR = dict()
        for node in self.G.nodes():
            DICT_NEIGHBOR[node] = tf.neighbor_search(self.G, node, AVER_DIST)
        # print('Neighbor search finished...')
        # print(DICT_NEIGHBOR[65])
        print('Score Calculation start...')
        with alive_bar(len(self.G.nodes())) as bar:
            for node in self.G.nodes():
                for i in range(INT_AVER_DIST,AVER_DIST,1):
                # for i in range(AVER_DIST):
                    self.centrality[node] += sum([gravity_model.gravity_formula(self.mass_source[node], self.mass_target[target], i+1) for target in DICT_NEIGHBOR[node][i]])
                    # if node == 65:
                    #     print(self.mass_source[node])
                # print(self.coefficient[node])
                self.centrality[node] *= self.coefficient[node]
                self.centrality[node] += self.G.out_degree(node) * self.coefficient[node]
                bar()
            
    def run(self,switch_mass,switch_co,switch_dist):
        # print("\n---------正在计算节点质量---------\n")
        self.mass(switch_mass)
        # print("\n---------正在计算节点距离---------\n")
        # self.distance(switch_dist)
        # print("\n---------正在计算节点系数---------\n")
        self.coefficient_func(switch_co)
        # print("\n---------正在计算节点分数---------\n")
        self.centrality_calc()
        
        
# import time
# import graph_create as gc

# graph = 'stormofswords'
# graph_class = gc.graph_create(graph)
# G = graph_class.G
# # ksh = ks.kshell(G)
# # print(min(list(ksh.values())))
# A = graph_class.A
# start = time.perf_counter()
# switch_mass = 'reachable'
# switch_co = 'klayer'
# switch_dist = 'calc'
# DiGM = gravity_model(A, G, graph,switch_mass,switch_co,switch_dist).centrality
# end = time.perf_counter()
# duration_DiGM = end - start
# print('-----------------------------')
# print(DiGM)
# print(duration_DiGM)
# print('-----------------------------')
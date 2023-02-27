
import numpy as np
import networkx as nx
import math
import pandas as pd
import kshell as ks
import localdim as ld
import tools_func as tf
import ismf


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
    
    
    def mass(self,switch):
        # k壳作质量
        if switch == 'kshell':
            self.mass_source = ks.kshell(self.G)
            self.mass_target = ks.kshell(self.G)
            
        elif switch == 'cluster_kshell':
            self.mass_source =  1   
            
        
            
            
        
        elif switch == 'degree':
            self.mass_source = [a[1] for a in self.G.out_degree()]
            self.mass_target = [a[1] for a in self.G.in_degree()]
            
        elif switch == 'inf_entropy':
            out_entropy = tf.run_all_nodes_entropy(self.G, self.A) 
            out_degree = [a[1] for a in self.G.out_degree()]
            constraint = tf.constraint(self.G)
            
            self.mass_source = np.multiply(out_entropy,out_degree)
            self.mass_source = np.multiply(self.mass_source, constraint)
            
            A_trans = np.transpose(self.A)
            in_entropy = tf.run_all_nodes_entropy(self.G, A_trans)
            in_degree = [a[1] for a in self.G.in_degree()]
            self.mass_target = np.multiply(in_entropy,in_degree)
            self.mass_target = np.multiply(self.mass_target, constraint)
            
            
            
            
        
        
        
        np.save('./'+self.graph+'/'+self.graph+'-mass.npy', self.mass) # 注意带上后缀名
        # self.mass = np.load('./'+self.graph+'/'+self.graph+'-mass.npy').item()
        
    def distance(self,switch_dist):
        '''
        input: 邻接矩阵
        return: 最短距离矩阵
        '''
        # self.size = len(A)
        
        if switch_dist == 'calc':
        
            self.dist = [[math.inf if self.A[i][j] == 0  else 1 for j in range(self.size)]for i in range(self.size) ]
            
            # self.dist = tf.efficient_dist(self.A)

            for k in range(self.size):
                for i in range(self.size):
                    for j in range(self.size):
                        if self.dist[i][j] > self.dist[i][k] + self.dist[k][j]:
                            self.dist[i][j] = self.dist[i][k] + self.dist[k][j]
                            # paths[i][j] = paths[i][k]
                    # np.savetxt('out最短距离矩阵第'+str(i)+'行.txt', a, fmt='%f',delimiter='\t')
                if(k % 100 == 0):
                    print("Floyd process: %d"%k)
            np.savetxt('./'+self.graph+'/'+self.graph+'最短距离矩阵.txt', self.dist, fmt='%f',delimiter='\t')
            
        elif switch_dist == 'txt':
            self.dist = np.loadtxt('./'+self.graph+'/'+self.graph+'最短距离矩阵.txt',dtype=float,delimiter='\t')
        
    def coefficient_func(self,switch_co):
        if switch_co == 'local_dim':
            self.coefficient = [a+1 for a in ld.run_local_dim(self.G,self.L)]
            # self.coefficient = 1
        elif switch_co == 'ism':
            ism_dict = ismf.ism_res(self.G, self.A, len(self.A))
            self.coefficient = [ism_dict['%d'%(node+1)] for node in self.G.nodes()]
            co_max = max(self.coefficient)
            self.coefficient = [1+a/co_max for a in self.coefficient]
            # print(ism_list)
            
        elif switch_co == 'kshell':
            kshell_list = ks.kshell(self.G)
            differ = max(kshell_list) - min(kshell_list)
            self.coefficient = [1 + ( a - min(kshell_list) ) * differ for a in kshell_list]
            
            
            
    
    def cut_off_radius(self):
        self.cutoff_radius = 1
    
    def centrality_calc(self):
        
        for item in self.G.nodes():
            sum = 0
            for i in range(self.size):
                if( self.A[item][i] != math.inf ):
                    sum += self.coefficient[item] * gravity_model.gravity_formula(self.mass_source[item], self.mass_target[i], self.dist[item][i])
            self.centrality[item] = sum
            
    def run(self,switch_mass,switch_co,switch_dist):
        print("\n---------正在计算节点质量---------\n")
        self.mass(switch_mass)
        print("\n---------正在计算节点距离---------\n")
        self.distance(switch_dist)
        print("\n---------正在计算节点系数---------\n")
        self.coefficient_func(switch_co)
        print("\n---------正在计算节点分数---------\n")
        self.centrality_calc()
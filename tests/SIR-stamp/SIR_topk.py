'''
Description: 
Author: Junwen Yang
Date: 2023-03-04 20:39:27
LastEditTime: 2023-03-14 15:11:04
LastEditors: Junwen Yang
'''
import networkx as nx
import random
from alive_progress import alive_bar
import numpy as np
import pandas as pd
import networkx as nx
np.warnings.filterwarnings('ignore', category=np.VisibleDeprecationWarning)

def SIR_RUN(G, infected_nodes_source, beta, gamma, max_time):
    """
    SIR model simulation with given networkx graph, initial infected nodes, 
    infection rate (beta), recovery rate (gamma), and simulation time (max_time).
    """
    infected_nodes = infected_nodes_source.copy()
    susceptible_nodes = list(set(G.nodes()) - set(infected_nodes))
    S = len(susceptible_nodes)
    I = len(infected_nodes)
    R = 0
    time = 0
    state = {node: 'S' for node in susceptible_nodes}
    state.update({node: 'I' for node in infected_nodes})
    states = {'S': S, 'I': I, 'R': R}
    result = [states]
    
    while time < max_time and I > 0:
        new_infected_nodes = []
        new_recovered_nodes = []
        
        for infected_node in infected_nodes:
            neighbors = list(G.successors(infected_node))
            for neighbor in neighbors:
                if state[neighbor] == 'S' and random.uniform(0, 1) < beta:
                    state[neighbor] = 'I'
                    new_infected_nodes.append(neighbor)
        
            if random.uniform(0, 1) < gamma:
                state[infected_node] = 'R'
                new_recovered_nodes.append(infected_node)
        
        for node in new_infected_nodes:
            infected_nodes.append(node)
            susceptible_nodes.remove(node)
        for node in new_recovered_nodes:
            infected_nodes.remove(node)
            R += 1
        
        S = len(susceptible_nodes)
        I = len(infected_nodes)
        # print(states)
        states = {'S': S, 'I': I, 'R': R}
        
        # states = [S, I, R]
        result.append(states)
        # print(infected_nodes)
        time += 1
    
    return result




def SIR_average(G, infected_nodes, beta, gamma, max_time, num_simulations):
    """
    Run SIR simulation for num_simulations times and return the average
    of the last 50 simulation results.
    """
    results = []
    with alive_bar(num_simulations,bar='blocks',title='SIR Simulation ---> ') as bar:
        for i in range(num_simulations):
            result = SIR_RUN(G, infected_nodes, beta, gamma, max_time)
            # print(result)
            avg_result = {k: np.mean([d[k] for d in result]) for k in result[0]}
            results.append(avg_result)
            bar()

    avg_results = {k: np.mean([d[k] for d in results]) for k in results[0]}
    return avg_results




# 定义一个字典，存储各种算法和对应的节点列表
def SIR_TOPK(G, beta, gamma, max_time,rank_dict,loop_num):
    

    # 定义一个空DataFrame，用于存储结果
    results_df = pd.DataFrame()

    # 遍历rank_dict中的每个算法及其对应的节点列表
    # with alive_bar(len(rank_dict),bar='blocks',title='SIR Simulation...') as bar:  
    for algorithm, rank_nodes in rank_dict.items():
        # 定义一个空列表，用于存储结果
        result_list = []
        # 遍历节点列表
        
        # 在网络中设置该节点为感染节点
        infected_nodes = rank_nodes
        
        
        # 运行SIR模拟，并获取结果
        avg_lists = []
        with alive_bar(loop_num,bar='blocks',title='SIR Simulation / '+algorithm+' ---> ') as bar:
            for i in range(loop_num):
                result = SIR_RUN(G, infected_nodes, beta, gamma, max_time)
                # 将结果中I列和R列的值相加，组成一个列表
                sum_IR = [d['I'] + d['R'] for d in result]
                avg_lists.append(sum_IR)
                bar()
        # 求avg_lists中每个列表对应位置的平均值
        
        max_length = max([len(i) for i in avg_lists])
        for avg_index in range(len(avg_lists)):
            avg_lists[avg_index].extend([avg_lists[avg_index][-1]] * (max_length - len(avg_lists[avg_index])))
            
        all_data_matrix = np.array(avg_lists)
        avg_vec = np.mean(all_data_matrix, axis=0)
        # print(all_data_matrix)
        # avg_lists = np.array(avg_lists)
        # avg_vec = np.mean(avg_lists, axis=0)
        
        
        # print(sum_IR)
        # 将算法名称和该节点的结果添加到result_list中
        # result_list.append({'Algorithm': algorithm, 'Node': rank_nodes, 'IR_sum': avg_vec})
        # print(result_list)
        results_df[algorithm] = pd.DataFrame(avg_vec)
            # bar()
    return results_df

directed_network_list = [
    'MesselShale_foodweb',
    'email-Eu-core',
    'bitcoinalpha',
    'moreno_health',
    'Wiki-Vote',
    'twitterreferendum'
    ]
# DC_rank = CC_rank = BC_rank = [1,2,3,4,5,6,7,8,9,10]


def split_dataframe_to_dict(df):
    dict_data = {}
    for column in df.columns:
        dict_data[column] = df[column].tolist()
    return dict_data

for top_percent in [0.02,0.05,0.1]:
    for beta_ in [0.1,0.15,0.2,0.25,0.3]:
        # beta_ = 0.2
        gamma_ =  0.2
        max_time_ = 20
        loop_num_ = 100

        top_percent = 0.05
        path = './results/SIR_step/'
        filename = path + 'SIR_step_03-12-'+str(beta_)+'-'+str(gamma_)+'-20s.xlsx'
        empty_df = pd.DataFrame()
        empty_df.to_excel(filename)



        for network in directed_network_list:
            
            # 读取各种算法的节点排名列表
            results = pd.read_excel('./results/centrality/all_centrality_rank03-05_15-19.xlsx', sheet_name=network).drop(['Unnamed: 0'], axis=1)
            # 将DataFrame按列转换为字典，key为算法名称，value为节点列表
            rank_dict = split_dataframe_to_dict(results)
            # print(rank_dict.keys())
            
            # 仅保留前top_percent的节点
            for key in rank_dict:
                rank_dict[key] = rank_dict[key][:int(len(rank_dict[key]) * top_percent)]
                
            # 读取网络
            G = nx.read_weighted_edgelist('./data/' + network + '.edgelist', nodetype=int, create_using=nx.DiGraph())
            
            # 运行SIR模拟
            print("\n Running SIR simulation on network: ", network, "... \n")
            res = SIR_TOPK(G, beta=beta_, gamma=gamma_, max_time=max_time_, rank_dict=rank_dict,loop_num=loop_num_)
            
            # 将结果写入Excel
            with pd.ExcelWriter(filename, mode='a', engine="openpyxl") as writer:
                res.to_excel(writer, sheet_name=network)




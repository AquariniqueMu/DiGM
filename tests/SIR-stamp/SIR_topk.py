'''
Description: 
Author: Junwen Yang
Date: 2023-03-04 20:39:27
LastEditTime: 2023-03-05 10:42:55
LastEditors: Junwen Yang
'''
import networkx as nx
import random
from alive_progress import alive_bar

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
            neighbors = list(G.neighbors(infected_node))
            for neighbor in neighbors:
                if state[neighbor] == 'S' and random.random() < beta:
                    state[neighbor] = 'I'
                    new_infected_nodes.append(neighbor)
        
            if random.random() < gamma:
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


import numpy as np

def SIR_average(G, infected_nodes, beta, gamma, max_time, num_simulations):
    """
    Run SIR simulation for num_simulations times and return the average
    of the last 50 simulation results.
    """
    results = []
    with alive_bar(num_simulations) as bar:
        for i in range(num_simulations):
            result = SIR_RUN(G, infected_nodes, beta, gamma, max_time)
            # print(result)
            avg_result = {k: np.mean([d[k] for d in result]) for k in result[0]}
            results.append(avg_result)
            bar()
    # print(results[0][0])
    # print(results)
    # avg_result = np.mean(results, axis=0)
    # avg_result = np.mean(results, axis=0)
    avg_results = {k: np.mean([d[k] for d in results]) for k in results[0]}
    return avg_results


import pandas as pd
import networkx as nx


# 定义一个字典，存储各种算法和对应的节点列表
def SIR_TOPK(G, beta, gamma, max_time,rank_dict):
    

    # 定义一个空DataFrame，用于存储结果
    results_df = pd.DataFrame()

    # 遍历rank_dict中的每个算法及其对应的节点列表
    for algorithm, rank_nodes in rank_dict.items():
        # 定义一个空列表，用于存储结果
        result_list = []
        # 遍历节点列表
        
        # 在网络中设置该节点为感染节点
        infected_nodes = rank_nodes
        # 运行SIR模拟，并获取结果
        result = SIR_RUN(G, infected_nodes, beta, gamma, max_time)
        # 将结果中I列和R列的值相加，组成一个列表
        sum_IR = [d['I'] + d['R'] for d in result]
        # print(sum_IR)
        # 将算法名称和该节点的结果添加到result_list中
        result_list.append({'Algorithm': algorithm, 'Node': rank_nodes, 'IR_sum': sum_IR})
        # print(result_list)
        results_df[algorithm] = pd.DataFrame(result_list[0]['IR_sum'])
    return results_df

DC_rank = CC_rank = BC_rank = [1,2,3,4,5,6,7,8,9,10]

# # 将各种算法的rank节点转化为list类型，例如DC_top5, CC_top5等
# DC_top5 = list(DC_rank[:int(len(DC_rank)*0.5)])
# CC_top5 = list(CC_rank[:int(len(CC_rank)*0.5)])
# BC_top5 = list(BC_rank[:int(len(BC_rank)*0.5)])
# rank_dict = {'DC': DC_top5, 'CC': CC_top5, 'BC': BC_top5}

# 将各种算法的rank节点转化为list类型
rank_dict = {
    'DC': DC_rank, 
    'CC': CC_rank, 
    'BC': BC_rank
    }
top_percent = 0.05
for key in rank_dict:
    rank_dict[key] = rank_dict[key][:int(len(rank_dict[key]) * top_percent)]




G = nx.read_weighted_edgelist('./data/stormofswords.edgelist', nodetype=int)
res = SIR_TOPK(G, 0.1, 0.1, 100, rank_dict)

# 输出结果
print(res)



'''
Description: 用于生成SIR模型的标准中心性序列
Author: Junwen Yang
Date: 2023-03-04 20:39:27
LastEditTime: 2023-03-05 13:05:20
LastEditors: Junwen Yang
'''
import networkx as nx
import random
from alive_progress import alive_bar
import datetime
import numpy as np
import pandas as pd

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



def SIR_average(G, infected_nodes, beta, gamma, max_time, num_simulations):
    """
    Run SIR simulation for num_simulations times and return the average
    of the last 50 simulation results.
    """
    results = []
    # with alive_bar(num_simulations) as bar:
    for i in range(num_simulations):
        result = SIR_RUN(G, infected_nodes, beta, gamma, max_time)
        # print(result)
        avg_result = {k: np.mean([d[k] for d in result]) for k in result[0]}
        results.append(avg_result)
            # bar()
    # print(results[0][0])
    # print(results)
    # avg_result = np.mean(results, axis=0)
    # avg_result = np.mean(results, axis=0)
    avg_results = {k: np.mean([d[k] for d in results]) for k in results[0]}
    return avg_results


undirected_network_list = [
    # 'MesselShale_foodweb',
    # 'bitcoinalpha',
    # 'moreno_health',
    # 'Wiki-Vote',
    'twitterreferendum'
    ]


beta_ = 0.2
gamma_ = 0.2
max_time_ = 400
num_simulations_ = 20

now = datetime.datetime.now()
date_string = now.strftime('%m-%d_%H-%M')
filepath = './results/SIR_standard/'
filename = 'standard_series_'+date_string+'.xlsx'
empty_df = pd.DataFrame()
empty_df.to_excel(filepath+filename)



# with alive_bar(len(undirected_network_list), title="Outer Loop") as outer_bar:
for net in undirected_network_list:
    
    print("==========================Processing network: ", net+"==========================")
    
    G = nx.read_weighted_edgelist('./data/'+net+'.edgelist', nodetype=int)

    res = dict()
    with alive_bar(G.number_of_nodes(), title="Current Network Simulation",bar='blocks') as inner_bar:
        for node in G.nodes():
            res_dict = SIR_average(G, infected_nodes=[node], beta = beta_, gamma = gamma_, max_time = max_time_, num_simulations = num_simulations_)
            res[node] = (res_dict['I'] + res_dict['R']) / G.number_of_nodes()
            inner_bar()  
    # Convert res dictionary to dataframe
    df_res = pd.DataFrame.from_dict(res, orient='index', columns=['Infection Ratio'])

    # Save dataframe to Excel file
    with pd.ExcelWriter(filepath+filename, mode='a', engine="openpyxl") as writer:
        df_res.to_excel(writer, sheet_name=net)

        


        


'''
Description: 
Author: Junwen Yang
Date: 2023-02-13 11:09:48
LastEditTime: 2023-02-21 21:06:07
LastEditors: Junwen Yang
'''
import networkx as nx
import matplotlib.pyplot as plt

# 初始化网络
G = nx.DiGraph()

# 添加18个节点
for i in range(1,18,1):
    G.add_node(i)

# 添加节点之间的有向边
# for i in range(17):
#     for j in range(i + 1, 18):
#         G.add_edge(i, j)

# G.add_edge(1,2)
# G.add_edge(1,3)
# G.add_edge(1,4)
# G.add_edge(1,5)
# G.add_edge(1,6)

# TODO:其他方法的识别结果，特别是ODC 
# TODO：1到3节点的连边反向
G.add_edges_from([(1,2),(1,3),(1,4),(1,5)])
G.add_edges_from([(2,6),(2,7),(2,8)])
G.add_edges_from([(3,13)])
G.add_edges_from([(4,10),(4,11),(4,12)])
G.add_edges_from([(5,9)])
G.add_edges_from([(7,14),(7,15)])
G.add_edges_from([(9,16)])
G.add_edges_from([(11,17)])
G.add_edges_from([(12,18)])
G.add_edges_from([(14,13),(8,9),(16,4),(13,4)])
# 画图
plt.figure(figsize=(48,24))

nx.draw(G, with_labels=True, node_size=1000, node_color='r', font_size=10, font_color='b', font_weight='bold', alpha=0.5, linewidths=10, width=3, edge_color='b', style='dashed',pos=nx.shell_layout(G))

# print(nx.average_shortest_path_length(G))
import tools_func as tf
# print(tf.AVERAGE_DISTANCE(G))
AVER_DIST = tf.AVERAGE_DISTANCE(G)
INT_AVER_DIST = int(AVER_DIST / 2 + 0.5)
# AVER_DIST = int(AVER_DIST + 0.5)
print('\n')
print(AVER_DIST)
print(INT_AVER_DIST)
print('\n')

import gravity as grv
import numpy as np
A = np.array(nx.adjacency_matrix(G).todense())
switch_mass = 'density'
switch_co = 'cc'
switch_dist = 'calc'
DiGM = grv.gravity_model(A, G, 'example_digm',switch_mass,switch_co,switch_dist).centrality
print(DiGM)
# TODO：计算中心性

# 打印网络
# nx.draw_networkx(G)
# plt.show()
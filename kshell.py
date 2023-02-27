'''
Author: AquarniqueMu 237795826@qq.com
Date: 2022-07-12 09:49:18
LastEditors: AquarniqueMu 237795826@qq.com
LastEditTime: 2022-07-12 10:11:22
FilePath: \contrac-gravity\kshell.py
Description: 这是默认设置,请设置`customMade`, 打开koroFileHeader查看配置 进行设置: https://github.com/OBKoro1/koro1FileHeader/wiki/%E9%85%8D%E7%BD%AE
'''



def kshell(G):
    """
    kshell(G)计算k-shell值
    """
    graph = G.copy()
    importance_dict = {}
    ks = 1
    while graph.nodes():
        temp = []
        node_degrees_dict = gDegree(graph)
        kks = min(node_degrees_dict.values())
        while True:
            for k, v in node_degrees_dict.items(): 
                if v == kks:
                    # temp.append(k)
                    importance_dict[k] = ks
                    graph.remove_node(k)
                    node_degrees_dict = gDegree(graph)
            if kks not in node_degrees_dict.values():
                break
        # importance_dict[ks] = temp
        ks += 1
    return importance_dict

def gDegree(G):
    """
    将G.degree()的返回值变为字典
    """
    node_degrees_dict = {}
    for i in G.degree():
        node_degrees_dict[i[0]]=i[1]
    return node_degrees_dict.copy()
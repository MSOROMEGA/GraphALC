import sys
sys.path.append('core')
import pandas as pd
import networkx as nx
import matplotlib.pyplot as plt


def result_display(node_list):
    # OPTIMAL VALUE DISPLAY
    flow_list = []
    for node in node_list:
        flow_list += node.optxv
    product_flow = pd.DataFrame(
        [{"From": arc[0], "To": arc[1], "Product":arc[2], "Flow": int(flow[arc])} for flow in flow_list for arc in flow.keys() if flow[arc] > 1e-3]
    )
    product_flow.index=[''] * len(product_flow)
    product_flow
    product_flow1 = product_flow.groupby(['From','To']).apply(lambda x: list({p:f for p,f in zip(x[('Product')],x[('Flow')])}.values())).reset_index()
    product_flow2 = product_flow.groupby(['From','To']).apply(lambda x: list({p:f for p,f in zip(x[('Product')],x[('Flow')])}.keys())).reset_index()
    product_flow = pd.merge(product_flow2,product_flow1,on=['From','To'])
    product_flow.columns = ['From','To','Product','Flow']
    suppliers, factories, depots, customers = ["S1", "S2",], ["F1", "F2",], ["D1", "D2",], ["C1", "C2", "C3", "C4",]
    G = nx.DiGraph()
    G.add_nodes_from(suppliers)
    G.add_nodes_from(factories)
    G.add_nodes_from(depots)
    G.add_nodes_from(customers)
    G.add_edges_from([(arc[0], arc[1]) for arc in product_flow[["From", "To"]].values])
    pos = {node: (0, 2+i) for i, node in enumerate(suppliers)}
    pos.update({node: (1, 2+i) for i, node in enumerate(factories)})
    pos.update({node: (2, 2+i) for i, node in enumerate(depots)})
    pos.update({node: (3-0.1*(i-1.5)**4, 1+i) for i, node in enumerate(customers)})
    node_color = ['#ca0636']*len(suppliers) + ['#cc8583']*len(factories) + ['#ffe4e1']*len(depots) + ['#59b7d3']*len(customers)
    node_color = ['#2db6da']*len(suppliers) + ['#27dcc3']*len(factories) + ['#c797d2']*len(depots) + ['#97afb9']*len(customers)

    nx.draw(G, pos, with_labels=True, node_color=node_color, node_size=1000, font_size=8, font_color='black', font_weight='bold')
    nx.draw_networkx_edge_labels(G, pos, edge_labels={(arc[0], arc[1]): "{}".format(arc[3]) for arc in product_flow[["From", "To", "Product", "Flow"]].values}, label_pos=0.35, font_size=8,horizontalalignment='center',verticalalignment='center',rotate=True,)
    objVal = sum([node.objVal for node in node_list])
    plt.text(0., 3.5, "Total Cost: {:.2f}".format(round(objVal)), fontsize=12, fontweight='bold')
    plt.text(0., 4, "Demand unsatisfied: {:.0f}".format(node_list[-1].unstdemand), fontsize=12, fontweight='bold')
    plt.show()
    

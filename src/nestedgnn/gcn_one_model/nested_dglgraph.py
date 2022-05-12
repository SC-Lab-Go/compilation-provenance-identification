import torch
from dgl import DGLGraph
from graph_util_graph import *

class Nested_DGLGraph:

    def __init__(self, nested_graph, self_loop, cuda):

        self.outer_graph = self.process(nested_graph.graph, self_loop, cuda)
        self.inner_graphs = []

        for graph_one in nested_graph.inner_graphs:
            self.inner_graphs.append(self.process(graph_one, self_loop, cuda))

    def process(self, graph, self_loop, cuda):

        if self_loop:
            graph.remove_edges_from(graph.selfloop_edges())
            graph.add_edges_from(zip(graph.nodes(), graph.nodes()))
        g = DGLGraph(graph)
        #n_edges = g.number_of_edges()
        # normalization
        degs = g.in_degrees().float()
        norm = torch.pow(degs, -0.5)
        norm[torch.isinf(norm)] = 0
        if cuda:
            norm = norm.cuda()
        g.ndata['norm'] = norm.unsqueeze(1)
        return g


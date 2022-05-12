"""GCN using DGL nn package
References:
- Semi-Supervised Classification with Graph Convolutional Networks
- Paper: https://arxiv.org/abs/1609.02907
- Code: https://github.com/tkipf/gcn
"""
import torch
import torch.nn as nn
from dgl.nn.pytorch import GraphConv
from nested_dglgraph import Nested_DGLGraph
from gcn import myGCN
from gcn import graphGCN

class NestedGCN(nn.Module):
    def __init__(self,
                 inner_graph_feats,
                 in_feats_inner,
                 n_hidden,
                 n_classes,
                 n_layers,
                 activation,
                 dropout):
        super(NestedGCN, self).__init__()
        self.inner_graph_feats = inner_graph_feats

        self.model_outer = graphGCN(inner_graph_feats,
                                    n_hidden,
   #                                 n_hidden,
                                    n_classes,
                                    n_layers,
                                    activation,
                                    dropout)
        self.model_inner = myGCN(in_feats_inner,
                                    n_hidden,
                                    inner_graph_feats,
                                    n_layers,
                                    activation,
                                    dropout)

    def forward(self, g, inner_features):
        temp_features = []
        for i in range(len(g.inner_graphs)):
# TODO: node features should be different or none
#            print(i)
            h_inner = self.model_inner(g.inner_graphs[i], inner_features[i])
# TODO: node features in the outer graph, or concatanate
            h_graph = torch.mean(h_inner, dim = 0)
            #logits = torch.mean(logits, dim = 0)
            temp_features.append(h_graph)
#        print(len(g.inner_graphs), temp_features)
# Why feature length is zero
        if len(temp_features) == 0:
            zero_feature = [0.0] * self.inner_graph_feats
#            print(zero_feature)
            temp_features = [torch.FloatTensor(zero_feature).cuda()]
        features_new = torch.stack(temp_features)
        h = self.model_outer(g.outer_graph, features_new)
#        h = torch.mean(h, dim = 0)
        return h


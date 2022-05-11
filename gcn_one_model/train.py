import argparse, time
import numpy as np
import torch
import torch.nn as nn
import torch.nn.functional as F
from dgl import DGLGraph
from dgl.data import register_data_args, load_data
from graph_util_graph import *
from gcn import myGCN
from nested_gcn import NestedGCN
from sklearn.metrics import classification_report
from nested_dglgraph import Nested_DGLGraph

#from gcn_mp import GCN
#from gcn_spmv import GCN

def get_deeper_analysis(predicted, labels):
    print("deeper analysis\n")
    print('labels: ',labels)
    print('predicted: ',predicted)
    report = classification_report(labels, predicted)
    print(report)

def evaluate(model, graph, features, labels, mask):
    model.eval()
    with torch.no_grad():
        logits = model(graph, features)
        logits = logits[mask]
        labels = labels[mask]
        _, indices = torch.max(logits, dim=1)
        get_deeper_analysis(indices.cpu().numpy(), labels.cpu().numpy())

        correct = torch.sum(indices == labels)
        #print(indices.shape)
        return correct.item() * 1.0 / len(labels)

#def evaluate_nested_graph_embedding(model, g, inner_features, labels, mask):
def evaluate_nested_graph_embedding(model, nested_dglgraphs, inner_features, labels, mask):
    model.eval()

    with torch.no_grad():
        predicted = []
        real_labels = []
        correct = 0

        for i in range(len(mask)):
            if int(mask[i]) == 1 and i < len(nested_dglgraphs):
              #  print(i, labels[i].data)
                logits = model(nested_dglgraphs[i], inner_features[i])
#                logits = logits[mask]
#                labels = labels[mask]
                _, l = torch.max(logits, dim=1)
#                print(l[0].item(), labels[i].item())
                predicted.append(l[0].item())
                real_labels.append(labels[i].item())

                if l[0] == labels[i]:
                    correct += 1
#        print(predicted)
#        print(real_labels)
        #get_deeper_analysis(np.array(predicted), np.array(real_labels))
        get_deeper_analysis(np.array(predicted), np.array(real_labels))
        #print(indices.shape)

        return correct * 1.0 / mask.sum().item()


def main(args):
    # load and preprocess dataset
    #data = load_data(args)
# Load my own data
    #args.dataset='/home/UNT/mi0214/NestedGNN_compromised_host/lanl_2015/user_graph'
    print("Dataset: ",args.dataset)
    print("args.selfloop: ",args.selfloop)
    data = load_nested_many(args)
    print(type(data))
    #print('Train Mask: ',data.graphs[1])
    #print('Test Mask: ',sum(data.test_mask))
#    print(data.train_mask)
#    print(data.val_mask)
#    print(data.test_mask)

#    for g in data.inner_graphs:
#        print(g.number_of_nodes(), g.number_of_edges())
#    print(len(data.inner_graphs))
#    exit()
#    print(list(data.features[0]))
#    features = torch.FloatTensor(data.features)
#    inner_features = []
#    for one in data.inner_features:
#        inner_features.append(torch.FloatTensor(one))

    labels = torch.LongTensor(data.labels)
    print("Labels: ",labels)
    
    #train_mask = torch.ByteTensor(data.train_mask)
    #val_mask = torch.ByteTensor(data.val_mask)
    #test_mask = torch.ByteTensor(data.test_mask)
    train_mask = torch.ByteTensor(data.train_mask)
    val_mask = torch.ByteTensor(data.val_mask)
    test_mask = torch.ByteTensor(data.test_mask)
    
    print("train_mask: ",train_mask)
    print('test_mask',test_mask)
    #exit(-1)
#    in_feats = features.shape[1]
#    in_feats_inner = inner_features[0].shape[1]
    n_classes = data.num_labels
    n_graphs = data.num_graphs
#    n_nodes = data.graph.number_of_nodes()
#    n_edges = data.graph.number_of_edges()
# Weight for imbalanced labels
    
    #- weight = torch.FloatTensor(np.array([1, 2]))
    weight = torch.FloatTensor(np.array([1, 2, 3, 4,5,6]))
    #print(weight)
    inner_graph_feats = 16
#    n_classes = 2
    in_feats_inner = 9

    print("""----Data statistics------'
      #Graphs %d
      #inner_graph_feats %d
      #in_feats_inner %d
      #Classes %d
      #Train samples %d
      #Val samples %d
      #Test samples %d""" %
          (n_graphs, inner_graph_feats, in_feats_inner, n_classes,
              train_mask.sum().item(),
              val_mask.sum().item(),
              test_mask.sum().item()))

#    exit()
    if args.gpu < 0:
        cuda = False
    else:
        cuda = True
        torch.cuda.set_device(args.gpu)
#        features = features.cuda()
#        for i in range(len(inner_features)):
#            inner_features[i] = inner_features[i].cuda()
        labels = labels.cuda()
        weight = weight.cuda()
        train_mask = train_mask.cuda()
        val_mask = val_mask.cuda()
        test_mask = test_mask.cuda()
#    in_feats = features.shape[1]
#    print(in_feats)
#    # graph preprocess and calculate normalization factor

    # create GCN model
#    model = GCN(g,
#                in_feats,
#                args.n_hidden,
#                n_classes,
#                args.n_layers,
#                F.relu,
#                args.dropout)
# Two models, one for outer, another for inner, they could use different parameters

    model = NestedGCN(inner_graph_feats,
                    in_feats_inner,
                    args.n_hidden,
                    n_classes,
                    args.n_layers,
                    F.relu,
                    args.dropout)
    if cuda:
        model.cuda()
#    loss_fcn = torch.nn.CrossEntropyLoss(weight)
    loss_fcn = torch.nn.CrossEntropyLoss()
    #loss_fcn = torch.nn.CrossEntropyLoss()
#    loss_fcn = torch.nn.BCEWithLogitsLoss()
    # use optimizer
#    for key in model_outer.parameters():
#        print(key, type(key), key.shape)
#        print()
#    exit()
#        print(key, model_outer.parameters()[key])
#    print(model_outer.parameters())
#    print(model_inner.parameters())
    optimizer = torch.optim.Adam(model.parameters(), lr=args.lr, weight_decay=args.weight_decay)
    #optimizer = torch.optim.Adam(model_outer.parameters(), lr=args.lr, weight_decay=args.weight_decay)
    #optimizer = torch.optim.Adam(model_outer.parameters(), lr=args.lr, weight_decay=args.weight_decay)
    # initialize graph
# Changed

    nested_dglgraphs = []
    inner_features = []

# =============================================================================
#     count = 0;
#     for i in range(data.num_graphs):
# #        print(i, data.graphs[i].graph.number_of_nodes(), len(data.graphs[i].inner_graphs))
#         item = data.graphs[i]
#         print('------- GRAPH %d-------',i)
#         print("data.graphs[i]: ",type(item))
#         print("data.graphs[i].labels: ",data.graphs[i].labels)
#         print("# data.graphs[i].features: ",len(data.graphs[i].features))
#         
#         print("data.graphs[i].graph.node(): ",(data.graphs[i].graph.node()))
#         print("data.graphs[i].graph.edges(): ",(data.graphs[i].graph.edges()))
#         print("data.graphs[i].inner_features: ",(data.graphs[i].inner_features))
#         print("data.graphs[i].inner_graphs: ",(data.graphs[i].inner_graphs[i].edges()))
#         
#         print("# Nodes: ",len(data.graphs[i].graph.node()))
#         print("#Edges: ",len(data.graphs[i].graph.edges()))
#         print("#inner_features: ",len(data.graphs[i].inner_features))
#         print("#inner_graphs: ",len(data.graphs[i].inner_features))
#         count= count + 1
#         if count>=1:
#             exit(-1)
# =============================================================================

#Debugging information loop
# =============================================================================
#     for i in range(data.num_graphs):
# #        print(i, data.graphs[i].graph.number_of_nodes(), len(data.graphs[i].inner_graphs))
#         args.selfloop = True
#         g = Nested_DGLGraph(data.graphs[i], args.selfloop, cuda)
#         feat = data.graphs[i].inner_features
#         feat_tensor = []
#         print("g.outer_graph",g.outer_graph.edges())
#         print("inner_graphs",g.inner_graphs[i].edges())
#         print("feat",feat[i])
#         for one in feat:
#             print(one)
#         break
#         
# =============================================================================
        
    for i in range(data.num_graphs):
#        print(i, data.graphs[i].graph.number_of_nodes(), len(data.graphs[i].inner_graphs))
        args.selfloop = True
        g = Nested_DGLGraph(data.graphs[i], args.selfloop, cuda)
        feat = data.graphs[i].inner_features
        feat_tensor = []
        for one in feat:
            if cuda:
                feat_tensor.append((torch.FloatTensor(one)).cuda())
            else:
                feat_tensor.append((torch.FloatTensor(one)))
#        if cuda:
#            feat_tensor.append((torch.FloatTensor(feat)).cuda())
#        else:
#            feat_tensor.append((torch.FloatTensor(feat)))


        nested_dglgraphs.append(g)
        inner_features.append(feat_tensor)

#    for one in data.inner_features:
#        inner_features.append(torch.FloatTensor(one))
    print("len(nested_dglgraphs) %s" %(len(nested_dglgraphs)))

    dur = []
    model.train()
    for epoch in range(args.n_epochs):
        loss_list = []
        if epoch >= 3:
            t0 = time.time()

        for i in range(len(train_mask)):
            if int(train_mask[i]) == 1 and i < len(nested_dglgraphs):
              #  print(i, labels[i].data)
                #print(i, len(nested_dglgraphs), len(inner_features))
                #debug
                #print("nested_dglgraphs[i]: ",nested_dglgraphs[i].outer_graph.edges())
                #print("inner_features[i]: ",len(inner_features[i]))
                #exit(-1)
                logits = model(nested_dglgraphs[i], inner_features[i])
                #print("logits = %s" %(logits))

                loss = loss_fcn(logits, labels[i].unsqueeze(0))
                #loss_list.append(loss.detach().numpy())
                loss_list.append((loss.detach()).cpu().numpy())

                optimizer.zero_grad()
                loss.backward()
                #loss.backward(retain_graph = True)
                optimizer.step()

        if epoch >= 3:
            dur.append(time.time() - t0)
#            break
#
        if epoch % 1 == 0:
            #print("sum(val_mask): ",sum(val_mask))
            if sum(val_mask) > 0:
                acc = evaluate_nested_graph_embedding(model, nested_dglgraphs, inner_features, labels, val_mask)
#            acc = evaluate(model, features, labels, train_mask)
#            acc = evaluate(model_outer, g.outer_graph, features_new, labels, train_mask)
#            print("Epoch {:05d} | Time(s) {:.4f} | Loss {:.4f} | Accuracy {:.4f}". format(epoch, np.mean(dur), loss.item(), acc))
            #acc = evaluate(model_outer, g.outer_graph, features_new, labels, val_mask)
            #print("Epoch {:05d} | Time(s) {:.4f} | Loss {:.4f} | Accuracy {:.4f} | " "ETputs(KTEPS) {:.2f}". format(epoch, np.mean(dur), loss.item(), acc, n_edges / np.mean(dur) / 1000))
                print("Epoch {:05d} | Time(s) {:.4f} | Loss {:.4f} | Accuracy {:.4f}". format(epoch, np.mean(dur), np.mean(np.array(loss_list)), acc))
        if epoch % 2 == 1:
            time_infer = time.time()
            acc = evaluate_nested_graph_embedding(model, nested_dglgraphs, inner_features, labels, test_mask)
   # acc = evaluate_nested(model, g, inner_features, labels, test_mask)
#    acc = evaluate(model_outer, g.outer_graph, features_new, labels, test_mask)
            print("Test Accuracy | Epoch {:05d} | Time(s) {:.4f} | Loss {:.4f} | Accuracy {:.4f}". format(epoch, np.mean(dur), np.mean(np.array(loss_list)), acc))         
           #print("Test Accuracy {:.4f} | Time(s) {:.4f}".format(acc, time.time() - time_infer))
#    exit(0)

#    print()
    time_infer = time.time()
    acc = evaluate_nested_graph_embedding(model, nested_dglgraphs, inner_features, labels, test_mask)
   # acc = evaluate_nested(model, g, inner_features, labels, test_mask)
#    acc = evaluate(model_outer, g.outer_graph, features_new, labels, test_mask)
    print("Test Accuracy {:.4f} | Time(s) {:.4f}".format(acc, time.time() - time_infer))


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='GCN')
    register_data_args(parser)
    parser.add_argument("--dropout", type=float, default=0.5,
            help="dropout probability")
    parser.add_argument("--gpu", type=int, default=-1,
            help="gpu")
    parser.add_argument("--lr", type=float, default=1e-2,
            help="learning rate")
    parser.add_argument("--n-epochs", type=int, default=100,
            help="number of training epochs")
    #parser.add_argument("--dataset",help="dataset folder")
    parser.add_argument("--n-hidden", type=int, default=8,
            help="number of hidden gcn units")
#    parser.add_argument("--inner_graph_feats", type=int, default=16,
#            help="number of inner graph features")
    parser.add_argument("--n-layers", type=int, default=2,
            help="number of hidden gcn layers")
    parser.add_argument("--weight-decay", type=float, default=5e-4,
            help="Weight for L2 loss")
    parser.add_argument("--selfloop", action='store_true',
            help="graph self-loop (default=False)")
    parser.set_defaults(selfloop=False)
    args = parser.parse_args()
    print(args)

    print("python3 -W ignore train.py --dataset /home/yuede/yuede_at_raid0_24TB/lanl_2015/loadable_graph/ --gpu 0 --self-loop --n-epochs 10")
    main(args)

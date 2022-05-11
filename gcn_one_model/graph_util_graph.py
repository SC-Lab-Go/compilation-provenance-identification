import os
import csv
import numpy as np
import networkx as nx
import time
import multiprocessing
import pickle as pk
from dgl.data import register_data_args

class nested_one:
    def __init__(self):
    # should be numpy array
        self.features = np.array([[]])
        self.labels = np.array([])
        self.train_mask = np.array([])
        self.val_mask = np.array([])
        self.test_mask = np.array([])
        self.num_labels = 0
        self.graph = nx.DiGraph()
        self.inner_graphs = []
        self.inner_features = []
        self.in_feats_inner = 9
#        self.inner_nodes = 6607

    def update_graph(self):

#        print(len(self.inner_graphs), self.graph.number_of_nodes())

        if self.graph.number_of_nodes() < len(self.inner_graphs):
            node_set = set(self.graph.nodes())
            for i in range(len(self.inner_graphs)):
                if i not in node_set:
                    self.graph.add_node(i)
        #print(self.labels.size, self.features.size, self.graph.number_of_nodes())


# Option 1: normalized compact graph, each node has a one-hot embedding, identity matrix
    def load_edge_list(self, outer_graph_file,args, limit = None, inner = False):
        graph = nx.DiGraph()
# If the graph does not exist, we simply return an empty graph
        if not os.path.isfile(outer_graph_file):
            graph.add_node(0)
            return graph
        with open(outer_graph_file, "r") as fp:
            if not limit:
                for line in csv.reader(fp):
                    graph.add_edge(int(line[0]), int(line[1]))
                    #print("Edge ",line)
            else:
                for line in csv.reader(fp):
                    u, v = int(line[0]), int(line[1])
                    
                    if u >= limit:
                        break
                    if v >= limit:
                        continue
                    graph.add_edge(u, v)
                    
        if graph.number_of_nodes() == 0:
            graph.add_node(0)
        if args.selfloop:
            for node in graph.nodes():
                graph.add_edge(node, node)
        
        return graph
#        print(self.graph.number_of_nodes(), self.graph.number_of_edges())

# Option 2: unified sparse graph, same node
#    def load_edge_list(self, outer_graph_file, limit = None, inner = False):
#        graph = nx.DiGraph()
#        with open(outer_graph_file, "r") as fp:
#            if not limit:
#                for line in csv.reader(fp):
#                    graph.add_edge(int(line[0]), int(line[1]))
#            else:
#                for line in csv.reader(fp):
#                    u, v = int(line[0]), int(line[1])
#                    if u >= limit:
#                        break
#                    if v >= limit:
#                        continue
#                    graph.add_edge(u, v)
#        if inner:
#            node_set = set(graph.nodes())
#            for i in range(self.inner_nodes):
#                if i not in node_set:
#                    graph.add_node(i)
#        return graph
#        print(self.graph.number_of_nodes(), self.graph.number_of_edges())

    def load_label(self, label_split_file, limit = None):
        label_list = []
        split_list = []
        label_set = set()
# Step 1: get label array
        index = 0
        with open(label_split_file, "r") as fp:
            for line in csv.reader(fp):
                index += 1
                if limit and index > limit:
                    break
                label_list.append(int(line[0]))
                split_list.append(int(line[1]))
                if int(line[0]) not in label_set:
                    label_set.add(int(line[0]))

        l = len(label_list)
        self.labels = np.array(label_list)
        self.num_labels = len(label_set)

# Step 2: get mask array
        self.train_mask = np.zeros(l)
        self.val_mask = np.zeros(l)
        self.test_mask = np.zeros(l)
        for i in range(l):
            if split_list[i] == 0:
                self.train_mask[i] = 1
            elif split_list[i] == 1:
                self.val_mask[i] = 1
            else:
                self.test_mask[i] = 1
#        print(self.num_labels, np.sum(self.train_mask), np.sum(self.val_mask), np.sum(self.test_mask))

    def load_feature(self, graph, feature_file, is_inner = False):
        #print("feature_file: ",feature_file)
        #self.features = np.random.rand(self.graph.number_of_nodes(), 20)
        if is_inner:
            feature_matrix = []
            if not os.path.isfile(feature_file):
                feature_vector = []
                for i in range(self.in_feats_inner):
                    feature_vector.append(0)
                feature_vector[0] = 1
                feature_matrix.append(feature_vector)

            if os.path.isfile(feature_file):
                with open(feature_file, "r") as fp:
                    for line in csv.reader(fp):
                        
                        feature_vector = []
                        for one in line:
                            feature_vector.append(float(one))
                        feature_matrix.append(feature_vector)
#                        print(len(feature_vector))
            if len(feature_matrix) == 0:
                feature_vector = [0 for i in range(self.in_feats_inner)]
                feature_matrix.append(feature_vector)

            #print("----",len(feature_matrix))
            return feature_matrix
        else:
            features = np.ones((graph.number_of_nodes(), 1))
            return features

    #def load_data(self, outer_graph_file, label_split_file, feature_file, limit = None):
    def load_data(self, outer_graph_file, feature_file, args,label_split_file = None, limit = None):
        self.graph = self.load_edge_list(outer_graph_file,args, limit)
        #print("self.graph: ",nx.to_dict_of_dicts(self.graph))
        if label_split_file:
            self.load_label(label_split_file, limit)
        self.features = self.load_feature(self.graph, feature_file)

    def get_inner_graph_index(self, index_file):
        inner_graph_list = []
        with open(index_file, "r") as fp:
            for line in csv.reader(fp):
                inner_graph_list.append(line[0])
        #print('get_inner_graph_index: ',inner_graph_list)
        return inner_graph_list

    def deal_one(self, inner_graph_folder, inner_graph_list, shared_list, s, e):

        for i in range(len(inner_graph_list)):
            graph_file = os.path.join(inner_graph_folder, inner_graph_list[i] + ".edge_list")
            graph = self.load_edge_list(graph_file)
#            self.inner_graphs.append(graph)
            shared_list[s + i] = graph

    def load_inner_graph_parallel(self, data_folder, inner_graph_folder, index_file = None):
        if not index_file:
            index_file = os.path.join(data_folder, "merged_vertex_index_sampled.txt")
        inner_graph_list = self.get_inner_graph_index(index_file)


        num_core = min(multiprocessing.cpu_count(), len(inner_graph_list))
        step = int(len(inner_graph_list) / num_core)

        if num_core * step < len(inner_graph_list):
            step += 1

        manager = multiprocessing.Manager()
        shared_list = manager.list(range(len(inner_graph_list)))
#        for i in range(inner_graph_list):
#            shared_list.append(
        jobs = []
#        begin_time = time.time()
        for i in range(num_core):
            s = step * i
            if s > len(inner_graph_list):
                continue
            e = min(s + step, len(inner_graph_list))

            graph_list_temp = inner_graph_list[s: e]
            p = multiprocessing.Process(target = self.deal_one, args = (inner_graph_folder, graph_list_temp, shared_list, s, e))
            jobs.append(p)
            p.start()

        for p in jobs:
            p.join()
        for i in range(len(inner_graph_list)):
            self.inner_graphs.append(shared_list[i])


    def load_inner_graph_and_feature(self, graph_name, graph_folder, inner_graph_folder, args,index_file = None, limit = None):
        if not index_file:
            index_file = os.path.join(graph_folder, "merged_vertex_index_sampled.txt")
        
        
        inner_graph_list = self.get_inner_graph_index(index_file)
        
#        print(inner_graph_list)
#        exit()
#        print(len(inner_graph_list))
        #print("graph_name", graph_name, len(inner_graph_list))
        for i in range(len(inner_graph_list)):
            inner_graph_name = str(i)
            graph_file = os.path.join(inner_graph_folder, inner_graph_name + ".edge_list")
            graph = self.load_edge_list(graph_file,args ,inner = True)
            
#            print(graph_file, graph.number_of_nodes())

            feature_file = os.path.join(inner_graph_folder, inner_graph_name + ".feat")
            feature = self.load_feature(graph, feature_file, is_inner = True)
            #print(graph.nodes())
            
            
#            print(len(feature), len(feature[0]), graph.number_of_nodes())
            # add orphan node to graph
            if graph.number_of_nodes() < len(feature):
                node_set = set(graph.nodes())
                for v in range(len(feature)):
                    if v not in node_set:
                        graph.add_node(v)

            self.inner_graphs.append(graph)
            self.inner_features.append(feature)
            
            
            if limit and i == limit - 1:
                break
#        exit(0)

class nested_many:
    def __init__(self):
        self.graphs= []
        self.train_mask = np.array([])
        self.val_mask = np.array([])
        self.test_mask = np.array([])
        self.num_labels = 0
        self.num_graphs = 0
        self.labels = np.array([])
        self.in_feats_inner = 1000 #3162 # ToDo: double check

    def load_data(self, graph_folder, label_split_file, args,graph_list = None, limit = None):
#        self.graph = self.load_edge_list(outer_graph_file, limit)
        if not graph_list:
            graph_list = self.load_label(label_split_file, limit)
        else:
            self.load_label(label_split_file, limit)
#        print(graph_list)
#        exit(0)

        
        self.graphs = self.load_nested_many(graph_list, graph_folder, args,limit)
        self.num_graphs = len(self.graphs)
        

#        self.features = self.load_feature(self.graph, feature_file)
#        print("# of graphs, %s\n", len(self.data))
#        for g in self.data:
#            print(g.graph.number_of_nodes())

    def get_graph_list(self, inner_list_file):
        inner_list = []
        with open(inner_list_file, "r") as fp:
            for line in csv.reader(fp):
                inner_list.append(line[1].strip())
        return inner_list

    def load_host_map(self, host_map_file):
        host_map = {}
        with open(host_map_file, "r") as fp:
            for line in csv.reader(fp):
                host_map[line[1].strip()] = line[0]
        return host_map


    def load_nested_many(self, graph_list, graph_folder,args, limit = None):
        nested_graphs = []

        pk_file = os.path.join(graph_folder, "nested_many1.pk")
        if os.path.isfile(pk_file):
#        if False:
            print("Loading nested graphs from nested_many.pk")
            nested_graphs = pk.load(open(pk_file, "rb"))
        else:
            print("Loading nested graphs from raw files")
            for graph_name in graph_list:
                graph_path = os.path.join(graph_folder, graph_name + ".edge_list")
                feat_path = os.path.join(graph_folder, graph_name + ".feat")
#                pas = nested_one()
#                pas.load_data(graph_path, feat_path, None, limit)
                
                outer_graph = nested_one()
                outer_graph.load_data(graph_path, feat_path,args, None, limit)
                #print("outer_graph: ",outer_graph.in_feats_inner)
                #print("outer_graph: ",outer_graph.inner_graphs)
                
#                exit(0)

#                print(outer_graph)
#                exit(0)
                #nested_graphs.append(pas)

                inner_graph_list_file = os.path.join(graph_folder, graph_name + ".map")
#            inner_graph_list = self.get_graph_list(inner_list_file)
                inner_graph_folder = os.path.join(graph_folder, graph_name + "_inner")
#                host_map = self.load_host_map(os.path.join(graph_folder, graph_name + ".map"))
#                print(inner_graph_list_file, inner_graph_folder, host_map)
#                exit(0)

                outer_graph.load_inner_graph_and_feature(graph_name, graph_folder, inner_graph_folder,args, inner_graph_list_file, limit)
                outer_graph.update_graph()
                nested_graphs.append(outer_graph)
                
#                print(outer_graph)
#                for one in outer_graph:
#                    print(one, outer_graph
#                exit(0)
            
            
                #print("outer_graph: ",outer_graph)
            #print("nested_graphs[0:10]: ",graph_name,nx.Graph(nested_graphs[0].graph).nodes())
            #exit(-1)
            pk.dump(nested_graphs, open(pk_file, "wb"))
        print("# of graphs, %s" %(len(nested_graphs)))
        return nested_graphs

    def load_label(self, label_split_file, limit = None):
        label_list = []
        split_list = []
        instance_list = []
        label_set = set()
        #print("label_split_file: ",label_split_file)
# Step 1: get label array
        index = 0
        with open(label_split_file, "r") as fp:
            for line in csv.reader(fp):
                #print("line: ",line)
                index += 1
                if limit and index > limit:
                    break
                instance_list.append(line[0])
                label_list.append(int(line[1]))
                split_list.append(int(line[2]))
                if int(line[0]) not in label_set:
                    label_set.add(int(line[1]))
        l = len(label_list)
        self.labels = np.array(label_list)
        self.num_labels = len(label_set)

# Step 2: get mask array
        self.train_mask = np.zeros(l)
        self.val_mask = np.zeros(l)
        self.test_mask = np.zeros(l)
        for i in range(l):
            if split_list[i] == 0:
                self.train_mask[i] = 1
            elif split_list[i] == 1:
                self.val_mask[i] = 1
            else:
                self.test_mask[i] = 1
        return instance_list

def load_nested_many(args):
    data_folder = args.dataset

    if not os.path.isdir(data_folder):
        raise ValueError("%s does not exist" %(data_folder))
    else:
        print("%s exists" %(data_folder))

    if "user_graph" in data_folder:
        time_beg = time.time()
        user_list = []
        with open(os.path.join(data_folder, "user_undersample.txt"), "r") as fp:
        #with open(os.path.join(data_folder, "user_10.txt"), "r") as fp:
            for line in fp:
                user_list.append(line.strip())
        label_split_file = os.path.join(data_folder, "label_split.csv")
        nested_data = nested_many()
        
        nested_data.load_data(data_folder, label_split_file, user_list,args)
        time_end = time.time()

        print("Time of loading nested graphs, %.3lf" %(time_end - time_beg))
        return nested_data

    elif "malware" or "output_folder" or "baseline_graph" in data_folder:
        time_beg = time.time()
        label_split_file = os.path.join(data_folder, "label_split_311.csv")
        nested_data = nested_many()
        #print("Train Mask",nested_data.train_mask)
        nested_data.load_data(data_folder, label_split_file,args)
#        nested_data.load_data(data_folder, label_split_file, limit = 100)
        #print(nested_data.labels)
        time_end = time.time()
        print("Time of loading nested graphs, %.3lf" %(time_end - time_beg))
        return nested_data


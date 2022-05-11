#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Apr 21 00:38:15 2022

@author: mi0214
"""


import os
import sys
import csv
import json
import networkx as nx
from os import listdir
from os.path import isfile, join
compilerList = ["GCC", "ICC", "CLANG", "LLVM", "PGI"]

## merge Binary & Function
#class BinaryFunction:
#    def __init__(self):
#        # Part 1: from Binary
#        self.name = ""
#        self.label = ""
#        self.n_functions = 0
#        self.fcg_edge_list = []
##        self.function_name = [] # the function name list, ordered
#        self.function_feature = [] # the predefined features for each function. Empty for now, TODO
#        # Part 2: from function
#        self.function_name = [] # ordered
#        self.function_address = [] # ordered, in decimal
#        self.function_size = [] # per function per number of nodes
#        self.function_cfg_edge_list = [] # per function per list of (cfg)
#        self.function_block_addr = [] # per function per list of (block address)
#        self.function_block_feature = [] # per function per list of (block feature vectors)



def load_json(file_path):
    fp = open(file_path, "r")
    json_str = json.load(fp)
    binary_json = json.loads(json_str)
#    print(type(binary_json))
#    print(binary_json.keys())
    fp.close()
    return binary_json

def dump_edge_list(edge_list, graph_file):
    with open(graph_file, "w") as fp:
        for edge in edge_list:
            fp.write(','.join([str(edge[0]), str(edge[1])]) + '\n')

def dump_feat_list(function_feature, feat_file):
    with open(feat_file, "w") as fp:
        for feature in function_feature:
            output = ','.join([str(x) for x in feature])
            fp.write(output + '\n')

def dump_map(function_name, function_address, map_file):
    with open(map_file, "w") as fp:
        for i in range(len(function_name)):
            fp.write(','.join([function_name[i], str(function_address[i])]) + '\n')

def generate_nested_graph(binary_json, index, output_path):

# Step 1: outer graph
    outer_graph_file = os.path.join(output_path, "%s.edge_list" %(index))
    outer_feat_file = os.path.join(output_path, "%s.feat" %(index))

    outer_inner_map = os.path.join(output_path, "%s.map" %(index))

    dump_edge_list(binary_json['fcg_edge_list'], outer_graph_file)
    dump_feat_list(binary_json['function_feature'], outer_feat_file)

    dump_map(binary_json['function_name'], binary_json['function_address'], outer_inner_map)

# Step 2: inner graph
    inner_graph_folder = os.path.join(output_path, "%s_inner" %(index))
    if not os.path.exists(inner_graph_folder):
        os.mkdir(inner_graph_folder)

    for func_id in range(binary_json['n_functions']):
        inner_graph_file = os.path.join(inner_graph_folder, "%s.edge_list" %(func_id))
        dump_edge_list(binary_json['function_cfg_edge_list'][func_id], inner_graph_file)

        inner_feat_file = os.path.join(inner_graph_folder, "%s.feat" %(func_id))
        dump_feat_list(binary_json['function_block_feature'][func_id], inner_feat_file)


def getGroundTruth(binfile_name):
	comp_name = ""
	version = ""
	opt_lvl = ""
	for comp in compilerList:
		if binfile_name.find(comp.lower()) != -1:
			comp_name = comp
			sub = binfile_name.find(comp.lower())
			rem_sub_string = binfile_name[sub:len(binfile_name)]
			_,ver_opt = rem_sub_string.split("-")
			version = ver_opt[0:len(ver_opt)-3]
			opt_lvl = ver_opt[len(ver_opt)-2:len(ver_opt)]
			#print comp_name+version+opt_lvl
			break
	return (comp_name,version,opt_lvl)

def main(input_path, output_path):

    file_list = os.listdir(input_path)
    file_name_list = []
    label_list=[]
    
    print(file_list)

    index = 0
    for file_one in file_list:
        if file_one.endswith(".json"):
            file_path = os.path.join(input_path, file_one)
            print(file_path)
#            print(file_path)
# Step 1: Load the json file of each binary
            binary_json = load_json(file_path)
            #print(binary_json)
            
# Step 2: Generate the nested graph for binary_json
            
            file_name = file_one[:-5]
            file_name_list.append(file_name)
            generate_nested_graph(binary_json, index, output_path)
            index += 1
            
            #get groundtruthlabel
            cmp,ver,opt= getGroundTruth(file_name)
            #print(cmp+"_"+ver+"_"+opt)
            lbl = cmp+"_"+ver+"_"+opt
            label_list.append(lbl)
            #print(label_list)
            if index % 100 == 0:
                print(index)
#            break
                
# Step 3: Save file_name_list
    index_file = os.path.join(output_path, "graph_index.csv")
    with open(index_file, "w") as fp:
        for i in range(index):
            fp.write(','.join([str(i),label_list[i] ,file_name_list[i]]) + '\n')
    
    
    labels = set(label_list)
    print(labels)
       
    label_file = os.path.join(output_path, "labels_list.csv")
    with open(label_file, "w") as fp:
        i = 0
        for lbl in labels:
            fp.write(','.join([str(i),lbl]) + '\n')
            i=i+1

#    print(file_name_list)

if __name__ == "__main__":
    if len(sys.argv) != 3:
        print("Usage: python load_binary_json.py <input_path> <output_path>\n")
        exit(-1)
    main(sys.argv[1], sys.argv[2])



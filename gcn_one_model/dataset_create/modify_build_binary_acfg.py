#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Apr 21 14:25:44 2022

@author: mi0214
"""


import os
import sys
import csv
import json
import networkx as nx

compilerList = ["GCC", "ICC", "CLANG", "LLVM", "PGI"]

# merge Binary & Function
class BinaryFunction:
    def __init__(self):
        # Part 1: from Binary
        self.name = ""
        self.label = ""
        self.n_functions = 0
        self.fcg_edge_list = []
#        self.function_name = [] # the function name list, ordered
        self.function_feature = [] # the predefined features for each function. Empty for now, TODO
        # Part 2: from function
        self.function_name = [] # ordered
        self.function_address = [] # ordered, in decimal
        self.function_size = [] # per function per number of nodes
        self.function_cfg_edge_list = [] # per function per list of (cfg)
        self.function_block_addr = [] # per function per list of (block address)
        self.function_block_feature = [] # per function per list of (block feature vectors)
    def merge(self, binary):
        self.name = binary.name
        self.label = binary.label
        self.n_functions = binary.n_functions
        self.fcg_edge_list = binary.fcg_edge_list

        for function in binary.function_list:
            self.function_name.append(function.name)
            self.function_address.append(function.addr)
            self.function_size.append(function.n_blocks)
            self.function_cfg_edge_list.append(function.cfg_edge_list)
            self.function_block_addr.append(function.block_addr)
            self.function_block_feature.append(function.block_feature)

class Function:
    def __init__(self):
        self.name = ""
        self.addr = 0 # in decimal
        self.n_blocks = 0
        self.cfg_edge_list = []
        self.block_addr = [] # the starting addr of each block, ordered
        self.block_feature = [] # one feature per node, ordered

class Binary:
    def __init__(self):
        self.name = ""
        self.label = ""
        self.n_functions = 0
        self.fcg_edge_list = []
#        self.function_name = [] # the function name list, ordered
        self.function_list = [] # the list of Function objects, ordered
        self.function_feature = [] # the predefined features for each function. Empty for now, TODO
        # Three temporary files, empty after loading
        self.cfg_edge_list = []
        self.block_feature = []
        self.block_addr = []
        self.function2block = {}
        self.function2edge_list = {}

    def load(self, binary_path, binary2label):
        self.name = binary_path.split('/')[-1][:-4] # remove _dir
        self.name = binary2label[0]
#        print(self.name)
# The four graph related files
        func_info_file = os.path.join(binary_path, "func_to_id_addr.csv")
        block_info_file = os.path.join(binary_path, "block_id_to_info.csv")
        block_addr_file = os.path.join(binary_path, "block_id_to_label.csv")
        cfg_file = os.path.join(binary_path, "cfg_edge_list.graph")
        fcg_file = os.path.join(binary_path, "fcg_edge_list.graph")
        block_feature_file = os.path.join(binary_path, "feature.csv")

# Step 2: load function call graph
        if os.path.exists(fcg_file):
            self.fcg_edge_list = self.load_edge_list(fcg_file)
#        print(len(self.fcg_edge_list))

# Step 3: load control flow graph
        if os.path.exists(cfg_file):
            self.cfg_edge_list = self.load_edge_list(cfg_file)
#        print(len(self.cfg_edge_list))

# Step 4: load basic block feature
        if os.path.exists(block_feature_file):
            self.block_feature = self.load_feature(block_feature_file)
#        print(len(self.block_feature))

# Step 5: load basic block info
        if os.path.exists(block_info_file):
            self.load_function2block(block_info_file, block_addr_file)
#        print(len(self.function2block))

# Step 6: update function2edge_list
#        self.update_function2edge_list()

# Step 6: load function information
        if os.path.exists(func_info_file):
            self.load_func_info(func_info_file)
#        print(self.n_functions)

# Step 7: label the binary
        self.label_binary(binary2label)

# Step Final: clean the class
        self.clean()

    def clean(self):
        self.cfg_edge_list = []
        self.block_feature = []
        self.block_addr = []
        self.function2block = {}
        self.function2edge_list = {}

    def label_binary(self, binary2label):
        
        for key, val in binary2label.items():
            if self.name not in val.strip():
                #('\n\n------------------------------',self.name, ' : ',binary2label.values())
                print("%s does not have label" %(self.name))
                return
            self.label = binary2label[0]
            #print('\n\n2------------------------------',self.label, ' : ',binary2label.values())


    def load_function2block(self, block_info_file, block_addr_file):

        with open(block_info_file, "r") as fp:
            is_head = True
            for line in csv.reader(fp):
                if is_head:
                    is_head = False
                    continue
#                print(line)
                func_id = int(line[-2])
                block_id = int(line[0])
                if func_id not in self.function2block:
                    self.function2block[func_id] = []
                self.function2block[func_id].append(block_id)

        with open(block_addr_file, "r") as fp:
            is_head = True
            for line in csv.reader(fp):
                if is_head:
                    is_head = False
                    continue
                self.block_addr.append(int(line[2]))

    def load_feature(self, feature_file):
        feature_list = []
        with open(feature_file, "r") as fp:
            is_head = True
            for line in csv.reader(fp):
                if is_head:
                    is_head = False
                    continue
                feature = [float(x) for x in line[1:]]
                feature_list.append(feature)
        return feature_list

    def load_func_info(self, func_info_file):
        with open(func_info_file, "r") as fp:
            is_head = True
            for line in csv.reader(fp):
                if is_head:
                    is_head = False
                    continue
                function = Function()
                function.name = line[1]
                if line[2].startswith("0x"):
                    function.addr = int(line[2][:-1], 0)

                func_id = int(line[0])
                function.n_blocks = len(self.function2block[func_id])
                block_start = self.function2block[func_id][0]

                block_end = block_start + function.n_blocks

                function.block_feature = self.block_feature[block_start: block_end]
                function.block_addr = self.block_addr[block_start: block_end]

# low efficient
                for edge in self.cfg_edge_list:
                    u, v = int(edge[0]), int(edge[1])
#                    if u < block_start or v < block_start:
#                        continue
                    if u >= block_start and u < block_end and v >= block_start and v < block_end:
                        function.cfg_edge_list.append([u - block_start, v - block_start])

                    if u > block_end and v > block_end:
                        break

                self.function_list.append(function)
        self.n_functions = len(self.function_list)


    def load_edge_list(self, fcg_file):
        edge_list = []
        with open(fcg_file, "r") as fp:
            is_head = True
            for line in csv.reader(fp, delimiter = " "):
                if is_head:
                    is_head = False
                    continue
                edge_list.append([int(line[0]), int(line[1])])
        return edge_list

def clean_file(output_file):
    fp = open(output_file, "w")
    fp.close()

def get_directories(input_path):
  
    subfolders = [ f.path for f in os.scandir(input_path) if f.is_dir() ]
    return subfolders

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

def dump_to_json(x, output_file):

    with open(output_file, "w") as fp:
        json.dump(x, fp)

def process_binary(binary_home, binary2label, output_file):
    binary = Binary()
    #print("binary2label: ",binary2label)
    binary.load(binary_home, binary2label)
    #print("binary.name: ",binary.name)
    merged_binary = BinaryFunction()

    merged_binary.merge(binary)

    x = json.dumps(merged_binary.__dict__)
    dump_to_json(x, output_file)
#    print(binary.__dict__, '\n')
#    for function in binary.function_list:
#        print(function.__dict__)
#        break
#    print(dir(merged_binary))
#    exit(0)



def main(input_path, binary_label_file, output_path):
    
    binary2label = {}
    #grndTruthLabels=set()
    
    #binary_label_file = os.path.join(input_path, "program_id_to_name.csv")
    file_label = input_path.split("/")[-1][:-4]
    binary2label[0] = file_label
    
    #- commented
    #with open(binary_label_file, "r") as fp:
    #    for line in csv.reader(fp):
            
    #        binary2label[line[0]] = file_label #line[1]
            #print("binary2label[line[0]] : ",binary2label)

    num = 0
    
    with open(os.path.join(input_path, "program_id_to_name.csv"), "r") as fp:
        for line in csv.reader(fp):
            firm_name = line[1]
            #print(firm_name)
            #cmp,ver,opt= getGroundTruth(firm_name)
            #print(cmp+"_"+ver+"_"+opt)
            #print('Firm Name: ',line[0], firm_name)
#            if int(line[0]) < 6000:
#            if line[1].startswith("6e56") or line[1].startswith("8a00"):
#                continue
#            if int(line[0]) % 3 != 2:
#                continue
#            if int(line[0]) > 6000:
#                break
#            with open(os.path.join(input_path, firm_name, "program_id_to_name.csv"), "r") as firm_fp:
#                for index in csv.reader(firm_fp):
            #program_name = index[1].rsplit('.', 1)[0] + '_dir'

            program_name = firm_name
            
            
            
            #print("file_label: ",file_label)
            
            feature_folder = os.path.join(os.path.join(input_path, firm_name), program_name)
            
            #- modified by
            feature_folder = os.path.join(os.path.join(input_path, firm_name[:-4]+"_dir"))
            
            #print('feature_folder: ',feature_folder)
            
            if os.path.exists(feature_folder):
                output_file = os.path.join(output_path, file_label + ".json")
                #clean_file(output_file)
                #print(output_file)
                if os.path.exists(output_file):
                    continue

                #print("Label ",binary2label)
                process_binary(feature_folder, binary2label, output_file)
                num += 1
                if num % 10 == 0:
                    print(num)
#                    else:
#                        print("feature_folder,", feature_folder)


if __name__ == "__main__":
    #input_path='/home/UNT/mi0214/vestige/binall_snns_post'
    #print(get_directories(input_path))
    if len(sys.argv) != 3:
        print("Usage: python build_malware_acfg.py <input_path>  <output_path>\n")
        exit(-1)
    
    if sys.argv[1].endswith('.csv'):
        with open(sys.argv[1],'r') as file:
            sub_dir= file.readlines()
        #print(sub_dir)
    else:
        sub_dir = get_directories(sys.argv[1])
    count = 1
    for sub_sub_dir in sub_dir:
        #print(sub_sub_dir.strip())
        sub_sub_dir = sub_sub_dir.strip()
        if sub_sub_dir.endswith("_dir"):
            print(sub_sub_dir)
            
            main(sub_sub_dir, sub_sub_dir+"/program_id_to_name.csv", sys.argv[2])
            if count>=len(sub_dir):
                exit(-1)
            count = count +1



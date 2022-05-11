#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Apr 27 11:46:52 2022

@author: mi0214
"""

import time
import csv
import sys
import random

class Instance:
    def init(self):
        self.index = -1
        self.label = ""
        self.partition = -1

def get_label_list(label_file):

    index = 0
    label_list = []
    with open(label_file, "r") as fp:
        for line in fp:
            label_list.append(line.strip())

    return label_list
        
def get_interested_label(interested_label_file):
    #interested_label_list = []
    interested_label_list = {}
    with open(interested_label_file, "r") as fp:
        for line in csv.reader(fp):
            #interested_label_list.append(line[1].strip())
            interested_label_list[int(line[0].strip())]=str(line[1].strip())
    return interested_label_list

def get_stats_train_split(all_label_list, interested_label_list):
    label_dict = {}
    
    #O-3 index represent OL
    # O = O0
    # 1 = O1
    # 2 = O2
    # 3 = O3
    # Keep the stats of how many number of testing, training, validation samples are used
    train_valid_test_split={"train":[0,0,0,0],"validation":[0,0,0,0],"testing":[0,0,0,0]}
    
    for i in range(len(all_label_list)):
        toolchain_label = int(all_label_list[i].split(',')[1])
        partition_label = int(all_label_list[i].split(',')[2])
        
# =============================================================================
        # get the lable of toolchain from the all lables file
        # get the toolchain name and check the last character which is our OL number
        # add +1 to corresponding split index of OL
        if partition_label==0:
             train_valid_test_split['train'][int(interested_label_list[toolchain_label][-1])]+=1
        elif partition_label==1:
             train_valid_test_split['validation'][int(interested_label_list[toolchain_label][-1])]+=1
        else:
            train_valid_test_split['testing'][int(interested_label_list[toolchain_label][-1])]+=1
# =============================================================================
    
    return train_valid_test_split
#def get_train_val_stats(all_labels,interested_labels):
#    for 

def main(all_label_file, interested_label_file, output_folder):

    all_label_list = get_label_list(all_label_file)
    interested_label_list = get_interested_label(interested_label_file)
    train_valid_test_split = get_stats_train_split(all_label_list, interested_label_list)

    #print("all_label_list: ",all_label_list)
    #print("interested_label_list: ",interested_label_list)
    #print("label_dict: ",label_dict)
    
    print(train_valid_test_split)
    print('train: ',sum(train_valid_test_split['train']))
    print('validation: ',sum(train_valid_test_split['validation']))
    print('testing: ',sum(train_valid_test_split['testing']))
    
    #split_label_dict(label_dict)

#    for label in label_dict:
#        print(label)
#        for instance in label_dict[label]:
#            print(instance.index, instance.label, instance.partition)

    #dump_to_file(label_dict, interested_label_list, output_folder)

#    split_and_dump(all_label_list, interested_label_list, output_folder)


if __name__ == "__main__":

    folder = '/home/UNT/mi0214/NestedGNN_compromised_host' \
    '/nested_gnn/script_binary/output_folder'
    
    interested_labels_list='/home/UNT/mi0214/NestedGNN_compromised_host' \
    '/nested_gnn/script_binary/output_folder/labels_list.csv'
    
    all_labels_list='/home/UNT/mi0214/NestedGNN_compromised_host' \
    '/nested_gnn/script_binary/output_folder/label_split_311.csv'
    
    main(all_labels_list, interested_labels_list, folder)



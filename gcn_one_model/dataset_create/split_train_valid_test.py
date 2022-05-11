import os
import pandas as pd
import pickle as pkl
import time
import csv
import sys
import random

class Instance:
    def init(self):
        self.index = -1
        self.name = ""
        self.label = ""
        self.partition = -1

def split_label_dict(label_dict,testing_binaries,training_binaries,software):
    
    for label in label_dict:
        label_list = label_dict[label]
        l = len(label_list)
        for i in range(l):
            for sw in software:
                for tr_bin in training_binaries:
                    if sw + "." + tr_bin in label_dict[label][i].name:
                        label_dict[label][i].partition = 0
                for ts_bin in testing_binaries:
                    if sw + "." + ts_bin in label_dict[label][i].name:
                        label_dict[label][i].partition = 2
    #print data            
    #for label in label_dict:
    #    for instance in label_dict[label]:
    #        print(instance.index, instance.label,instance.name, instance.partition)
# =============================================================================
#     for label in label_dict:
#         label_list = label_dict[label]
#         
#         l = len(label_list)
#         
#         #print(label, ' ', l)
#         
#         index_list = []
#         for i in range(l):
#             index_list.append(i)
#         #random.shuffle(index_list)
# # train: validation: test = 2: 2: 6
#         step_1 = int(l * 0.6)
#         step_2 = int(l * 0.8)
#         train = set(index_list[: step_1])
#         valid = set(index_list[step_1: step_2])
#         test = set(index_list[step_2: ])
# 
#         for i in range(l):
#             for util in util_list:
#                 print(util.strip())
#                 if util.strip() not in testing_binaries:
#                     #print('Testing')
#                     label_dict[label][i].partition = 1
#                 else:
#                     label_dict[label][i].partition = 0
# =============================================================================

def split_and_dump(label_list, output_folder):

    l = len(label_list)

    index_list = []
    for i in range(l):
        index_list.append(i)
    random.shuffle(index_list)
# train: validation: test = 2: 2: 6
    step_1 = int(l * 0.2)
    step_2 = int(l * 0.4)
    train = set(index_list[: step_1])
    valid = set(index_list[step_1: step_2])
    test = set(index_list[step_2: ])

    with open(os.path.join(output_folder, "label_split_311.csv"), "w") as fp:
        for i in range(l):
            line = label_list[i] + ','
            if i in train:
                line += '0' # train
            elif i in valid:
                line += '1' # valid
            else:
                line += '2' # test
            fp.write(line + '\n')


def get_label_list(label_file):

    index = 0
    label_list = []
    with open(label_file, "r") as fp:
        for line in fp:
            label_list.append(line.strip())

    return label_list

def get_interested_label(interested_label_file):
    interested_label_list = []
    with open(interested_label_file, "r") as fp:
        for line in csv.reader(fp):
            interested_label_list.append(line[1].strip())
    return interested_label_list

def get_label_dict(all_label_list, interested_label_list):
    label_dict = {}
    #print("function: get_label_dict")
    #print("all_label_list: ",all_label_list)
    #print("interested_label_list: ",interested_label_list)
    for i in range(len(all_label_list)):
        label = all_label_list[i].split(',')[1]
        name = all_label_list[i].split(',')[2]
        #ind = interested_label_list.index(all_label_list[i].split(',')[1])
        #print('INDEX:  ',ind, " : Label: ",all_label_list[i].split(',')[1])
        if label in interested_label_list:
            if label not in label_dict:
                label_dict[label] = []
            instance = Instance()
            instance.index = i
            instance.name = name
            instance.label = label
            #print('label: ',label)
            label_dict[label].append(instance)
    return label_dict
#    for key in label_dict:
#        print(key, len(label_dict[key]))

def dump_to_file(label_dict, interested_label_list, output_folder):
    label2index = {}
    index = 0
    for label in interested_label_list:
        label2index[label] = index
        index += 1
    #print("label2index: ",label2index)

    output_dict = {}
    output_file = os.path.join(output_folder, "label_split_311.csv")
    for label in label_dict:
        for instance in label_dict[label]:
            #print(instance.index, instance.label,instance.name, instance.partition)
            output = ','.join([str(instance.index), str(label2index[instance.label]), str(instance.partition)]) + '\n'
            output_dict[instance.index] = output
            index += 1

    with open(output_file, "w") as fp:
        for one in sorted(output_dict.keys()):
            #print("output_dict[one]: ",output_dict[one])
            fp.write(output_dict[one])

def get_utility_list(files,software):
    util_list = []
    for fName in files:
        fName = fName.split(',')[2]
        for sw in software:
            #fName = fName.split('/')[-1]
            if sw in fName:
                util = fName[len(sw):].split('.')
                #print('util: ',util[1])
               
                if util[1] not in util_list:
                    util_list.append(util[1])
                    #print(util_list)
    #print(util_list)
    return util_list


def main(all_label_file, interested_label_file, output_folder):
    
    testing_binaries = ['bashversion','mksyntax','egrep','diff3']
    software=['grep-2.16', 'diffutils-3.3' ,'wget-1.15' ,'bash-4.3', 'tar-1.27.1']
    
    all_label_list = get_label_list(all_label_file)
    interested_label_list = get_interested_label(interested_label_file)
    label_dict = get_label_dict(all_label_list, interested_label_list)
    
    util_list =  get_utility_list(all_label_list,software)
    
    for t_bin in testing_binaries:
        util_list.remove(t_bin)
    
    #print("all_label_list: ",all_label_list)
    #print("interested_label_list: ",interested_label_list)
    #print("label_dict: ",label_dict)
    
    #split_label_dict(label_dict,testing_binaries,util_list,software)
    
    training_binaries = util_list
    
    split_label_dict(label_dict,testing_binaries,training_binaries,software)
#    for label in label_dict:
#        print(label)
#        for instance in label_dict[label]:
#            print(instance.index, instance.label, instance.partition)

    dump_to_file(label_dict, interested_label_list, output_folder)
    #print("label_dict: ",(label_dict))

#    split_and_dump(all_label_list, interested_label_list, output_folder)


if __name__ == "__main__":

    if len(sys.argv) != 4:
        print("Usage: python split_train_valid_test.py <all_label_file> <intrested_label_file> <output_folder>")
        #print("Example:\npython split_train_valid_test.py /home/yuedeji/data/cyber_data/malware_sei/label.txt /home/yuedeji/data/cyber_data/malware_sei/label_split.csv")
        print("Example:\npython split_train_valid_test.py /home/yuedeji/data/cyber_data/malware_sei/malware_nested/label_all.txt /home/yuedeji/data/cyber_data/malware_sei/malware_nested/label_limit_100.csv /home/yuedeji/data/cyber_data/malware_sei/malware_nested")
        exit(-1)
    main(sys.argv[1], sys.argv[2], sys.argv[3])


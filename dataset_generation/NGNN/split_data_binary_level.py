import shutil, os
import random
import math
import sys
from os import walk
from os import listdir
from os.path import isfile, join


import shutil, os, random
import math
from os import walk
from os import listdir
from os.path import isfile, join


def get_directories(input_path):
  
    subfolders = [ f.path for f in os.scandir(input_path) if f.is_dir()]
    return subfolders

def get_sw_list(files):
    sw_list = []
    for fName in files:
        sw_name = fName.split('.')
        if sw_name[0] not in sw_list:
            sw_list.append(sw_name[0])
            #print(fName)
    return sw_list

def get_utility_list(files,software):
    util_list = []
    for fName in files:
        for sw in software:
            fName = fName.split('/')[-1]
            if sw in fName:
                util = fName[len(sw):].split('.')
                #print('util: ',util[1])
               
                if util[1] not in util_list:
                    util_list.append(util[1])
                    #print(util_list)
    #print(util_list)
    return util_list

def getDataset(sub_dir,software,utility,opt_levels):
    dataset = [];
    for f in sub_dir:
        for ol_ind in range(len(opt_levels)): 
            for sw in software:
                for util in utility:
                    if (sw+"."+util) in f and f.endswith(opt_levels[ol_ind]+'_dir'):
                        if f not in dataset:
                            dataset.append(f)
    return dataset

def createPathIfNotExists(path):
    if not os.path.exists(path):
    #print('Path Not Exists')
        os.makedirs(path)
        print("The new directory is created!",path)



if len(sys.argv)!=2:
    print("python split_data_binary_level.py <arguments for Optimization Level(example O0:O1:O2:O3)>")
    exit(-1)

opt_levels = sys.argv[1].split(":")
print(opt_levels)

testing_binaries = ['bashversion','mksyntax','egrep','diff3']
 
software=['grep-2.16', 'diffutils-3.3' ,'wget-1.15' ,'bash-4.3', 'tar-1.27.1']

src='/home/UNT/mi0214/vestige/binall_snns_post'


out_file= os.getcwd()+'/samples_folder.csv'

master_dataset=[]
train_dataset = []
test_dataset = []


sub_dir = get_directories(src)


# =============================================================================
# #sw_list = get_sw_list(onlyfiles)
util_list =  get_utility_list(sub_dir,software)

#training_binaries = res = [util for util in util_list if util not in testing_binaries]

print("training_binaries: ",util_list)

master_dataset = getDataset(sorted(sub_dir),software,util_list,opt_levels)

with open(out_file,'w') as file:
    for item in master_dataset:
        file.write(item+"\n")
    file.close()

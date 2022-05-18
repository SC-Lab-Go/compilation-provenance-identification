import shutil, os
import random
import math
from os import walk
from os import listdir
from os.path import isfile, join


import shutil, os, random
import math
from os import walk
from os import listdir
from os.path import isfile, join

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
            if sw in fName:
                util = fName[len(sw):].split('.')
                #print('util: ',util)
               
                if util[1] not in util_list:
                    util_list.append(util[1])
                    #print(util_list)
    #print(util_list)
    return util_list

def getDataset(files,software,utility):
    dataset = [];
    for f in onlyfiles:
        for sw in software:
            for util in utility:
                if (sw+"."+util) in f:
                    print(f)
                    dataset.append(f)
    return dataset

def createPathIfNotExists(path):
    if not os.path.exists(path):
    #print('Path Not Exists')
        os.makedirs(path)
        print("The new directory is created!",path)

def getFileLines():
    file1 = open('testing_wo_coreutils.txt', 'r')
    Lines = file1.readlines()
    return Lines
def copyFiles(src_path,des_path, master_dataset, train_dataset,test_dataset):

    
    test_folder=des_path+'binary_level/test'
    train_folder=des_path+'binary_level/train'
    createPathIfNotExists(test_folder)
    createPathIfNotExists(train_folder)
    for f in master_dataset:
        direct= (src_path+f)#.replace("/","\\") #only for windows
    #print(direct)
        path = os.path.join(direct)
        if f in test_dataset:
            shutil.copy(path, test_folder)
        elif f in train_dataset:
            shutil.copy(path, train_folder)
        
#src='L:/VIS/'
#test_folder=src+'test'
#train_folder=src+'train'
#k=1

software=['grep-2.16', 'diffutils-3.3' ,'wget-1.15' ,'bash-4.3', 'tar-1.27.1']
src = '/home/UNT/mi0214/binary_6552/'
des= '/home/UNT/mi0214/origin_ins/vestige_baseline_ds/'

master_dataset=[]
train_dataset = []
test_dataset = []

#Lines = getFileLines()
#for file in Lines:
#    onlyfiles.append(file[:-1].split('/')[-1])
onlyfiles = []
onlyfiles = [f for f in listdir(src) if isfile(join(src, f))]



#sw_list = get_sw_list(onlyfiles)
util_list =  get_utility_list(onlyfiles,software)

random.shuffle(util_list)
print('util_list: ',util_list)
print('util_list len: ',len(util_list))



num_of_train_utility = math.ceil(len(util_list)*0.7)
num_of_test_utility = len(util_list) - num_of_train_utility

train_utility_list = util_list[:num_of_train_utility]
test_utility_list = util_list[num_of_train_utility:]

print(train_utility_list)
print(test_utility_list)

train_dataset = getDataset(sorted(onlyfiles),software,train_utility_list)
test_dataset = getDataset(sorted(onlyfiles),software,test_utility_list)



master_dataset = train_dataset + test_dataset


    
copyFiles(src,des, master_dataset, train_dataset,test_dataset)




#files = ['file1.txt', 'file2.txt', 'file3.txt', 'file4.txt']

        


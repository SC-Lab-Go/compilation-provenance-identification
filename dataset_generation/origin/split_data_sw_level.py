import shutil, os
import math
from os import walk
from os import listdir
from os.path import isfile, join
src = '/home/UNT/mi0214/binary_6552/'
des= '/home/UNT/mi0214/origin_ins/vestige_baseline_ds/'

test_folder=des+'sw_level/test'
train_folder=des+'sw_level/train'
k=1


#manual selection is done to do software level testing

train_software=['grep-2.16' ,'wget-1.15' ,'bash-4.3', 'tar-1.27.1']
test_software = ['diffutils-3.3']
#test_software = ['binutils-2.30']

utility=['egrep', 'fgrep','grep','cat' , 'cmp', 'diff' , 'diff3' , 'sdiff', 'wget','bash', 'bashversion', 'mkutilbins', 'mksyntax','mksignames','tar']

master_dataset=[]
train_dataset = []
test_dataset = []
onlyfiles = [f for f in listdir(src) if isfile(join(src, f))]


def createPathIfNotExists(path):
    if not os.path.exists(path):
    #print('Path Not Exists')
        os.makedirs(path)
        print("The new directory is created!",path)

createPathIfNotExists(test_folder)
createPathIfNotExists(train_folder)

for f in onlyfiles:
    for sw in train_software:
        if sw in f:
                train_dataset.append(f)
    for testing_sw in test_software:
        if testing_sw in f:
                test_dataset.append(f)

num_of_test_files = math.ceil(len(master_dataset)*0.7)
num_of_train_files = len(master_dataset) - num_of_test_files


master_dataset = test_dataset + train_dataset

#test_dataset = master_dataset[:num_of_test_files]
#train_dataset = master_dataset[num_of_test_files:]
print('master_dataset: ',len(master_dataset))
print('test_dataset: ',len(test_dataset))
print('train_dataset: ',len(train_dataset) , ' ' , num_of_train_files)
#files = ['file1.txt', 'file2.txt', 'file3.txt', 'file4.txt']
#print('test_dataset: ',test_dataset)
#print('_________________________________')
#print('train_dataset: ',train_dataset)

#print('onlyfiles: ',len(onlyfiles))

for f in master_dataset:
    direct= (src+f)#.replace("/","\\") #only for windows
    print(direct)
    path = os.path.join(direct)
    #print(path)
    if f in test_dataset:
        shutil.copy(path, test_folder)
    elif f in train_dataset:
        shutil.copy(path, train_folder)

import os
import sys
import commands
import csv
import random

def get_file_set(list_file):

    file_set = set()
    with open(list_file, "r") as fp:
        for line in fp:
            file_set.add(line.rsplit("/", 1)[-1].strip())

    return file_set

def get_feature_set(feature_file):

    feature_set = set()

    with open(feature_file, "r") as fp:
        for line in fp:
            index = line.split()[0].strip()
            feature_set.add(index)

    return feature_set

def get_specific_file_list(data_folder, raw_file_set):
    '''Training or Testing file list'''
    cp_list = ["GCC_4.6.4", "GCC_4.8.4", "GCC_5", "Clang 3.3", "Clang 3.5", "Clang 5.0"]#,"LLVM_3.3", "LLVM_3.5", "LLVM_5.0"]
    op_list = ["O0", "O1", "O2", "O3"]

    specific_file_list = []
    raw_file_list = os.listdir(data_folder)
    for file_one in raw_file_list:
        if not file_one.endswith(".data"):
            continue
        for cp in cp_list:
            for op in op_list:
                provenance = cp + "_" + op
                if provenance in file_one:
                    file_name = file_one.split(provenance)[-1][1:-5]
                    if file_name in raw_file_set:
                        specific_file_list.append(file_one)

    return specific_file_list

def get_file_feature_list(file_path, feature_set, index_map):

    feature_list = []
    with open(file_path, "r") as fp:
        for line in fp:
            line_list = line.split()
            new_line = index_map[line_list[0]]

            for pair in line_list[1:]:
                if pair.split(':')[0] in feature_set:
                    new_line = new_line + " " + pair
            feature_list.append(new_line)

    return feature_list

def get_index_map(index_file):
    index_dict = {}
    with open(index_file, "r") as fp:
        for line in fp:
            index_list = line.split(" ")[0].split(",")
            index_dict[index_list[-1]] = line.split(" ")[0]

    return index_dict

def get_filtered_feature_list(raw_file_set, feature_set, data_folder, index_map, output_file_name):

    specific_file_list = get_specific_file_list(data_folder, raw_file_set)
    print "# of specific files", len(specific_file_list)

    new_feature_list = []

    output_file = os.path.join(data_folder, output_file_name)

    for file_name in specific_file_list:
        file_path = os.path.join(data_folder, file_name)
        print file_path
        new_feature_list = new_feature_list +  get_file_feature_list(file_path, feature_set, index_map)

    random.shuffle(new_feature_list)

    with open(output_file, "w") as fp:
        for line in new_feature_list:
            fp.write(line + "\n")


def main(train_file, test_file, data_folder, selected_feature_file, index_file):

    train_file_set = get_file_set(train_file)
    test_file_set = get_file_set(test_file)

    print "# of training files,", len(train_file_set)
    print "# of testing files,", len(test_file_set)

    feature_set = get_feature_set(selected_feature_file)
#    print feature_set
    print "# of selected features,", len(feature_set)

    index_map = get_index_map(index_file)
    print index_map
    print "# of indexs,", len(index_map)

    get_filtered_feature_list(train_file_set, feature_set, data_folder, index_map, "train_hierarchical_random.csv")

    get_filtered_feature_list(test_file_set, feature_set, data_folder, index_map, "test_hierarchical_random.csv")


if __name__ == "__main__":

    if len(sys.argv) != 6:
        print "python convert_to_hierarchical_format.py <train_file_list> <test_file_list> <data_folder> <selected_feature_file> <index_file>"
        exit(-1)

    main(sys.argv[1], sys.argv[2], sys.argv[3], sys.argv[4], sys.argv[5])

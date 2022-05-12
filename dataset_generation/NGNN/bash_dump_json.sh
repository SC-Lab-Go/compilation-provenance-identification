

#python build_binary_acfg.py /home/yuedeji/data/cyber_data/malware_sei/malware_processed /home/yuedeji/data/cyber_data/malware_sei/meta_data/binary_label.csv /home/yuedeji/data/cyber_data/malware_sei/malware_json

home=/home/UNT/mi0214/vestige/binall_snns_post
home=/home/UNT/mi0214/dataset_creation/nested_gnn/samples_folder.csv

output_folder=/home/UNT/mi0214/feature_nestgnn/json_folder


output_folder=/home/UNT/mi0214/feature_nestgnn/binary_baseline_json


python modify_build_binary_acfg.py $home $output_folder

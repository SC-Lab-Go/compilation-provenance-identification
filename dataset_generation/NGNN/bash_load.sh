

output_folder=/home/UNT/mi0214/NestedGNN_compromised_host/nested_gnn/script_binary/output_folder

#python generate_nested_graph.py /home/yuedeji/data/cyber_data/malware_sei/malware_json /home/yuedeji/data/cyber_data/malware_sei/malware_nested
#echo 'E'
input_folder=/home/UNT/mi0214/feature_nestgnn/json_folder
output_folder=/home/UNT/mi0214/NestedGNN_compromised_host/nested_gnn/script_binary/output_folder

#baseline data folders
input_folder=/home/UNT/mi0214/feature_nestgnn/binary_baseline_json
output_folder=/home/UNT/mi0214/NestedGNN_compromised_host/nested_gnn/script_binary/baseline_graph


python modify_generate_nested_graph.py $input_folder $output_folder 

#python3 -W ignore train.py --dataset /home/yuedeji/data/cyber_data/lanl_2015/user_graph/ --gpu 1
#python3 -W ignore train.py --dataset /home/yuedeji/data/cyber_data/lanl_2015/user_graph/


data=/home/UNT/mi0214/NestedGNN_compromised_host/nested_gnn/script_binary/baseline_graph

python -W ignore train.py --dataset $data --gpu -1 

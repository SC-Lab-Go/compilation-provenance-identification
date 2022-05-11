import os

for num_process in [4, 8, 16, 32, 64]:
#num_process = 64
#gpu = 3
    for accumulate in ['mean', 'sum']:
        for i in range(10):
            cmd_sed_1 = "sed -i '/inner_graph_feats =/c\    inner_graph_feats = %s' train.py" %(num_process)
            cmd_sed_2 = "sed -i '/h_graph = torch/c\            h_graph = torch.%s(h_inner, dim = 0)' nested_gcn.py" %(accumulate)
            result_file = "result_%s_%s/nestedgnn_%s.csv" %(num_process, accumulate, i)
            #cmd = "python3 -W ignore train.py --dataset /home/yuedeji/data/cyber_data/lanl_2015/sampled_graph/ --gpu %s > %s" %(gpu, result_file)
            cmd = "python3 -W ignore train.py --dataset /home/yuedeji/data/cyber_data/lanl_2015/user_graph/ > %s" %(result_file)
            os.system(cmd_sed_1)
            os.system(cmd_sed_2)
            print("num_process", num_process, "accumulate", accumulate, "i", i)
            os.system(cmd)


model=/home/UNT/mi0214/origin_ins/models/model_binary_level/
output_file=/home/UNT/mi0214/origin_ins/result_binary.csv
testing_list=/home/UNT/mi0214/origin_ins/vestige_baseline_ds/origin_binary/test.txt 
#testing_list=/home/UNT/mi0214/origin_ins/vesitge_dataset/dataset/coreutils.txt
python2 testing_origin_write_csv.py $testing_list $output_file $model

python2 get_test_accu.py $output_file

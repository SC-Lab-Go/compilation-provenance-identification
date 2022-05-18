origin_home=/home/UNT/mi0214/origin_ins
test_file=$origin_home/vestige_dataset/dataset/test_data_wo_coreutils.txt
training_file=$origin_home/vestige_dataset/dataset/coreutils.txt

global_features_trained_data=/home/UNT/mi0214/origin_ins/vestige_global_feature
selected_features_file=$origin_home/vestige_ds_model/features.txt

echo $global_features_trained_data
python2 convert_to_hierarchical_format.py $training_file $test_file $global_features_trained_data $selected_features_file toolchain-index_hierarchical.txt

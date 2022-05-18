origin_home=/home/UNT/mi0214/origin_ins
#unseen_binarylist=$origin_home/vestige_dataset/dataset/test_data_wo_coreutils.txt
unseen_binarylist=/home/UNT/mi0214/origin_ins/vestige_baseline_ds/origin_binary/test.txt
working_dir=/home/UNT/mi0214/work_dir/ 
model_dir=$origin_home/models/model_binary/

python2 origin_alter_get_accuracy.py --unseenbinlist $unseen_binarylist --workingdir $working_dir --installdir $origin_home --modeldir $model_dir

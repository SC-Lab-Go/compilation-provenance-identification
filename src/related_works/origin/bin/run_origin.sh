origin_home=/home/UNT/mi0214/origin_ins
unseen_binary=/home/UNT/mi0214/origin_ins/vestige_baseline_ds/origin_binary/test/CLANG/3.5/O3/diffutils-3.3.diff3.clang-3.5.O3
working_dir=/home/UNT/mi0214/work_dir/ 
model_dir=$origin_home/models/model_sw_level
model_dir=/home/UNT/mi0214/origin_ins/bin/data
python2 _Origin.py --binpath $unseen_binary --workingdir $working_dir --installdir $origin_home --modeldir $model_dir

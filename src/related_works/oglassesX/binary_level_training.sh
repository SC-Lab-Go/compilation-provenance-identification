epoch=50
batch=100
block_length=64
limit_size=25000
k=1

#binary level testing and traing dataset
training_ds=/home/UNT/mi0214/oglassesX_installed/vestige_baseline_ds/oglasses_binary_level/training/
testing_ds=/home/UNT/mi0214/oglassesX_installed/vestige_baseline_ds/oglasses_binary_level/testing/
model=/home/UNT/mi0214/oglassesX_installed/modified_oglassesX/models/binary_level/binary_vestige_baseline_model


#training phase
python3 modify_o-glassesX.py -d $training_ds -om $model -s $limit_size -e $epoch -b $batch -l $block_length

#testing phase
#python3 modify_o-glassesX.py -d $testing_ds -im $model -s $limit_size -e $epoch -b $batch -l $block_length -k $k

#python3 o-glassesX.py -d $testing_ds -im $model -s $limit_size -e $epoch -b $batch -l $block_length
#file=/home/UNT/mi0214/oglassesX_installed/vestige_baseline_ds/oglasses_sw_level/testing/CLANG3.3_32_O0/diffutils-3.3.cmp.clang-3.3.O0.bin

#get accuracy
#python3 get_accuracy.py -im $model -i $file

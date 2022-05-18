##this script will convert Vestige 6552 binaries files into the required format of the origin.

dataset_type=train
level=binary_level
home=/home/UNT/mi0214/origin_ins/vestige_baseline_ds/
src=/home/UNT/mi0214/origin_ins/vestige_baseline_ds/$level/$dataset_type
des=/home/UNT/mi0214/origin_ins/vestige_baseline_ds/origin_binary/$dataset_type

GCC=("4.6.4" "4.8.4" "5")
OL=("O0" "O1" "O2" "O3")
CLANG=("3.3" "3.5" "5.0")


for gcc in "${GCC[@]}"
do
for ol in "${OL[@]}"
do
dest=$des/GCC/$gcc/$ol
#echo $dest
mkdir -p $dest
cp $src/*gcc-$gcc.$ol $dest

done
done




for clng in "${CLANG[@]}"
do
for ol in "${OL[@]}"
do
dest=$des/CLANG/$clng/$ol
#echo $dest
mkdir -p $dest
cp $src/*clang-$clng.$ol $dest

done
done


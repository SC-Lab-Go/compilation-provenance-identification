##this script will convert Vestige 6552 binaries files into the required format of this technique. Later on making the tree in this format apply radare2 instructions to convert this into the input


home=/home/UNT/mi0214/oglassesX_installed
#training_sw_name=("coreutils-8.21" "coreutils-8.29" "binutils-2.30" "binutils-2.25")

#testing_sw_name=("openssl-1.0.1u" "openssl-1.0.1f" "grep-2.16" "postgresql" "snns" "diffutils-3.3" "wget-1.15" "bash-4.3" "tar-1.27.1")
testing_sw_name=("diffutils-3.3")
training_sw_name=("grep-2.16" "wget-1.15" "bash-4.3" "tar-1.27.1")

GCC=("4.6.4" "4.8.4" "5")
OL=("O0" "O1" "O2" "O3")
CLANG=("3.3" "3.5" "5.0")
#OL=("O0" "O1" "O2" "O3")
OL=("O0" "O1" "O2" "O3")
arc=32
hyphen=_
for sw in "${training_sw_name[@]}"
do
for gcc in "${GCC[@]}"
do
for ol in "${OL[@]}"
do
dest=$home/vestige_baseline_ds/training/GCC$gcc$hyphen$arc$hyphen$ol
#echo $dest
mkdir -p $dest
src=$home/vesitge_bin_dataset_creation/
cp $src/$sw*gcc-$gcc.$ol.bin $dest
#pr=$home/mk_dataset/binary_6552/*gcc-$gcc.$ol
#echo $pr
done
done
done


for sw in "${training_sw_name[@]}"
do
for clng in "${CLANG[@]}"
do
for ol in "${OL[@]}"
do
dest=$home/vestige_baseline_ds/training/CLANG$clng$hyphen$arc$hyphen$ol
#echo $dest
mkdir -p $dest
src=$home/vesitge_bin_dataset_creation/
cp $src/$sw*clang-$clng.$ol.bin $dest
#pr=$home/mk_dataset/binary_6552/*gcc-$gcc.$ol
#echo $pr
#dest=$home/mk_dataset/$sw/Clang$gcc/$ol
#ls $dest
#mkdir -p $dest
#src=$home/binary_6552
#cp $src/$sw*.clang-$gcc.$ol $dest
done
done
done


#------------------------------------------------------------------------
# testing dataset

for sw in "${testing_sw_name[@]}"
do
for gcc in "${GCC[@]}"
do
for ol in "${OL[@]}"
do
dest=$home/vestige_baseline_ds/testing/GCC$gcc$hyphen$arc$hyphen$ol
#echo $dest
mkdir -p $dest
src=$home/vesitge_bin_dataset_creation/
cp $src/$sw*gcc-$gcc.$ol.bin $dest
#pr=$home/mk_dataset/binary_6552/*gcc-$gcc.$ol
#echo $pr
done
done
done


for sw in "${testing_sw_name[@]}"
do
for clng in "${CLANG[@]}"
do
for ol in "${OL[@]}"
do
dest=$home/vestige_baseline_ds/testing/CLANG$clng$hyphen$arc$hyphen$ol
#echo $dest
mkdir -p $dest
src=$home/vesitge_bin_dataset_creation/
cp $src/$sw*clang-$clng.$ol.bin $dest
#pr=$home/mk_dataset/binary_6552/*gcc-$gcc.$ol
#echo $pr
#dest=$home/mk_dataset/$sw/Clang$gcc/$ol
#ls $dest
#mkdir -p $dest
#src=$home/binary_6552
#cp $src/$sw*.clang-$gcc.$ol $dest
done
done
done



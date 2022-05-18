home_origin=/home/UNT/mi0214/origin_ins

training_file_list=/home/UNT/mi0214/origin_ins/vestige_baseline_ds/origin_sw/train.txt
#training_file_list=/home/UNT/mi0214/origin_ins/vesitge_dataset/dataset/coreutils.txt

crfsuit=$home_origin/bin/crfsuite
extract_bin_feature=$home_origin/bin/extractFeat
extract_features=$home_origin/feature_extracted_vestige_dataset  #path where features of the training dataset will be stored
global_feature_index=$home_origin/vestige_global_feature

keep_feature=2000 #$1 #keep first argument as number of features

type=sw_level
model_out_dir=$home_origin/models/model_$type

mkdir -p $model_out_dir
mkdir -p $global_feature_index
#step 1: Generating Featrues from the training dataset

python2 FeatGen.py --filelist $training_file_list --idiom 1:2:3 --graphlet 1:2:3  --path_to_extract_bin $extract_bin_feature --outputdir $extract_features

#echo "Feature Generation Part Done: Next in Progress"

#generated features will be used for global feature descriptor

#step 2: generating global feature index, use path of outputdir of FeatGen.py file as input 
python2 GenDataFiles.py --filelist $training_file_list --idiom 1:2:3 --graphlet 1:2:3 --featdir $extract_features --outputdir $global_feature_index

echo "Global Feature Generation Part Done: Next in Progress"


#Step 3: Feature Selection
python2 FS.py --filelist $training_file_list --datadir $global_feature_index --keep $keep_feature  --output $global_feature_index/fs.txt

echo "Feature Selection Part Done: Training Model in Progress"

#step 4: train model from the selected features

python2 TrainModel.py --filelist $training_file_list  --datadir $global_feature_index --featurelist $global_feature_index/fs.txt --path_to_crfsuite $crfsuit

#copy files to new model dir feat_list.txt, toolchain-index.txt (generated in global feature index folder) and model.dat
mv $home_origin/bin/model.dat $model_out_dir/model.dat
mv $global_feature_index/fs.txt $model_out_dir/features.txt
mv $global_feature_index/toolchain-index.txt $model_out_dir/toolchain-index.txt

echo "model copied to: $model_out_dir"
rm lbfgs_checkpoint.data
rm tmp.crf.train.txt

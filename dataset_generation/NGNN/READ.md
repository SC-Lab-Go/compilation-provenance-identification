
Step1: run "gen_data_binary_level.sh" this will generate a sample list file when we are using baseline dataset and specify Opt levels.

Step2: run "bash_dump_json.sh", to generate ACFG, make sure the argument, I provided csv file, which is stored in step1.

Step3: run "bash_load.sh" this will create nestedgraph data for the json files generated in step 2.

Step4: run split_train_test.sh to convert generate a split file.

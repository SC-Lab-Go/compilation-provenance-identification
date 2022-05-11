
Step1: run "split_data_binary_level.py" this will generate a sample list file if we are using baseline dataset.

Step2: run "bash_dump_json.sh", to generate ACFG, make sure the argument, I provided csv file, which i stored in step1.

Step3: run "bash_load.sh" this will create nestedgraph data for the json files generated in step 2.

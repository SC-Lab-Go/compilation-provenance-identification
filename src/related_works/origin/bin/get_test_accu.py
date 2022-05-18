import os
import sys
import commands
import csv
compilerList = ["GCC", "ICC", "CLANG", "LLVM", "PGI"]
def get_match(origin, predict):

#    print origin, predict
    if origin[0].strip() == predict[0].strip() and origin[1].strip() == predict[1].strip():
        return 1, 1, 1

    elif origin[1].strip() == predict[1].strip():
        return 0, 1, 0

    elif origin[0].strip() == predict[0].strip():
        return 1, 0, 0

    return 0, 0, 0
    
def get_match_provenance(ground_truth, predicted):

    print "In get_match_provenance: ",ground_truth, predicted
    a,b,c,com= 0,0,0,0
    gt_labels = ground_truth.split("-")
    isCombined = False
    for predict in predicted:
    	pt_label = predict.strip().split("-")
    	#print gt_labels
    	#print pt_label
    	if ground_truth.lower().strip() == predict.lower().strip():
    		#return 1,1,1
    		com+=1
    		a+=1
    		b+=1
    		c+=1
    		 #we mathced all values
    	elif gt_labels[0] == pt_label[0] and gt_labels[1].strip() == pt_label[1].strip() and gt_labels[2].strip() != pt_label[2].strip():
    		#return 1,0,0
    		com+=0
    		a+=1
    		b+=1
    		c+=0
    	elif gt_labels[0] == pt_label[0] and gt_labels[1].strip() != pt_label[1].strip() and gt_labels[2].strip() == pt_label[2].strip():
    		#return 0,1,0
    		com+=0
    		a+=1
    		b+=0
    		c+=1
    	elif gt_labels[0] == pt_label[0] and gt_labels[1].strip() != pt_label[1].strip() and gt_labels[2].strip() != pt_label[2].strip():
    		#return 0,1,0
    		com+=0
    		a+=1
    		b+=0
    		c+=0
    	
    	
    	#elif 
    	
    		
    #if origin[0].strip() == predict[0].strip() and origin[1].strip() == predict[1].strip():
     #   return 1, 1, 1

    #elif origin[1].strip() == predict[1].strip():
     #   return 0, 1, 0

    #elif origin[0].strip() == predict[0].strip():
     #   return 1, 0, 0

    return com,a,b,c
    

def getGroundTruth(binfile_name):
	comp_name = ""
	version = ""
	opt_lvl = ""
	for comp in compilerList:
		if binfile_name.find(comp.lower()) != -1:
			comp_name = comp
			sub = binfile_name.find(comp.lower())
			rem_sub_string = binfile_name[sub:len(binfile_name)]
			_,ver_opt = rem_sub_string.split("-")
			version = ver_opt[0:len(ver_opt)-3]
			opt_lvl = ver_opt[len(ver_opt)-2:len(ver_opt)]
			#print comp_name+version+opt_lvl
			break
	return (comp_name,version,opt_lvl)
	
	
def get_test_accuracy(input_file):

    total = 0
    compiler = 0
    optimization = 0
    combined = 0
    version = 0
    total = 0
    predicted_total = 0
    with open(input_file, "r") as csv_file:
    	
        for line in csv.reader(csv_file):
        	
        	#print(line)
        	#spli_line = line.split(",") #first column is binary name, other column are predicted labels
        	bin_path = line[0]
        	bin_name = bin_path.split("/")[-1]
        	predicted = line[1:]
        	
        	total += 1
        	predicted_total += len(predicted)
        	
        	gt_bin_comp, gt_bin_version,gt_bin_olvl = getGroundTruth(bin_name)
        	
        	GT_Label = gt_bin_comp+ "-"+gt_bin_version+"-"+gt_bin_olvl
        	#print gt_bin_comp+ "-"+gt_bin_version+"-"+gt_bin_olvl
        	
        	#print "In main: ",GT_Label + " : "+str(predicted)
        	
        	com,a,b,c = get_match_provenance(GT_Label,predicted)
        	#compiler += a
        	#optimization += b
        	#combined += c
        	combined += com
        	compiler += a
        	version += b
        	optimization += c
        	print com,a,b,c
    
    print "Compiler,", compiler * 1.0 / predicted_total
    print "Optimization,", optimization * 1.0 / predicted_total
    print "Version,", version * 1.0 / predicted_total
    print "Combined,", combined * 1.0 / total
    print compiler,version, optimization, combined, total    

def get_test_accu(input_file):

    total = 0
    compiler = 0
    optimization = 0
    combined = 0
    with open(input_file, "r") as csv_file:

        for line in csv.reader(csv_file):
            #temp_file =  line
            if len(line) > 2 and line[0].startswith("Address"):
                print "line[0]: "+line[0]
                origin_list = line[0].split("_")
                origin = [line[1], line[-1]]
                
                total += 1
                if len(line) == 3:
                    print "LINE: "+str(origin)
                    predict = line[2].split("-")[1:]
                    
                    print "predict: "+str(predict)
                    
                    a, b, c = get_match(origin, predict)
                    compiler += a
                    optimization += b
                    combined += c

                # multiple precisions
                else:
                    predict_list = []
                    for one in line[2:]:
                        predict_list += [one.split("-")[1], one.split("-")[-1].strip()]
#                    print "predict_list", predict_list
                    for i in range(int(len(predict_list) / 2)):
                        a, b, c = get_match(origin, predict_list[2 * i: 2 * i + 2])
#                        print a, b, c
                        if c == 1 or b == 1:
                            compiler += a
                            optimization += b
                            combined += c
                            break
                if b == 0:
                    print line

#    print "Compiler family,", compiler_family * 1.0 / total
    #if total<=0:
    #	total=1
    
    print "Compiler,", compiler * 1.0 / total
    print "Optimization,", optimization * 1.0 / total
    print "Combined,", combined * 1.0 / total
    print compiler, optimization, combined, total

    return optimization * 1.0 / total

if __name__ == "__main__":

    if len(sys.argv) != 2:
        print "python get_test_accu.py <test_result.csv>"
        exit(-1)
    print "input "+sys.argv[1]
    get_test_accuracy(sys.argv[1])

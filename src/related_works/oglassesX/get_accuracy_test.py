import os
from subprocess import *

compilerList = ["GCC", "ICC", "CLANG", "LLVM", "PGI"]

def get_match_provenance(ground_truth, predicted):

    #print "In get_match_provenance: ",ground_truth, predicted
    a,b,c,com= 0,0,0,0
    gt_labels = ground_truth.split("-")
    isCombined = False
    predicted = [predicted]
    for predict in predicted:
    	pt_label = predict.strip().split("-")
    	print(predict)
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
	
	
def Execute(binaryfile, model,length=64,blocklimit=25000):
    cmd = "python3 get_accuracy.py -im {0} -i {1} -l {2} -s {3}".format(model, binaryfile, length, blocklimit).replace('\n','')
    print(cmd)
    p = Popen(cmd, shell=True, stdout=PIPE, stderr=PIPE)
    msg, err = p.communicate()
    print(msg)
    if (len(err) > 0):
        print ("Error message:", err)
    return msg
    
#Comment any one of the level to do the testing    
# software level testing
unseen_binaryfiles = '/home/UNT/mi0214/oglassesX_installed/vestige_baseline_ds/oglasses_sw_level/test.txt'
model='/home/UNT/mi0214/oglassesX_installed/modified_oglassesX/models/software_level/sw_vestige_baseline_model'

#binary level testing
unseen_binaryfiles = '/home/UNT/mi0214/oglassesX_installed/vestige_baseline_ds/oglasses_binary_level/test.txt'
model='/home/UNT/mi0214/oglassesX_installed/modified_oglassesX/models/binary_level/binary_vestige_baseline_model'

unseen_binaryfiles = open(unseen_binaryfiles, 'r')

total = 0
compiler = 0
optimization = 0
combined = 0
version = 0
total = 0
predicted_total = 0

for binfile in unseen_binaryfiles:
        
        
        data=str(Execute(binfile,model).decode("utf-8"))
        #data="b'[0, 0, 0, 0, 0, 0, 0, 0, 90, 73511, 9, 65754, 13, 0, 1001, 8729, 0, 0, 0, 0, 0, 0, 0, 0] CLANG5.0_32_O1\nTime: 2723.4689571857452\n'"
        #data="[0, 0, 0, 0, 0, 0, 0, 0, 16, 16738, 2, 11127, 19, 0, 395, 2258, 0, 0, 0, 0, 0, 0, 0, 0] CLANG5.0_32_O1\nTime: 563.8351168632507\n"
        
        # getting file name and removing the suffix .bin
        filename = binfile.split("/")[-1]
        filename = filename[:len(filename)-5]
        
        # get ground truth label of the binary
        gt_bin_comp, gt_bin_version,gt_bin_olvl = getGroundTruth(filename)	
        ground_truth = (gt_bin_comp+ "-"+gt_bin_version+"-"+gt_bin_olvl).strip()
        
        # get predicted labels
        out=data.split("\n")
        predicted = out[0][out[0].find(']')+1:len(out[0])].strip()
        predicted_output = predicted.split('_')
        if "GCC" in predicted_output[0]:
                pr_comp = "GCC"
                pr_ver = predicted_output[0][4:len(predicted_output[0])]
        else:
                pr_comp = "CLANG"
                pr_ver = predicted_output[0][5:len(predicted_output[0])]  
        
        pr_op_level = predicted_output[2]
        predicted_label= (pr_comp + "-" + pr_ver + "-" + pr_op_level).strip()
        
        print(ground_truth,predicted_label)
        
        com,a,b,c = get_match_provenance(ground_truth,predicted_label)
        #compiler += a
        	#optimization += b
        	#combined += c
        combined += com
        compiler += a
        version += b
        optimization += c
        total+=1
        print (com,a,b,c)
        print(predicted_label,ground_truth)
print ("Compiler,", compiler * 1.0 / total)
print ("Optimization,", optimization * 1.0 / total)
print ("Version,", version * 1.0 / total)
print ("Combined,", combined * 1.0 / total)
print (compiler,version, optimization, combined, total)

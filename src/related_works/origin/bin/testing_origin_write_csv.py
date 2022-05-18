import os
import sys
import commands


def test_origin(input_file, output_file,model_dir):

# currently use os.listdir, may extend to os.walk later

    #bin_list = os.listdir(input_folder)
    bin_list = open(input_file, 'r')
    count = 0
    #tot = 0
    with open(output_file, "w") as fp_write:
        for bin_name in bin_list:
#            if "_x86_" not in bin_name:
#                continue
            bin_path = bin_name #os.path.join(input_folder, bin_name)
            count = count +1

            cmd = "python2 _Origin.py --binpath %s --modeldir %s --workingdir /home/UNT/mi0214/work_dir/  --installdir /home/UNT/mi0214/origin_ins/" %(bin_path,model_dir) 
            cmd = cmd.replace("\n","")

            print "model: ",cmd 
            #print len(cmd)
            status, output = commands.getstatusoutput(cmd)
            print "status: "+str(output)
            
            if "Address" in output:
            	#tot = tot + 1
            	splited = output.split("\n") #output of origin is splitted 
            	address_string = splited[2]
            	
            	predicted_provenance = address_string.strip().split(",")[1:]
            	predicted_provenance = ",".join(predicted_provenance)
            	print  "Writing to file: Binary Name: "+bin_name.strip() +"\nPredicted " +str(predicted_provenance)
            	
            	if status == 0:
                	fp_write.write(bin_name.strip() + "," + predicted_provenance + "\n")
            
            #print output

            #if status == 0:
             #   fp_write.write(bin_name + "," + output + "\n")
            
            #if count>=15:
            #	break

if __name__ == "__main__":

    if len(sys.argv) != 4:
        print "python test_origin.py <test_file_txt> <output_file><model_dir>"
        exit(-1)

    test_origin(sys.argv[1], sys.argv[2],sys.argv[3])


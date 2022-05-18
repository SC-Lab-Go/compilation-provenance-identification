import sys
import argparse
import os
from subprocess import *

compilerList = ["GCC", "ICC","CLANG", "LLVM", "PGI"]

def getParameters():
    parser = argparse.ArgumentParser(description='Extract function level code features for toolchain identification')
    parser.add_argument("--filelist", help="A list of binaries to extract features", required=True)
    parser.add_argument("--outputdir", help="The directory to store extracted features", required = True)
    parser.add_argument("--idiom", help="Extract instruction idioms with specified sizes.")
    parser.add_argument("--graphlet", help="Extract graphlets for functions")
    parser.add_argument("--path_to_extract_bin", help="The installed binary for extracting features", required=True)
    parser.add_argument("--thread", help="The number of threads for feature extraction", type=int, default=1)
    args = parser.parse_args()
    return args 

def ParseFeatureSize(param):
    if param == None:
        return None
    ret = []
    for size in param.split(":"):
        ret.append(int(size))
    return ret

def Execute(featType, featSize, path, filename):
    global featureDir
    out = os.path.join(featureDir, "{0}.{1}.{2}".format(filename, featType, featSize))
    cmd = "OMP_NUM_THREADS={0} ".format(args.thread)
    #cmd += "LD_PRELOAD=/home/xm13/dyninst-pp/install/lib/libtbbmalloc_proxy.so "
    
    cmd += "LD_PRELOAD=/home/UNT/mi0214/spack/opt/spack/linux-ubuntu20.04-x86_64_v4/gcc-9.3.0/intel-tbb-2020.3-djkwn3y3j7romjovlzjozssq7oegile2/lib/libtbbmalloc_proxy.so "
    cmd += "{0} {1} {2} {3} {4}".format(args.path_to_extract_bin, path, featType, featSize, out)
    print cmd
    p = Popen(cmd, shell=True, stdout=PIPE, stderr=PIPE)
    msg, err = p.communicate()
    print "Debug: ",msg
    if (len(err) > 0):
        print "1: Error message:", err
 

def GenerateFeatures(featType, featSizes, path, filename):
    if featSizes == None:
        return
    if featType == "libcall" or featType == "insns_freq":
        Execute(featType, 1, path, filename)
    else:
        for size in featSizes:
	    Execute(featType, size, path, filename)

def BuildDirStructure(featRootDir, dirs):
    curDir = os.getcwd()
    os.chdir(featRootDir)
    for d in dirs:
        if not os.path.exists(d):
	    os.makedirs(d)
	os.chdir(d)
    os.chdir(curDir)

def GenerateDirPath(parts):
    # the output directory should have the following structure
    # featureRootDir/proj/compiler/version/opt
    compiler = "None"
    for i in range(len(parts)):
        parts[i]=parts[i].upper()
        if parts[i] in compilerList:
	    compiler = parts[i]
	    version = parts[i+1]
	    opt = parts[i+2]
	    proj = parts[i-1]
	    break
    assert(compiler != "None")
    BuildDirStructure(args.outputdir, [proj, compiler, version, opt])
    return os.path.join(args.outputdir, proj, compiler, version, opt)

args = getParameters()
idiomSizes = ParseFeatureSize(args.idiom)
graphletSizes = ParseFeatureSize(args.graphlet)
for line in open(args.filelist, "r"):
    print line 
    path = line[:-1]
    parts = path.split("/")
    #print "length: "+str(len(parts))+"  "+str(path)
    featureDir = GenerateDirPath(parts)
    filename = path.split("/")[-1]
    #print "Done"
    GenerateFeatures("idiom", idiomSizes, path, filename)
    GenerateFeatures("graphlet", graphletSizes, path, filename)


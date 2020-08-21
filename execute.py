import os
import sys
import argparse
import csv 
from programs.data_processing.format_ghsom_input_vector import format_ghsom_input_vector
parser = argparse.ArgumentParser(description='manual to this script')
parser.add_argument('--tau1', type=float, default = 0.1)
parser.add_argument('--tau2', type=float, default=0.01)
parser.add_argument('--data', type=str, default=None)
parser.add_argument('--train_column', type=str, default = None)
parser.add_argument('--index', type=str, default=None)

args = parser.parse_args()

print('tau1 = %s, tau2 = %s' % (args.tau1, args.tau2))
print('data = %s, index = %s' % (args.data,args.index))
current_path = os.getcwd()
print('Current:',current_path)
##############################
# GHSOM Settings
##############################
# create ghsom input vector file 
#Ref: http://www.ifs.tuwien.ac.at/~andi/somlib/download/SOMLib_Datafiles.html#input_vectors
def create_ghsom_input_file(name, index, train_column):
    try:
        format_ghsom_input_vector(name, index, train_column)
        print('Success to create ghsom input file.')
    except Exception as e:
        print('Failed to create ghsom input file.')
        print('Error:',e)

# create ghsom prop file 
# Ref: http://www.ifs.tuwien.ac.at/dm/somtoolbox/examples/PROPERTIES
def create_ghsom_prop_file(name, tau1 = 0.1, tau2 = 0.01, sparseData ='yes', isNormalized = 'false', randomSeed = 7, xSize = 2, ySize = 2, learnRate = 0.7,numIterations = 20000):
    with open('./applications/%s/GHSOM/%s_ghsom.prop' % (name,name), 'w', newline='',encoding='utf-8') as csvfile:
        writer = csv.writer(csvfile)
        
        # Parameter settings
        writer.writerow(['workingDirectory=./'])
        writer.writerow(['outputDirectory=./output/%s' % name])
        writer.writerow(['namePrefix=%s' % name])
        writer.writerow(['vectorFileName=./data/%s_ghsom.in' % name])
        writer.writerow(['sparseData=%s' % sparseData])
        writer.writerow(['isNormalized=%s' % isNormalized])
        writer.writerow(['randomSeed=%s' % randomSeed])
        writer.writerow(['xSize=%s' % xSize])
        writer.writerow(['ySize=%s' % ySize])
        writer.writerow(['learnRate=%s' % learnRate])
        writer.writerow(['numIterations=%s' % numIterations])
        writer.writerow(['tau=%s' % tau1])
        writer.writerow(['tau2=%s' % tau2])

# clustering high-dimensional data
def ghsom_clustering(name):
    try:
        print('cmd=','.\programs\GHSOM\somtoolbox.bat GHSOM .\\applications\%s\GHSOM\%s_ghsom.prop -h' % (name,name))
        os.system('.\programs\GHSOM\somtoolbox.bat GHSOM .\\applications\%s\GHSOM\%s_ghsom.prop -h' % (name,name))
    except Exception as e:
        print('Error:',e)
# extract output data
def extract_ghsom_output(name, current_path):
    print('cmd=','7z e applications\%s\GHSOM\output\%s -o%s\\applications\%s\GHSOM\output\%s' % (name,name,current_path,name,name))
    os.system('7z e applications\%s\GHSOM\output\%s -o%s\\applications\%s\GHSOM\output\%s' % (name,name,current_path,name,name))



# check a new application folder is exist in /applications or not
if os.path.exists('%s/applications/%s' % (current_path, args.data)):
    print('Warning : /applications/%s is exist.' % args.data)
else:
    print('Creating /applications/%s ....' % args.data)
    try:
        # create a new application folder in /applications
        os.makedirs('%s/applications/%s' % (current_path, args.data))
        print('Success to create /applications/%s folder.' % (args.data))
        
        ##############################
        # data folders settings
        ##############################
        # create a folder for data
        os.makedirs('%s/applications/%s/data' % (current_path, args.data))

        ##############################
        # GHSOM folders settings
        ##############################
        # create a folder for GHSOM
        os.makedirs('%s/applications/%s/GHSOM' % (current_path, args.data))

        # # create a folder for GHSOM prop
        # os.makedirs('%s/applications/%s/GHSOM/prop' % (current_path, args.data))

        # create a folder for GHSOM input vector
        os.makedirs('%s/applications/%s/GHSOM/data' % (current_path, args.data))

        # create a folder for GHSOM output
        os.makedirs('%s/applications/%s/GHSOM/output' % (current_path, args.data))

        create_ghsom_input_file(args.data, args.index, args.train_column)
        create_ghsom_prop_file(args.data, args.tau1, args.tau2)
        ghsom_clustering(args.data)
        extract_ghsom_output(args.data, current_path)

    except Exception as e:
        print('Failed to create /applications/%s folder due to :%s' % (args.data, str(e)))

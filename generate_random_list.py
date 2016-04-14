import random
import os
ab_path = os.path.abspath(__file__)
path_folder = os.path.join(os.path.dirname(ab_path),'rating_log/v4')
file_list = os.listdir(path_folder)
file_list_amz = []
for files in file_list:
    fn = open(os.path.join(path_folder,files))
    line = fn.readline()
    if len(line)>20:
        print files
        file_list_amz.append(files)
print 'that is all'
print len(file_list_amz)
file_list_20 = random.sample(file_list_amz,20)
for file in file_list_20:
    print file


#!/usr/bin/python
#import os
import commands
#for i in range(0, 83):
for file_num in range(0, 1):
    #urls = os.system(index_command)
    index_output = commands.getstatusoutput('./index nz2_merged/' + str(file_num) + '_index')
    #urls = commands.getoutput(index_command)
    indexes = index_output[1].split('\n')
    length = 0
    for index in indexes:
        if index == '':
            continue
        status = index.split()
        url = status[0]
        length += int(status[3])
        print url, length
        data_output = commands.getstatusoutput('./data nz2_merged/' + str(file_num) + '_data ' + str(length))
        print data_output[1]
        if length > 14000:
            break

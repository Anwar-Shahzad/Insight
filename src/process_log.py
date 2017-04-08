import sys
import shlex
#import pandas as pd

#['./src/process_log.py', './log_input/log.txt', './log_output/hosts.txt', './log_output/hours.txt', './log_output/resources.txt', './log_output/blocked.txt']

#['221.195.71.14', '-', '-', '[01/Jul/1995:00:00:54', '-0400]', '"GET', '/shuttle/missions/sts-71/mission-sts-71.html', 'HTTP/1.0"', '200', '13387\n']

log = open(sys.argv[1],"r")
#log = open("../log.txt","r")

##### get top 10 hosts ####
hostTable = {}
resourceTable = {}
timeTable = {}
count = 0
#DD/MON/YYYY:HH:MM:SS -0400]
#index = pd.date_range('01/Jul/1995', periods=2471040, freq='S')
#series = pd.Series(0,index=index)
for line in log:
    lineList = shlex.split(line, posix=False)
    if lineList[-2] != '400':
        resourceName = lineList[5].split(' ')[1]
        resourceSize = 0 if lineList[-1] == '-' else lineList[-1]
        resourceSize = int(resourceSize)
        if resourceName in resourceTable:
            resourceTable[resourceName] += resourceSize
        else:
            resourceTable[resourceName] = resourceSize
    host = lineList[0]
    if host in hostTable:
        hostTable[host] += 1
    else:
        hostTable[host] = 1

    time = lineList[3][1:]
    reformat_time = time[:11] + ' ' + time[12:]
    #print reformat_time
    #temp = series.get(reformat_time)
    #print temp
    #series.set_value(reformat_time, temp+1)


        
    if count % 100000 == 0:
        print count / 100000
    count += 1
    
host_file = open(sys.argv[2],"w")
#host_file = open("../hosts.txt","w")   
host_file.writelines([host + "," + str(hostTable[host]) + "\n" for host in sorted(hostTable, key = hostTable.get, reverse = True)[:10]])
host_file.close()

resource_file = open(sys.argv[4],"w")
#resource_file = open("../resources.txt","w")
resource_file.writelines([resourceName + "\n" for resourceName in sorted(resourceTable, key = resourceTable.get, reverse = True)[:10]])
resource_file.close()

#resource_file = open(sys.argv[4],"r")
#print resource_file.read()

log.close()

import sys
import shlex

#['./src/process_log.py', './log_input/log.txt', './log_output/hosts.txt', './log_output/hours.txt', './log_output/resources.txt', './log_output/blocked.txt']

#['221.195.71.14', '-', '-', '[01/Jul/1995:00:00:54', '-0400]', '"GET', '/shuttle/missions/sts-71/mission-sts-71.html', 'HTTP/1.0"', '200', '13387\n']

log = open(sys.argv[1],"r")

##### get top 10 hosts ####
hostTable = {}
resourceTable = {}
count = 0
for line in log:
    lineList = shlex.split(line, posix=False)
    try:
        resourceName = lineList[5].split(' ')[1]
    except IndexError:
        print lineList
    resourceSize = 0 if lineList[-1] == '-' else lineList[-1]
    #if isinstance(resourceSize, str):
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
    if count % 100000 == 0:
        print count / 100000
    count += 1
    
host_file = open(sys.argv[2],"w")
host_file.writelines([host + "," + str(hostTable[host]) + "\n" for host in sorted(hostTable, key = hostTable.get, reverse = True)[:10]])
host_file.close()

resource_file = open(sys.argv[4],"w")
resource_file.writelines([resourceName + "\n" for resourceName in sorted(resourceTable, key = resourceTable.get, reverse = True)[:10]])
resource_file.close()

resource_file = open(sys.argv[4],"r")
#print resource_file.read()

log.close()

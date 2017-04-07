import sys

#['./src/process_log.py', './log_input/log.txt', './log_output/hosts.txt', './log_output/hours.txt', './log_output/resources.txt', './log_output/blocked.txt']

#print len(sys.argv)
#print str(sys.argv)

#print str(sys.argv[1])

log = open(sys.argv[1],"r")
#print log.read()


##### get top 10 hosts ####
hostTable = {}
for line in log:
    lineList = line.split(' ')
    host = lineList[0]
    if host in hostTable:
        hostTable[host] += 1
    else:
        hostTable[host] = 1
host_file = open(sys.argv[2],"w")
host_file.writelines([str(host) + "," + str(hostTable[host]) + "\n" for host in sorted(hostTable, key = hostTable.get, reverse = True)[:10]])





host_file.close()
log.close()

# 0.2
#
# 0.1: init app
# 0.2: add snimpy, logging and argparser
#
#
#
# ftp://ftp.cisco.com/pub/mibs/v2/CISCO-PROCESS-MIB.my
# ftp://ftp.cisco.com/pub/mibs/v2/CISCO-MEMORY-POOL-MIB.my
# ftp://ftp.cisco.com/pub/mibs/v2/CISCO-QOS-PIB-MIB.my
#
# + www reference
# http://www.oidview.com/mibs/9/CISCO-PROCESS-MIB.html
# https://supportforums.cisco.com/document/30366/oids-management
#
# + place where place mibs on mac
# cd /usr/local/share/mibs/ietf
# cd /usr/local/Cellar/libsmi/0.4.8/share/mibs/ietf

from ascii_graph import Pyasciigraph
from ascii_graph.colors import *
from ascii_graph.colordata import vcolor
from ascii_graph.colordata import hcolor

import logging, argparse, time, os

from snimpy.manager import Manager as M
from snimpy.manager import load

def main():

	os.system('clear')

	parser = argparse.ArgumentParser(description='cpu and memory realtime graph')

	parser.add_argument('-d','--deviceName', required=True, help="eg. mi-caiomario-ar501", dest="deviceName", default="mi-caiomario-ar501")
	parser.add_argument('-c','--community', required=False, help="eg. fwrocmn", dest="deviceComm", default="public")

	parser.add_argument('-m','--memory', required=False, help="eg. fwrocmn", action='store_true', dest="deviceMem", default=None)
	
	args = parser.parse_args()

	load("RFC1213-MIB")					# sysName, ecc..
	load("IP-FORWARD-MIB")
	load("IF-MIB")
	load("SNMPv2-MIB")
	load("SNMPv2-SMI")
	load("CISCO-PROCESS-MIB")
	load("CISCO-MEMORY-POOL-MIB")

	for loop in range(10):

		m = M(args.deviceName, args.deviceComm, 2)
		print m.sysDescr
		# print str(m.sysObjectID)

		m = M(args.deviceName, args.deviceComm, 2)

		for i in m.cpmCPUTotal5sec:
			cpu5s = m.cpmCPUTotal5sec[i]
		for i in m.cpmCPUTotal1min:
			cpu1m = m.cpmCPUTotal1min[i]
		for i in m.cpmCPUTotal5min:
			cpu5m = m.cpmCPUTotal5min[i]

		print

		cpuData = [ \
			('cpmCPUTotal5sec', cpu5s), \
			('cpmCPUTotal1min', cpu1m), \
			('cpmCPUTotal5min', cpu5m), \
			]

		pattern = [Gre, Yel, Red]
		col_cpuData = vcolor(cpuData, pattern)

		graph = Pyasciigraph()
		for line in  graph.graph(label='CPU Graph', data=col_cpuData):
		    print line

		if args.deviceMem:


			memFree = m.ciscoMemoryPoolFree[1]

			memUsed = m.ciscoMemoryPoolUsed[1]

			memData = [ \
				('ciscoMemoryPoolFree', memFree), \
				('ciscoMemoryPoolUsed', memUsed), \
				]

			pattern = [Gre, Yel, Red]
			col_memData = vcolor(memData, pattern)

			graph = Pyasciigraph()
			for line in  graph.graph(label='MEM Graph', data=col_memData):
			    print line

		time.sleep(5)
		os.system('clear')

if __name__ == '__main__':
	main()
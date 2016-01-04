# 0.7
#
# 0.1: init app
# 0.2: add snimpy, logging and argparser
# 0.3: tune graph, add hostname
# 0.4: minor changes
# 0.5: revert in objects
# 0.6: add logging
# 0.7: add history in 5 seconds graph
#

# buitins
import logging, argparse, time, os

# pip install
from ascii_graph import Pyasciigraph
from ascii_graph.colors import *
from ascii_graph.colordata import vcolor
from ascii_graph.colordata import hcolor

from snmpEngine import Device

# ++++++++++++++++++++
import logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)
# --------------------	

def main():

	os.system('clear')

	parser = argparse.ArgumentParser(description='cpu and memory realtime graph')

	parser.add_argument('-d','--deviceName', required=True, help="eg. mi-caiomario-ar501", dest="deviceName", default="mi-caiomario-ar501")
	parser.add_argument('-c','--community', required=False, help="eg. fwrocmn", dest="deviceComm", default="public")

	parser.add_argument('-m','--memory', required=False, help="eg. fwrocmn", action='store_true', dest="deviceMem", default=None)
	
	args = parser.parse_args()

	r1 = Device(args.deviceName, args.deviceComm)

	cpuData = []

	for index in range(10):

		### system infos	

		print r1.get_hostname
		print 
		print r1.get_descr
		# print r1.get_objID
		print 

		### 5 sec cpu with history

		r1.set_cpuStat()
		logging.debug(r1._cpu_5_sec)

		for inx,r1_5_sec_explode in enumerate(r1._cpu_5_sec):
			if index == inx:
				cpuData.append(('cpmCPUTotal5sec <==', r1_5_sec_explode))
			else:
				cpuData.append(('cpmCPUTotal5sec', r1_5_sec_explode))

		pattern = [Gre, Gre, Gre]
		col_cpuData = vcolor(cpuData, pattern)

		graph = Pyasciigraph(
			graphsymbol='*')
		for line in  graph.graph(label='CPU Graph (sh processes cpu sorted | i ^CPU)', data=col_cpuData):
		    print line

		print
		### 1 and 5 min cpu

		logging.debug(r1._cpu_1_min)
		logging.debug(r1._cpu_5_min)

		cpuData = [ \
			('cpmCPUTotal1min', r1._cpu_1_min[index]), \
			('cpmCPUTotal5min', r1._cpu_5_min[index]), \
			]

		pattern = [Yel, Red]
		col_cpuData = vcolor(cpuData, pattern)

		graph = Pyasciigraph()
		for line in  graph.graph(label='CPU Graph (sh processes cpu sorted | i ^CPU)', data=col_cpuData):
		    print line

		print
		### memory stats

		if args.deviceMem:

			r1.set_memStat()
			logging.debug(r1._mem_Free)
			logging.debug(r1._mem_Used)
			logging.debug(r1._mem_Alloc)

			memData = [ \
				('ciscoMemoryTotal', r1._mem_Free[index] + r1._mem_Used[index]), \
				('ciscoMemoryPoolFree', r1._mem_Free[index]), \
				('ciscoMemoryPoolUsed', r1._mem_Used[index]), \
				('ciscoMemoryPoolLargestFree', r1._mem_Alloc[index]), \
				]

			pattern = [Gre, Yel, Red, Blu]
			col_memData = vcolor(memData, pattern)

			graph = Pyasciigraph(
			human_readable='si',
			graphsymbol='+')
			for line in  graph.graph(label='MEM Graph (sh process memory sorted | i Processor Pool)', data=col_memData):
			    print line

		cpuData = []
		time.sleep(5)
		os.system('clear')

if __name__ == '__main__':
	main()
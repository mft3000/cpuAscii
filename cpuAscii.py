# 0.6
#
# 0.1: init app
# 0.2: add snimpy, logging and argparser
# 0.3: tune graph, add hostname
# 0.4: minor changes
# 0.5: revert in objects
# 0.6: add logging
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

	cpu = []
	mem = []

	for loop in range(10):

		print r1.get_hostname
		print 
		print r1.get_descr
		# print r1.get_objID

		r1.set_cpuStat()
		logging.info(r1._cpu_5_sec)
		logging.info(r1._cpu_1_min)
		logging.info(r1._cpu_5_min)

		cpuData = [ \
			('cpmCPUTotal5sec', r1._cpu_5_sec[-1]), \
			('cpmCPUTotal1min', r1._cpu_1_min[-1]), \
			('cpmCPUTotal5min', r1._cpu_5_min[-1]), \
			]

		pattern = [Gre, Yel, Red]
		col_cpuData = vcolor(cpuData, pattern)

		graph = Pyasciigraph()
		for line in  graph.graph(label='CPU Graph (sh processes cpu sorted | i ^CPU)', data=col_cpuData):
		    print line

		if args.deviceMem:

			r1.set_memStat()
			logging.info(r1._mem_Free)
			logging.info(r1._mem_Used)
			logging.info(r1._mem_Alloc)

		# 	memFree = m.ciscoMemoryPoolFree[1]

		# 	memUsed = m.ciscoMemoryPoolUsed[1]

		# 	memValid = m.ciscoMemoryPoolLargestFree[1]

			memData = [ \
				('ciscoMemoryTotal', r1._mem_Free[-1] + r1._mem_Used[-1]), \
				('ciscoMemoryPoolFree', r1._mem_Free[-1]), \
				('ciscoMemoryPoolUsed', r1._mem_Used[-1]), \
				('ciscoMemoryPoolLargestFree', r1._mem_Alloc[-1]), \
				]

			pattern = [Gre, Yel, Red]
			col_memData = vcolor(memData, pattern)

			graph = Pyasciigraph(
			human_readable='si',
			graphsymbol='+')
			for line in  graph.graph(label='MEM Graph (sh process memory sorted | i Processor Pool)', data=col_memData):
			    print line

		time.sleep(5)
		os.system('clear')

if __name__ == '__main__':
	main()
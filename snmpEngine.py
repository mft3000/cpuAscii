# 0.1
#
# 0.1: init lib
#
# sh processes cpu sorted | i ^CPU
# sh process memory sorted | i Processor Pool
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

# buitins
import logging

# pip install

from snimpy.manager import Manager as M
from snimpy.manager import load

load("RFC1213-MIB")					# sysName, ecc..
load("IP-FORWARD-MIB")
load("IF-MIB")
load("SNMPv2-MIB")
load("SNMPv2-SMI")
load("CISCO-PROCESS-MIB")
load("CISCO-MEMORY-POOL-MIB")

# ++++++++++++++++++++
import logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)
# --------------------	

class Device(object):

	snmpCommunity = "public"
	snmpTarget = ""
	sysName = ""
	sysDescr = ""
	sysObjectID = ""

	def __init__(self, target, community):
		
		self.snmpTarget = target
		self.snmpCommunity = community
		m = M(host=self.snmpTarget, community=self.snmpCommunity, version=2, none=True)

		self._cpu_5_sec = list()
		self._cpu_1_min = list()
		self._cpu_5_min = list()

		self._mem_Free = list()
		self._mem_Used = list()
		self._mem_Alloc = list()

		logging.info("loading hostname infos [1/x]...")

		self.sysName = str(m.sysName)

		logging.info("loading sysDescr infos [2/x]...")

		self.sysDescr = str(m.sysDescr)

		# logging.info("loading sysObjectID infos [3/x]...")

		# self.sysObjectID = str(m.sysObjectID)

	@property
	def get_hostname(self):
		"""
		Return hostname
		"""
		return self.sysName

	@property
	def get_descr(self):
		"""
		Return hostname
		"""
		return self.sysDescr

	@property
	def get_objID(self):
		"""
		Return hostname
		"""
		return self.sysObjectID

	def set_cpuStat(self):
		"""
		Return cpu infos
		"""
		m = M(host=self.snmpTarget,community=self.snmpCommunity,none=True)

		logging.info("loading cpu infos [4/x]...")

		for i in m.cpmCPUTotal5sec:
			self._cpu_5_sec.append(int(m.cpmCPUTotal5sec[i]))
		for i in m.cpmCPUTotal1min:
			self._cpu_1_min.append(int(m.cpmCPUTotal1min[i]))
		for i in m.cpmCPUTotal5min:
			self._cpu_5_min.append(int(m.cpmCPUTotal5min[i]))

	def set_memStat(self):
		"""
		Return cpu infos
		"""
		m = M(host=self.snmpTarget,community=self.snmpCommunity,none=True)
		
		logging.info("loading memory infos [5/x]...")

		self._mem_Free.append(int(m.ciscoMemoryPoolFree[1]))

		self._mem_Used.append(int(m.ciscoMemoryPoolUsed[1]))

		self._mem_Alloc.append(int(m.ciscoMemoryPoolLargestFree[1]))

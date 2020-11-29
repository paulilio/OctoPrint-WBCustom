# coding=utf-8
__author__ = "AstroPrint Product Team <product@astroprint.com>"
__license__ = 'GNU Affero General Public License http://www.gnu.org/licenses/agpl.html'

try:
    import urllib.request as urllib2
except ImportError:
    import urllib2
import socket, subprocess

from sys import platform

from octoprint.settings import settings
#from octoprint_WBCustom.astroprint.config import settings
#from octoprint_WBCustom.astroprint.settings import settings
from octoprint_WBCustom.astroprint.ro_config import roConfig

from .ssl import SslManager

class NetworkManager(object):
	def __init__(self):
		self.settings = settings()
		self.sslManager = SslManager()

	def isAstroprintReachable(self):
		try:
			urllib2.urlopen("%s/check" % roConfig('cloud.apiHost'),timeout=1)
			return True

		except urllib2.URLError:
			return False

	def checkOnline(self):
		timeout= 1
		addresses= ['8.8.8.8', '8.8.4.4', '208.67.222.222', '208.67.220.220'] #Google DNS(2), OpenDNS(2)

		for addr in addresses:
			status = subprocess.call("ping -W %d -c 1 %s > /dev/null 2>&1" % (timeout, addr), shell=True)
			if status == 0:
				return True
			else:
				continue

		return False

	# Called only once right after creation, it should do startup things that take some time so the creation Lock
  # does not block for too long. Only things that can be delayed as another thread can get the handle to the manager
  # before this function has been called.
	def startUp(self):
		return None

	def shutdown(self):
		return None

	def close(self):
		return None

	def conectionStatus(self):
		return 'connected'

	def getWifiNetworks(self):
		return None

	def isHotspotable(self):
		return None

	def getActiveConnections(self):
		return None

	def setWifiNetwork(self, bssid, password):
		return None

	def forgetWifiNetworks(self):
		return None

	def storedWifiNetworks(self):
		return []

	def deleteStoredWifiNetwork(self, networkId):
		return None

	def isHotspotActive(self):
		return None

	def hasWifi(self):
		return None

	def isOnline(self):
		return None

	def startHotspot(self):
		#return True when succesful
		return "Starting a hotspot is not supported"

	def stopHotspot(self):
		#return True when succesful
		return "Stopping a hotspot is not supported"

	def getHostname(self):
		return None

	def setHostname(self, name):
		return None

	@property
	def activeIpAddress(self):
		return None


	# Returns information about the network devices present
	# in the box
	#
	# [ { id, mac, type (wifi, wired), connected }, ..]
	@property
	def networkDeviceInfo(self):
		return None

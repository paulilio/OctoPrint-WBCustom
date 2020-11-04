# coding=utf-8
__author__ = "Daniel Arroyo <daniel@astroprint.com>"
__license__ = 'GNU Affero General Public License http://www.gnu.org/licenses/agpl.html'

import logging
import threading
import time
import os

from octoprint.server import eventManager
from octoprint.events import Events
from octoprint.settings import settings


from octoprint_WBCustom.astroprint.network import NetworkManager

class MacDevNetworkManager(NetworkManager):
	def __init__(self):
		self.logger = logging.getLogger(__name__)
		self._online = False
		self._storedWiFiNetworks = []
		self._config = {
			"autoConnect" : True,
			"name": "astrobox-dev"
		}

		self._loadDevConfig()

		self.name = self._config["name"]

		if self._config['autoConnect']:
			self._setActiveWifi(self.getWifiNetworks()[0])

		super(MacDevNetworkManager, self).__init__()

	def getActiveConnections(self):
		wireless = None
		wired = None

		wired = {
			'name': 'Wired Test',
			'ip': '127.0.0.1:5000',
			'mac': 'wi:re:d2:34:56:78:90',
		}

		if self._storedWiFiNetworks:
			for n in self._storedWiFiNetworks:
				if n['active']:
					wireless = {
						'id': 'localhost',
						'signal': 80,
						'name': n['name'],
						'ip': '127.0.0.1:5000',
						'mac': 'wi:fi:12:34:56:78:90',
						'secured': True
					}

		return {
			'wired': wired,
			'wireless': wireless,
			'manual': None
		}

	def storedWifiNetworks(self):
		return self._storedWiFiNetworks

	def deleteStoredWifiNetwork(self, networkId):
		for i in range(0, len(self._storedWiFiNetworks)):
			n = self._storedWiFiNetworks[i]
			if n['id'] == networkId:
				if n['active']:
					self._goOffline()
					eventManager.fire(Events.INTERNET_CONNECTING_STATUS, {'status': 'disconnected'})

				del self._storedWiFiNetworks[i]
				self.logger.info("Network [%s] with id [%s] deleted." % (n['name'], n['id']))
				return n['id']

	def hasWifi(self):
		return True

	def getWifiNetworks(self):
		return [
			{"id": "80:1F:02:F9:16:1B", "name": "Secured Network", "secured": True, "signal": 80, "wep": False},
			{"id": "90:1F:02:F9:16:1C", "name": "Open Network", "secured": False, "signal": 78, "wep": False},
			{"id": "74:DA:38:88:51:90", "name": "WEP Network", "secured": True, "signal": 59, "wep": True},
			{"id": "C0:7B:BC:1A:5C:81", "name": "Open Failed", "secured": False, "signal": 37, "wep": False}
		]

	def setWifiNetwork(self, bssid, password):
		for n in self.getWifiNetworks():
			if n['id'] == bssid:
				if n['secured']:
					if not password or len(password) < 3:
						self.logger.info("Missing password for a secured network")
						time.sleep(2)
						return 	{
							'err_code': 'invalid_psk',
							'message': 'Invalid Password'
						}

					elif password != 'pwd':
						self.logger.info("Password invalid. Needs to be 'pwd'")

						def action():
							eventManager.fire(Events.INTERNET_CONNECTING_STATUS, {'status': 'connecting'})
							time.sleep(2)
							eventManager.fire(Events.INTERNET_CONNECTING_STATUS, {'status': 'failed', 'reason': "no_secrets"})

						timer = threading.Timer(3, action)
						timer.daemon = True
						timer.start()

						return {"name": n['name']}

				else:
					if n["id"] == 'C0:7B:BC:1A:5C:81':
						self.logger.info("Open network with NO connection")

						def action():
							eventManager.fire(Events.INTERNET_CONNECTING_STATUS, {'status': 'connecting'})
							time.sleep(2)
							eventManager.fire(Events.INTERNET_CONNECTING_STATUS, {'status': 'failed', 'reason': "no_connection"})

						timer = threading.Timer(3, action)
						timer.daemon = True
						timer.start()

						return {"name": n['name']}

				time.sleep(1)
				return self._setActiveWifi(n)

	def isAstroprintReachable(self):
		return self.isOnline()

	def checkOnline(self):
		return self.isOnline()

	def isOnline(self):
		return self._online

	def startHotspot(self):
		#return True when succesful
		return "Not supporded on Mac"

	def stopHotspot(self):
		#return True when succesful
		return "Not supporded on Mac"

	def getHostname(self):
		return self.name

	def setHostname(self, name):
		self.name = name
		self.logger.info('Host name is set to %s ' % name)
		return True

	@property
	def activeIpAddress(self):
		return '127.0.0.1'

	@property
	def networkDeviceInfo(self):
		return [
			{
				'id': 'eth0',
				'mac': 'wi:re:d2:34:56:78:90',
				'type': 'wired',
				'connected': True
			},
			{
				'id': 'wlan0',
				'mac': 'wi:fi:12:34:56:78:90',
				'type': 'wifi',
				'connected': False
			}
		]

	def _goOnline(self):
		self._online = True
		eventManager.fire(Events.NETWORK_STATUS, 'online')

	def _goOffline(self):
		self._online = False
		eventManager.fire(Events.NETWORK_STATUS, 'offline')

	def _setActiveWifi(self, network):
		self.logger.info("Selected WiFi: %s" % network['name'])
		for n in self._storedWiFiNetworks:
			n['active'] = False

		self._storedWiFiNetworks.append({
			'id': network['id'],
			'name': network['name'],
			'active': True
		})

		def action():
			eventManager.fire(Events.INTERNET_CONNECTING_STATUS, {'status': 'connecting'})
			time.sleep(1)
			eventManager.fire(Events.INTERNET_CONNECTING_STATUS, {
				'status': 'connected',
				'info': {
					'type': 'wifi',
					'signal': network['signal'],
					'name': network['name'],
					'ip': '127.0.0.1:5000'
				}
			})

			self._goOnline()

		timer = threading.Timer(2, action)
		timer.daemon = True
		timer.start()

		return {'name': network['name']}

	def _loadDevConfig(self):
		settings_file = "%s/mac-dev-network.yaml" % settings().getConfigFolder()

		if os.path.isfile(settings_file):
			import yaml

			config = None
			with open(settings_file, "r") as f:
				config = yaml.safe_load(f)

			if config:
				def merge_dict(a,b):
					for key in b:
						if isinstance(b[key], dict):
							merge_dict(a[key], b[key])
						else:
							a[key] = b[key]

				merge_dict(self._config, config)

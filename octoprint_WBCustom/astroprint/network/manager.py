# coding=utf-8
__author__ = "Daniel Arroyo <daniel@astroprint.com>"
__license__ = 'GNU Affero General Public License http://www.gnu.org/licenses/agpl.html'

import threading

# singleton
_instance = None
creationLock = threading.Lock()

def networkManager():
	global _instance

	if _instance is None:
		needsStartingUp = False
		with creationLock:
			if _instance is None:
				#from octoprint_WBCustom.octoprint.settings import settings

				# we can't use a map as some of the import from the driver instances only
				# exists in their environments

				#driver = settings().get(['network', 'manager'])
				driver = "debianNetworkManager"

				if driver == 'debianNetworkManager':
					from octoprint_WBCustom.astroprint.network.debian import DebianNetworkManager

					_instance = DebianNetworkManager()

				elif driver == 'manual':
					from octoprint_WBCustom.astroprint.network.manual import ManualNetworkManager

					_instance = ManualNetworkManager()

				elif driver == 'MacDev':
					from octoprint_WBCustom.astroprint.network.mac_dev import MacDevNetworkManager

					_instance = MacDevNetworkManager()

				else:
					raise Exception('Invalid network manager: %s' % driver)

				needsStartingUp = True

		if needsStartingUp:
			_instance.startUp()

	return _instance

def networkManagerShutdown():
	global _instance

	_instance.shutdown()
	_instance = None

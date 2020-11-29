# coding=utf-8
__author__ = "AstroPrint Product Team <product@astroprint.com>"
__license__ = "GNU Affero General Public License http://www.gnu.org/licenses/agpl.html"
__copyright__ = "Copyright (C) 2016 3DaGoGo, Inc - Released under terms of the AGPLv3 License"

ASSETS_DEBUG = True
ASSETS_AUTO_BUILD = True

#APPNAME = 'AstroBox'
#instance = None
_instance = None

def settings():
	global _instance

	if _instance is None:

		default_settings = {'serial': {'port': None,
					'baudrate': None,
					'autoconnect': True,
					'log': False,
					'dsrdtrFlowControl': False,
					'rtsctsFlowControl': False,
					'swFlowControl': True,
					'timeout': {'detection': 0.5,
								'connection': 2.0,
								'communication': 10.0,
								'first_contact': 20.0,
								'temperature': 5,
								'sdStatus': 1},
					'additionalPorts': []},
		'server': {'host': '0.0.0.0',
					'port': 5000,
					'firstRun': True,
					'baseUrl': '',
					'scheme': '',
					'maxUploadSize': 200},
		'camera': {'manager': 'gstreamer',
					'encoding': 'h264',
					'size': '640x480',
					'framerate': '15/1',
					'format': 'x-raw',
					'pixelformat': 'YUYV',
					'source': 'USB',
					'debug-level': 0,
					'graphic-debug': False,
					'video-rotation': 0,
					'inactivitySecs': 120.0,
					'freq': 0},
		'clearFiles': False,
		'gcodeViewer': {'enabled': True,
						'mobileSizeThreshold': 2097152,
						'sizeThreshold': 20971520},
		'feature': {'temperatureGraph': True,
					'waitForStartOnConnect': False,
					'alwaysSendChecksum': False,
					'sdSupport': True,
					'sdAlwaysAvailable': False,
					'swallowOkAfterResend': True,
					'repetierTargetTemp': False},
		'folder': {'uploads': None,
					'timelapse': None,
					'timelapse_tmp': None,
					'logs': None,
					'virtualSd': None,
					'userPlugins': None,
					'tasks': None,
					'manufacturerPkg': None},
		'temperature': {'profiles': [{'name': 'ABS', 'extruder': 210, 'bed': 100}, {'name': 'PLA', 'extruder': 180, 'bed': 60}]}, 'printerParameters': {'movementSpeed': {'x': 6000,
												'y': 6000,
												'z': 700,
												'e': 100},
								'pauseTriggers': [], 'invertAxes': [], 'numExtruders': 1,
								'extruderOffsets': [{'x': 0.0, 'y': 0.0}], 'bedDimensions': {'x': 200.0,
												'y': 200.0, 'r': 100}},
		'appearance': {'name': '',
						'color': 'default'},
		'controls': [], 'system': {'actions': []}, 'accessControl': {'enabled': True,
							'userManager': 'astroprint.users.FilebasedUserManager',
							'userfile': None,
							'autologinLocal': False,
							'localNetworks': [
											'127.0.0.0/8'],
							'autologinAs': None},
		'cura': {'enabled': False,
					'path': '/default/path/to/cura',
					'config': '/default/path/to/your/cura/config.ini'},
		'cloudSlicer': {'loggedUser': None},
		'events': {'enabled': False,
					'subscriptions': []},
		'api': {'enabled': True,
				'key': None,
				'regenerate': True,
				'allowCrossOrigin': True},
		'terminalFilters': [{'name': 'Suppress M105 requests/responses', 'regex': '(Send: M105)|(Recv: ok T\\d*:)'}, {'name': 'Suppress M27 requests/responses', 'regex': '(Send: M27)|(Recv: SD printing byte)'}], 'devel': {'stylesheet': 'css',
					'virtualPrinter': {'enabled': False,
										'okAfterResend': False,
										'forceChecksum': False,
										'okWithLinenumber': False,
										'numExtruders': 1,
										'includeCurrentToolInTemps': True,
										'hasBed': True,
										'repetierStyleTargetTemperature': False,
										'extendedSdFileList': False}},
		'wifi': {'hotspotDevice': None,
					'hotspotOnlyOffline': True},
		'network': {'manager': 'debianNetworkManager',
					'interface': 'wlan0',
					'ssl': {'domain': None}},
		'software': {'infoDir': None,
						'variantFile': None,
						'useUnreleased': False,
						'lastCheck': None,
						'channel': 20},
		'printerSelected': None,
		'materialSelected': None,
		'qualitySelected': None,
		'customQualitySelected': None}


		_instance = defaults

	return _instance

# coding=utf-8
__author__ = "AstroPrint Product Team <product@astroprint.com>"
__license__ = "GNU Affero General Public License http://www.gnu.org/licenses/agpl.html"
__copyright__ = "Copyright (C) 2017 3DaGoGo, Inc - Released under terms of the AGPLv3 License"

import json

from . import PluginService

from octoprint_WBCustom.astroprint.boxrouter import boxrouterManager
from octoprint_WBCustom.astroprint.cloud import astroprintCloud, AstroPrintCloudInsufficientPermissionsException
from octoprint.events import eventManager, Events
from octoprint.server import userManager
from octoprint.settings import settings
from octoprint.events import Events

class AccountService(PluginService):
	_validEvents = [
		#watch the state of the user's account: connecting, connected, disconnected , error
		'account_state_change',
		'boxrouter_state_change',
		'fleet_state_change'
	]

	def __init__(self):
		super(AccountService, self).__init__()
		self._eventManager.subscribe(Events.ASTROPRINT_STATUS, self._onBoxrouterStateChange)
		self._eventManager.subscribe(Events.LOCK_STATUS_CHANGED, self._onAccountStateChange)
		self._eventManager.subscribe(Events.FLEET_STATUS, self._onFleetStateChange)

	#REQUESTS

	def login(self, data,callback):
		email = private_key = password = None

		if 'email' in data:
			email = data['email']

		if 'password' in data:
			password = data['password']

		if 'private_key' in data:
			private_key = data['private_key']

		if email and password:
			try:
				if astroprintCloud().signin(email, password, hasSessionContext= False):
					callback('login_success')

			except AstroPrintCloudInsufficientPermissionsException as e:
				self._logger.error("Not enough permissions to login: %s" % json.dumps(e.data))
				if 'org' in e.data and 'in_org' in e.data['org']:
					if e.data['org']['in_org']:
						callback('in_org_no_permissions',True)
					else:
						callback('not_in_org',True)

				else:
					callback('unkonwn_login_error',True)

			except Exception as e:
				self._logger.error("Error Signing into AstroPrint Cloud: %s" % e)
				callback('astroprint_unrechable',True)

		elif email and private_key:
			try:
				if astroprintCloud().signinWithKey(email, private_key, hasSessionContext= False):
						callback('login_success')

			except Exception as e:
				self._logger.error('user unsuccessfully logged in',exc_info = True)
				callback('no_login',True)

		else:
			self._logger.error('Invalid data received for login')
			callback('invalid_data',True)

	def validate(self, data, callback):
		email = password = None

		if 'email' in data:
			email = data['email']

		if 'password' in data:
			password = data['password']

		if email and password:
			try:
				if astroprintCloud().validatePassword(email, password):
					callback('validate_success')
				else:
					callback('invalid_data',True)

			except Exception as e:
				self._logger.error("Error validating passwrod with AstroPrint Cloud: %s" % e)
				callback('astroprint_unrechable',True)

		else:
			self._logger.error('Invalid data received for login')
			callback('invalid_data',True)


	def logout(self, data, callback):
		try:
			astroprintCloud().signout(hasSessionContext= False)
			callback('user successfully logged out')

		except Exception as e:
			self._logger.error('user unsuccessfully logged out: %s' % e , exc_info = True)
			callback('logged_out_unsuccess',True)

	def getStatus(self, callback):
		try:
			sets = settings()
			user = sets.get(["cloudSlicer", "loggedUser"])

			payload = {
				'userLogged': user if user else None,
				'boxrouterStatus' :  boxrouterManager().status
			}
			callback(payload)

		except Exception as e:
			self._logger.error('unsuccessfully user status got: %s' %e, exc_info = True)
			callback('getting_status_error')

	def connectBoxrouter(self, callback):
		try:
			boxrouterManager().boxrouter_connect()
			callback('connect_success')
		except Exception as e:
			self._logger.error('boxrouter can not connect: %s' %e, exc_info = True)
			callback('boxrouter_error', True)

	#EVENTS

	def _onAccountStateChange(self,event,value):
		sets = settings()
		user = sets.get(["cloudSlicer", "loggedUser"])
		data = {
			'userLogged': user if user else None,
		}
		self.publishEvent('account_state_change',data)

	def _onBoxrouterStateChange(self,event,value):
			data = {
				'boxrouterStatus' :  boxrouterManager().status
			}
			self.publishEvent('boxrouter_state_change',data)

	def _onFleetStateChange(self,event,value):
			data = {
				'orgId' :  value['orgId'],
				'groupId' :  value['groupId']
			}
			self.publishEvent('fleet_state_change',data)

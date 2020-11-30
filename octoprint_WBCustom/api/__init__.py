# coding=utf-8
from __future__ import absolute_import

__author__ = "Paulilio Castello Branco <paulilio.branco@gmail.com>"
__license__ = "GNU Affero General Public License http://www.gnu.org/licenses/agpl.html"
__copyright__ = "Copyright (C) 2020 Paulilio Castello Branco - Released under terms of the AGPLv3 License"


import octoprint.plugin
from flask import request, abort, jsonify, make_response

#from astroprint.network import NetworkManager
#from .astroprint.network import NetworkManager
from octoprint_WBCustom.astroprint.network.manager import networkManager

class WBCustomApi(octoprint.plugin.BlueprintPlugin):
    @octoprint.plugin.BlueprintPlugin.route("/echo", methods=["GET"])
    def myEcho(self):
        if not "text" in request.values:
            return make_response("Expected a text to echo back.", 400)
        return request.values["text"]

    #@api.route("/settings/network/wifi-networks", methods=["GET"])
    @octoprint.plugin.BlueprintPlugin.route("/wifi", methods=["GET"])
    def getNetworkSettings(self):

        nm = networkManager()

        return jsonify({
            'networks': nm.getActiveConnections(),
            'networkDeviceInfo': nm.networkDeviceInfo,
            'hasWifi': nm.hasWifi(),
            'storedWifiNetworks': nm.storedWifiNetworks()

        })

    #@api.route("/settings/network/wifi-networks", methods=["GET"])
    @octoprint.plugin.BlueprintPlugin.route("/wifi-networks", methods=["GET"])
    def getWifiNetworks():
        networks = networkManager().getWifiNetworks()

        if networks:
            return jsonify(networks = networks)
        else:
            return jsonify({'message': "Unable to get WiFi networks"})

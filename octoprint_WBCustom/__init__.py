# -*- coding: utf-8 -*-
from __future__ import absolute_import, unicode_literals

import octoprint.plugin

from .api import WBCustomApi
from .api.astroprint.api import WBCustomAstroPrintApi

class WBCustomPlugin(octoprint.plugin.StartupPlugin,
                       octoprint.plugin.TemplatePlugin,
                       WBCustomApi,
					   WBCustomAstroPrintApi):
    def on_after_startup(self):
        self._logger.info("WBCustomPlugin!")

__plugin_name__ = "WB Custom"
__plugin_version__ = "1.0.0"
__plugin_description__ = "Plugin da empresa WB"
__plugin_pythoncompat__ = ">=2.7,<4"
__plugin_implementation__ = WBCustomPlugin()

# -*- coding: utf-8 -*-
#------------------------------------------------------------
# PalcoTV Regex de 9straem
# Version 0.1 (17.10.2014)
#------------------------------------------------------------
# License: GPL (http://www.gnu.org/licenses/gpl-3.0.html)
# Gracias a la librería plugintools de Jesús (www.mimediacenter.info)


import os
import sys
import urllib
import urllib2
import re
import shutil
import zipfile
import time

import xbmc
import xbmcgui
import xbmcaddon
import xbmcplugin

import plugintools
import json


home = xbmc.translatePath(os.path.join('special://home/addons/plugin.video.palcotv-wip/', ''))
tools = xbmc.translatePath(os.path.join('special://home/addons/plugin.video.palcotv-wip/resources/tools', ''))
addons = xbmc.translatePath(os.path.join('special://home/addons/', ''))
resources = xbmc.translatePath(os.path.join('special://home/addons/plugin.video.palcotv-wip/resources', ''))
art = xbmc.translatePath(os.path.join('special://home/addons/plugin.video.palcotv-wip/art', ''))
tmp = xbmc.translatePath(os.path.join('special://home/addons/plugin.video.palcotv-wip/tmp', ''))
playlists = xbmc.translatePath(os.path.join('special://home/addons/playlists', ''))

icon = art + 'icon.png'
fanart = 'fanart.jpg'

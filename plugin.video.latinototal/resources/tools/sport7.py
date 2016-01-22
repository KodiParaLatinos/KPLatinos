# -*- coding: utf-8 -*-
#------------------------------------------------------------
# PalcoTV Parser de Arenavision
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


home = xbmc.translatePath(os.path.join('special://home/addons/plugin.video.palcotv/', ''))
tools = xbmc.translatePath(os.path.join('special://home/addons/plugin.video.palcotv/resources/tools', ''))
addons = xbmc.translatePath(os.path.join('special://home/addons/', ''))
resources = xbmc.translatePath(os.path.join('special://home/addons/plugin.video.palcotv/resources', ''))
art = xbmc.translatePath(os.path.join('special://home/addons/plugin.video.palcotv/art', ''))
tmp = xbmc.translatePath(os.path.join('special://home/addons/plugin.video.palcotv/tmp', ''))
playlists = xbmc.translatePath(os.path.join('special://home/addons/playlists', ''))

icon = art + 'icon.png'
fanart = 'fanart.jpg'


def arenavision_parser(params):
    plugintools.log("[PalcoTV-0.3.0].arenavision_parser "+repr(params))
    
    url = params.get("url")
    thumbnail = params.get("thumbnail")
    title = params.get("title")
    plugintools.log("title= "+title)
    data = plugintools.read(url)
    plugintools.add_item(action="" , title=title, url=url, thumbnail=thumbnail , fanart='http://wallpaper-download.net/wallpapers/football-wallpapers-football-stadium-wallpaper-wallpaper-36537.jpg' , folder = False, isPlayable = False)
    params["fanart"]=fanart
    plugintools.log("fanart= "+fanart)
    matches = plugintools.find_multiple_matches(data, '<li><a href=(.*?)>(.*?)</a></li>')    
    for url, title in matches:
        url = url.replace("'", "")
        if title.startswith("AV") == True:
            parse_av_channel(title, url, params)


def parse_av_channel(title, url, params):
    plugintools.log("[PalcoTV-0.3.0].parse_av_channel "+repr(params))
    
    data = plugintools.read(url)
    fanart = params.get("fanart")
    plugintools.log("fanart= "+fanart)    
    thumbnail = params.get("thumbnail")
    url = plugintools.find_single_match(data, 'sop://(.*?)>')
    url = url.replace('"', "").strip()
    if url == "":
        plugintools.add_item(action="play" , title=title + ' [COLOR red]OFF[/COLOR]', url=url, thumbnail=thumbnail , fanart='http://wallpaper-download.net/wallpapers/football-wallpapers-football-stadium-wallpaper-wallpaper-36537.jpg' , folder = False, isPlayable = True)                       
    else:
        url = 'sop://' + url
        url = 'plugin://plugin.video.p2p-streams/?url=' + url + '&mode=2&name=' + title        
        plugintools.add_item(action="play" , title=title, url=url, thumbnail=thumbnail , fanart='http://wallpaper-download.net/wallpapers/football-wallpapers-football-stadium-wallpaper-wallpaper-36537.jpg' , folder = False, isPlayable = True)

    
    

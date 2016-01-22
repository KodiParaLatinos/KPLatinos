# -*- coding: utf-8 -*-
#------------------------------------------------------------
# PalcoTV Parser de Sport7.ru
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


def sportseven(params):
    plugintools.log("[PalcoTV-0.3.0].sport7.ru "+repr(params))

    plugintools.add_item(action="", title='[COLOR white]s p o r t[COLOR red][B] 7[/B][/COLOR] . r u[/COLOR]' , url="", thumbnail = "http://sport7.ru/images/sport_logo.png" , fanart = "http://2.cdn.nhle.com/lightning/v2/ext/wallpaper/arena_fans_wallpaper_1680x1050.jpg" , folder=False, isPlayable=False)
    
    data = plugintools.read(params.get("url"))
    plugintools.log("data= "+data)
    matches = plugintools.find_single_match(data, 'class=\"head-match\"(.*?)class=\"mar-top5 jus\"')
    plugintools.log("matches= "+matches)
    title = plugintools.find_multiple_matches(matches, '<h2>(.*?)</h2>')
    for entry in title:
        canal = plugintools.find_single_match(matches, '<h2>'+entry+'(.*?)class=\"com_bl utext\"')
        plugintools.log("canal= "+canal)
        title = convertrus(entry)
        bitrate = plugintools.find_single_match(canal, '<div class=\"rc\">(.*?)</div>')
        url_p2p = plugintools.find_single_match(canal, 'sop://(.*?)\',')
        if url_p2p == "":
            url_p2p = plugintools.find_single_match(canal, 'acestream://(.*?)\'')
            url = 'plugin://plugin.video.p2p-streams/?url=acestream://' + url_p2p + '&mode=1&name='
            url = url.strip()
            plugintools.log("URL_Acestream= "+url)
            title = '[COLOR lightyellow]' + title + '  [/COLOR][COLOR lightblue] [Acestream] [/COLOR][COLOR green]['+bitrate+'][/COLOR]'
            plugintools.add_item(action="play", title=title, url=url, thumbnail = "http://sport7.ru/images/sport_logo.png", fanart = "http://2.cdn.nhle.com/lightning/v2/ext/wallpaper/arena_fans_wallpaper_1680x1050.jpg" , folder = False, isPlayable = False)
        else:
            url = 'plugin://plugin.video.p2p-streams/?url=sop://' + url_p2p + '&mode=2&name='
            url = url.strip()
            plugintools.log("URL_Sopcast= "+url)
            title = '[COLOR lightyellow]' + title + '  [/COLOR][COLOR darkorange] [Sopcast] [/COLOR][COLOR green]['+bitrate+'][/COLOR]'
            plugintools.add_item(action="play", title=title, url=url, folder = False, thumbnail = "http://sport7.ru/images/sport_logo.png", fanart = "http://2.cdn.nhle.com/lightning/v2/ext/wallpaper/arena_fans_wallpaper_1680x1050.jpg", isPlayable = False)


def convertrus(title):
    plugintools.log("[PalcoTV 0.3.0].convertrus "+title)

    title = title.strip()

    if title == "КХЛ ТВ":
        title = 'KHL HD'
    if title == 'Трансляции матчей КХЛ':
        title = 'KHL (Hockey hielo)'
    if title == 'Трансляции матчей НХЛ':
        title = 'KHL (Hockey hielo)'
    if title.find("футбол") >= 0:
        title = title.replace("футбол", "Fútbol")

    return title        
  

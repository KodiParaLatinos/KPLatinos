# -*- coding: utf-8 -*-
#------------------------------------------------------------
# PalcoTV Regex de 1torrent.ru
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

import xbmc
import xbmcgui
import xbmcaddon
import xbmcplugin

import plugintools


home = xbmc.translatePath(os.path.join('special://home/addons/plugin.video.palcotv/', ''))
tools = xbmc.translatePath(os.path.join('special://home/addons/plugin.video.palcotv/resources/tools', ''))
addons = xbmc.translatePath(os.path.join('special://home/addons/', ''))
resources = xbmc.translatePath(os.path.join('special://home/addons/plugin.video.palcotv/resources', ''))
art = xbmc.translatePath(os.path.join('special://home/addons/plugin.video.palcotv/art', ''))
tmp = xbmc.translatePath(os.path.join('special://home/addons/plugin.video.palcotv/tmp', ''))
playlists = xbmc.translatePath(os.path.join('special://home/addons/playlists', ''))

icon = art + 'icon.png'
fanart = 'fanart.jpg'



def torrentone(params):
    plugintools.log("[PalcoTV-0.3.0].Playlist Sport Channels Torrent1( "+repr(params))
    plugintools.add_item(action="", title = '[B][I][COLOR lightyellow]1torrent.tv Acestream Sports Playlist[/B][/I][/COLOR]', url = "", thumbnail = 'http://1torrent.tv/images/header_logo.png' , fanart = 'http://hdwallpappers.com/images/wallpapers/Allianz-Arena-Stadium-wallpaper.jpg' , folder = True, isPlayable = False)    

    url = params.get("url")
    thumbnail = params.get("thumbnail")
    fanart = params.get("fanart")
    title = params.get("title")
    plugintools.log("title= "+title)
    data = plugintools.read(url)
    plugintools.log("data= "+data)
    match = plugintools.find_single_match(data, 'tcon_6(.*?)</a></div></div></div></div>')
    plugintools.log("match sports= "+match)
    matches = plugintools.find_multiple_matches(match, '<a href="(.*?)</a>(.*?)</a>')

    for winy, xiny in matches:
        plugintools.log("winy= "+winy)
        plugintools.log("xiny= "+xiny)
        winy = winy.split("><")
        url = 'http://1torrent.tv' + winy[0]
        url = url.replace('"', "")
        thumbnail = 'http://1torrent.tv/images/header_logo.png'
        title = xiny.split(">")
        title = title[3]
        plugintools.log("title= "+title)
        plugintools.log("url= "+url)
        plugintools.log("thumbnail= "+thumbnail)
        plugintools.add_item(action="gethash_torrentone" , title = title, url = url , thumbnail = thumbnail , fanart = 'http://hdwallpappers.com/images/wallpapers/Allianz-Arena-Stadium-wallpaper.jpg' , isPlayable = True, folder = False)

        
def gethash_torrentone(params):
    plugintools.log("[PalcoTV-0.3.0].gethash_torrentone( "+repr(params))

    url = params.get("url")
    data = plugintools.read(url)
    plugintools.log("data= "+data)
    match = plugintools.find_single_match(data, 'this.loadPlayer\(\"(.*?)\n')
    match = match.replace('",{autoplay: true});', "")
    match = match.replace('}', "")
    match = match.strip()
    plugintools.log("match= "+match)
    title = params.get("title")
    title = title.strip()
    title_fixed = title.replace(" ", "+")
    url = 'plugin://plugin.video.p2p-streams/?url=' + match + '&mode=1&name=' + title_fixed
    plugintools.log("url= "+url)
    plugintools.play_resolved_url(url)
    

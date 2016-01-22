# -*- coding: utf-8 -*-
#------------------------------------------------------------
# PalcoTV Regex de vercosasgratis.com
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


# Función que guía el proceso de elaboración de la URL original
def vercosas(params):
    plugintools.log("[PalcoTV-0.3.0].Vercosasgratis "+repr(params))
    url_user = {}
    url_user["token"]='#ed%h0#w@12Fuck'
    
    # Construimos diccionario...
    url = params.get("url")
    url_extracted = url.split(" ")
    for entry in url_extracted:
        if entry.startswith("rtmp"):
            entry = entry.replace("rtmp=", "")         
            url_user["rtmp"]=entry
        elif entry.startswith("playpath"):
            entry = entry.replace("playpath=", "")
            url_user["playpath"]=entry            
        elif entry.startswith("swfUrl"):
            entry = entry.replace("swfUrl=", "")
            url_user["swfurl"]=entry
        elif entry.startswith("pageUrl"):
            entry = entry.replace("pageUrl=", "")
            url_user["pageurl"]=entry          
        elif entry.startswith("referer"):
            entry = entry.replace("referer=", "")
            url_user["referer"]=entry

    plugintools.log("URL_user dict= "+repr(url_user)) 
    pageurl = url_user.get("pageurl")
    referer = url_user.get("referer")
    
    body = gethttp_headers(pageurl, referer)
    getparams_vercosas(url_user, body)



# Vamos a hacer una llamada al pageUrl
def gethttp_headers(pageurl, referer):
      
    request_headers=[]
    request_headers.append(["User-Agent","Mozilla/5.0 (Macintosh; Intel Mac OS X 10_8_3) AppleWebKit/537.31 (KHTML, like Gecko) Chrome/26.0.1410.65 Safari/537.31"])
    request_headers.append(["Referer",referer])
    body,response_headers = plugintools.read_body_and_headers(pageurl, headers=request_headers)      
    plugintools.log("body= "+body)
    return body           

    

def getparams_vercosas(url_user, body):
    plugintools.log("[PalcoTV-0.3.0].getparams_vercosas " + repr(url_user) )

    # Obtenemos la URL del rtmp y el playpath
    streamer = re.compile('streamer\', \'(.*?)\'\);\n').findall(body)
    streamer = streamer[0]
    playpath = re.compile('file\', \'(.*?)\'\);\n').findall(body)
    playpath = playpath[0]
    playpath = playpath.replace("['", "")
    playpath = playpath.replace("']", "")
    print streamer
    print playpath
    url_user["rtmp"]=streamer
    url_user["playpath"]=playpath    
    url = url_user.get("rtmp") + ' playpath=' + url_user.get("playpath") + ' swfUrl=http://vercosasgratis.com/player.swf token=' + url_user.get("token") + ' pageUrl=http://vercosasgratis.com live=1 timeout=15'
    plugintools.play_resolved_url(url)


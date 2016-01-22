# -*- coding: utf-8 -*-
#------------------------------------------------------------
# PalcoTV Regex de vaughnlive
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
import time


home = xbmc.translatePath(os.path.join('special://home/addons/plugin.video.palcotv/', ''))
tools = xbmc.translatePath(os.path.join('special://home/addons/plugin.video.palcotv/resources/tools', ''))
addons = xbmc.translatePath(os.path.join('special://home/addons/', ''))
resources = xbmc.translatePath(os.path.join('special://home/addons/plugin.video.palcotv/resources', ''))
art = xbmc.translatePath(os.path.join('special://home/addons/plugin.video.palcotv/art', ''))
tmp = xbmc.translatePath(os.path.join('special://home/addons/plugin.video.palcotv/tmp', ''))
playlists = xbmc.translatePath(os.path.join('special://home/addons/playlists', ''))

icon = art + 'icon.png'
fanart = 'fanart.jpg'


def resolve_vaughnlive(params):
    plugintools.log("[PalcoTV-0.3.0].resolve_vaughnlive " + repr(params) )

    vaughnlive_user = {"rtmp": "" , "swfurl": "http://vaughnlive.tv/800021294/swf/VaughnSoftPlayer.swf" , "pageurl": "http://www.vaughnlive.tv/", "token":'#ed%h0#w18623jsda6523l'}

    # Construimos diccionario 'vaughn_user'
    url = params.get("url")
    url = url.strip()
    url_extracted = url.split(" ")
    for entry in url_extracted:
        if entry.startswith("rtmp"):
            entry = entry.replace("rtmp=", "")         
            vaughnlive_user["rtmp"]=entry
        elif entry.startswith("playpath"):
            entry = entry.replace("playpath=", "")
            vaughnlive_user["playpath"]=entry            
        elif entry.startswith("swfUrl"):
            entry = entry.replace("swfUrl=", "")
            vaughnlive_user["swfurl"]=entry
        elif entry.startswith("pageUrl"):
            entry = entry.replace("pageUrl=", "")
            vaughnlive_user["pageurl"]=entry
        elif entry.startswith("token"):
            entry = entry.replace("token=", "")
            vaughnlive_user["token"]=entry           
            
    # rtmp://50.7.78.138:443/live?kbjjHcUi6bZPicNvuKX5IxlcdGBj1HXm playpath=live_psntv_espnd11 live=1 timeout=20
    # rtmp://192.240.105.42:443live?V79PxK0XPeKslBL1dsbHTI6LWwNTop36 playpath=live_psntv_espnd11 live=1 timeout=20
    
    
    pageurl = vaughnlive_user.get("pageurl")
    body = gethttp_noref(pageurl)
    #plugintools.log("body= "+body)
    body = body.strip()
    plugintools.log("body= "+body)

    # Obtenemos token
    token = plugintools.find_single_match(body, 'vsVars.*= \"0m0(.*?)\"')
    plugintools.log("token= "+token)
    getedge = plugintools.find_single_match(body, '{ return \"(.*?)\"')
    getedge = getedge.split(",")
    getedge = getedge[0]
    plugintools.log("getedge= "+getedge)    
    url = 'rtmp://'+getedge+'/live?'+token+ ' playpath='+vaughnlive_user.get("playpath")+' live=1 timeout=20'
    print 'url',url
    plugintools.play_resolved_url(url)


def gethttp_noref(url):
    plugintools.log("[PalcoTV-0.3.0.Vaughn_Regex] ")    

    request_headers=[]
    request_headers.append(["User-Agent","Mozilla/5.0 (Macintosh; Intel Mac OS X 10_8_3) AppleWebKit/537.31 (KHTML, like Gecko) Chrome/26.0.1410.65 Safari/537.31"])
    body,response_headers = plugintools.read_body_and_headers(url, headers=request_headers)
    return body
    

# -*- coding: utf-8 -*-
#------------------------------------------------------------
# PalcoTV - XBMC Add-on by Juarrox (juarrox@gmail.com)
# Version 0.2.9 (18.07.2014)
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



def resolve_iguide(params):
    plugintools.log("[PalcoTV-0.3.0].resolve_iguide " + repr(params) )

    url = params.get("url")
    url = url.strip()
    # plugintools.log("URL antes de resolver= " + url)

    iguide_palco = {"rtmp": "rtmp://live2.iguide.to/redirect","swfurl": "http://cdn1.iguide.to/player/secure_player_iguide_embed_token.swf" , "pageurl": "http://www.iguide.to/", "token":'#ed%h0#w18623jsda6523lDGD'}
    iguide_user = {"rtmp": "","swfurl": "" , "pageurl": "", "token":""}

    url_extracted = url.split(" ")
    for entry in url_extracted:
        if entry.startswith("rtmp"):
            entry = entry.replace("rtmp=", "")
            entry = entry.replace("rtmp://$OPT:rtmp-raw=", "")            
            iguide_user["rtmp"]=entry
        elif entry.startswith("playpath"):
            entry = entry.replace("playpath=", "")
            iguide_user["playpath"]=entry            
        elif entry.startswith("swfUrl"):
            entry = entry.replace("swfUrl=", "")
            iguide_user["swfurl"]=entry
        elif entry.startswith("pageUrl"):
            entry = entry.replace("pageUrl=", "")
            iguide_user["pageurl"]=entry
        elif entry.startswith("token"):
            entry = entry.replace("token=", "")
            iguide_user["token"]=entry           
            
    if url.endswith("Conn=S:OK") == True:
        # plugintools.log("No tiene sufijo. Lo añadimos... ")        
        url = url.replace("Conn=S:OK", "")
        
    if url.startswith("rtmp://$OPT") == True:
        # plugintools.log("No tiene prefijo. Lo añadimos... ")
        url = url.replace("rtmp://$OPT:rtmp-raw=", "")

    plugintools.log("URL Iguide= " + url)
    params["url"] = url
    play_iguide(iguide_palco, iguide_user)



def resolve_ucaster(params):
    plugintools.log("[PalcoTV-0.3.0].resolve_ucaster " + repr(params) )

    url = params.get("url")
    url = url.strip()
    plugintools.log("URL antes de resolver= " + url)
    
    if url.endswith("Conn=S:OK") == False:
        plugintools.log("No tiene sufijo. Lo añadimos... ")        
        url = url + " Conn=S:OK"
        
    if url.startswith("rtmp://$OPT") == True:
        plugintools.log("No tiene prefijo. Lo añadimos... ")
        url = "rtmp://$OPT:rtmp-raw=" + url
        

    plugintools.log("URL Ucaster= " + url)
    params["url"] = url
    return params


def play_iguide(iguide_palco, iguide_user):
    plugintools.log("[PalcoTV-0.3.0].iGuide PalcoTV= " + repr(iguide_palco) )
    plugintools.log("[PalcoTV-0.3.0].iGuide User= " + repr(iguide_user) )

    playlist = xbmc.PlayList( xbmc.PLAYLIST_VIDEO )
    playlist.clear()
    
    url = iguide_user.get("rtmp") + " playpath=" + iguide_user.get("playpath") + " swfUrl=" + iguide_user.get("swfurl") + " live=1 pageUrl=" + iguide_user.get("pageurl") + " token=" + iguide_user.get("token")
    url_user = iguide_user.get("rtmp") + " playpath=" + iguide_user.get("playpath") + " swfUrl=" + iguide_user.get("swfurl") + " live=1 pageUrl=" + iguide_user.get("pageurl") + " token=" + iguide_user.get("token")
    url_palco = iguide_palco.get("rtmp") + " playpath=" + iguide_user.get("playpath") + " swfUrl=" + iguide_palco.get("swfurl") + " live=1 pageUrl=" + iguide_user.get("pageurl") + " token=" + iguide_palco.get("token")
    url_refixed = iguide_palco.get("rtmp") + " playpath=" + iguide_user.get("playpath") + " swfUrl=" + iguide_palco.get("swfurl") + " live=1 pageUrl=" + iguide_palco.get("pageurl") + " token=" + iguide_palco.get("token") + " Conn=S:OK"
    
    msg = "Resolviendo enlace ... "
    xbmc.executebuiltin("Notification(%s,%s,%i,%s)" % ('PalcoTV', msg, 3 , art+'icon.png'))  

    playlist.add(url_user)
    plugintools.log("[PalcoTV 0.2.87b playing URL playlist... "+url_palco)
    playlist.add(url_palco)
    plugintools.log("[PalcoTV 0.2.87b fixing URL by PalcoTV... "+url_refixed)
    playlist.add(url_refixed)
    plugintools.log("[PalcoTV 0.2.87b parsing URL... "+url_user)
    # xbmc.Player( xbmc.PLAYER_CORE_MPLAYER ).play(playlist)
        

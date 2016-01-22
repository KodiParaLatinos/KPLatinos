# -*- coding: utf-8 -*-
#------------------------------------------------------------
# PalcoTV Parser de laligatv.es
# Version 0.1 (18.10.2014)
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


def laligatv(params):
    plugintools.log("[PalcoTV-0.3.0].laligatv.es Playlist Sport Channels( "+repr(params))

    thumbnail = params.get("thumbnail")
    plugintools.log("thumbnail= "+thumbnail)
   
    plugintools.add_item(action="", title = '[B][I][COLOR darkviolet]LALIGATV.ES[/B][/I][/COLOR]', url = "", thumbnail = 'http://files.lfp.es/201402/640x360_06172611noticia-la-liga-tv.es.jpg' , fanart = 'https://fbcdn-sphotos-b-a.akamaihd.net/hphotos-ak-ash3/556377_550288405007723_1790184113_n.jpg' , folder = True, isPlayable = False)
    plugintools.add_item(action="", title = '[B][I][COLOR white]Las emisiones comenzarán 15 minutos antes de cada partido[/B][/I][/COLOR]', url = "", thumbnail = 'http://files.lfp.es/201402/640x360_06172611noticia-la-liga-tv.es.jpg' , fanart = 'https://fbcdn-sphotos-b-a.akamaihd.net/hphotos-ak-ash3/556377_550288405007723_1790184113_n.jpg' , folder = True, isPlayable = False)
    
    url = params.get("url")
    thumbnail = params.get("thumbnail")
    fanart = params.get("fanart")
    title = params.get("title")
    plugintools.log("title= "+title)
    data = plugintools.read(url)
    match_total = plugintools.find_single_match(data, 'id=\"coming-soon\"(.*?)fb-root')
    plugintools.log("match_total= "+match_total)
    matches_dia = plugintools.find_single_match(data, 'id=\"coming-soon\"(.*?)</div></div>')
    plugintools.log("matches_dia= "+matches_dia) 
    jornada = plugintools.find_multiple_matches(match_total, 'class=\"title_jornada\">(.*?)</div>')
    #print 'jornada',jornada       
    matches = plugintools.find_multiple_matches(matches_dia, '<a href="(.*?)</a>')
    plugintools.add_item(action="" , title = '[COLOR lavender][B]' + jornada[0] + '[/B][/COLOR]' , thumbnail = thumbnail , folder = False , isPlayable = False)
    
    for entry in matches:
        plugintools.log("entry= "+entry)
        url_partido = entry.split('"')
        url_partido = url_partido[0]
        url_partido = url_partido.strip()
        plugintools.log("url_partido= "+url_partido)
        hora = plugintools.find_single_match(entry, 'hora_partido_otras_competiciones\">(.*?)</span>')
        plugintools.log("hora= "+hora)
        local = plugintools.find_single_match(entry, 'equipo_local_otras_competiciones\">(.*?)</span>')
        visitante = plugintools.find_single_match(entry, 'equipo_visitante_otras_competiciones\">(.*?)</span>')
        plugintools.log("local= "+local)
        plugintools.log("viistante= "+visitante)
        plugintools.add_item(action="adelante_geturl" , title = '[COLOR lightyellow][B](' + hora + ')[/B][/COLOR][COLOR white] ' + local + ' - ' + visitante + ' [/COLOR]' , url = url_partido , thumbnail = params.get("thumbnail") , folder = False , isPlayable = True)

    if len(jornada) >= 2:
        plugintools.add_item(action="" , title = '[COLOR lavender][B]' + jornada[1] + '[/B][/COLOR]' , thumbnail = thumbnail , folder = False , isPlayable = False)
        matches_dia = plugintools.find_single_match(match_total, jornada[1]+'(.*?)</div></div>')
        plugintools.log("matches_dia= "+matches_dia)
        matches = plugintools.find_multiple_matches(matches_dia, '<a href="(.*?)</a>')
        for entry in matches:
            plugintools.log("entry= "+entry)
            url_partido = entry.split('"')
            url_partido = url_partido[0]
            url_partido = url_partido.strip()
            plugintools.log("url_partido= "+url_partido)
            hora = plugintools.find_single_match(entry, 'hora_partido_otras_competiciones\">(.*?)</span>')
            plugintools.log("hora= "+hora)
            local = plugintools.find_single_match(entry, 'equipo_local_otras_competiciones\">(.*?)</span>')
            visitante = plugintools.find_single_match(entry, 'equipo_visitante_otras_competiciones\">(.*?)</span>')
            plugintools.log("local= "+local)
            plugintools.log("viistante= "+visitante)
            plugintools.add_item(action="adelante_geturl" , title = '[COLOR lightyellow][B](' + hora + ')[/B][/COLOR][COLOR white] ' + local + ' - ' + visitante + ' [/COLOR]' , url = url_partido , thumbnail = params.get("thumbnail") , folder = False , isPlayable = True)       
    
        
               


def adelante_geturl(params):
    plugintools.log("[PalcoTV-0.3.0].LaLigatv.es getURL: "+repr(params))

    data = plugintools.read(params.get("url"))
    plugintools.log("data= "+data)
    url = plugintools.find_single_match(data, 'src: escape\(\"(.*?)\"')    
    plugintools.log("URL= "+url)
    plugintools.play_resolved_url(url)
        
        

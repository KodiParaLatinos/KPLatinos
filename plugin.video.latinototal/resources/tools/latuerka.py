# -*- coding: utf-8 -*-
#------------------------------------------------------------
# PalcoTV Parser de latuerka (Público TV)
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



def latuerka_menu(params):
    plugintools.log("[PalcoTV] La Tuerka Parser( "+repr(params))
    plugintools.add_item(action="", title = '[B][I][COLOR lightyellow]LaTuerka Videos[/B][/I][/COLOR]', url = "", folder = True, isPlayable = False)

    url = params.get("url")
    data = plugintools.read(url)
    #plugintools.log("data= "+data)
    menu = plugintools.find_single_match(data, '<ul class="menu-tuerka">(.*?)</ul>')
    #plugintools.log("menu_latuerka= "+menu)
    items_menu = plugintools.find_multiple_matches(menu, '<a href=([^<]+)</a>')

    for entry in items_menu:
        #plugintools.log("item= "+entry)
        entry = entry.split(">")
        url_program = entry[0]
        title_program = entry[1]
        url_program = url_program.replace('"', "")
        url_program = 'http://www.publico.es' + url_program
        plugintools.log("title_program= "+title_program)
        plugintools.log("url_program= "+url_program)
        plugintools.add_item(action="program_capis" , title = title_program , url = url_program , thumbnail = 'http://www.latuerka.net/img/logo.png' , fanart = 'http://www.latuerka.net/img/bg.jpg' , folder = True , isPlayable = False)


def program_capis(params):
    plugintools.log("[PalcoTV-0.3.0].LaTuerka Videos"+repr(params))
    fanart = params.get("extra")

    data = plugintools.read(params.get("url"))
    #plugintools.log("data= "+data)

    #<a href="/publico-tv/program/59/video/216146/otra-vuelta-de-tuerka-jesus-cintora" class="play"><span>Reproducir</span></a>
    items_programa = plugintools.find_multiple_matches(data, '<div class="thumb">(.*?)</li>')

    for entry in items_programa:
        plugintools.log("items_programa= "+entry)
        url_programa = plugintools.find_single_match(entry, '<a href=\"(.*?)\"')
        img_programa = plugintools.find_single_match(entry, '<img src=\"(.*?)\"')
        title_programa = plugintools.find_single_match(entry, 'title="">(.*?)</a></p>')
        title_programa = title_programa.split('title="">')
        title_programa = title_programa[1]
        title_programa = title_programa.replace("&ntilde;", "ñ")
        #url_programa = plugintools.find_multiple_matches(entry, '<a href=(.*?)class=\"foto')
        url_programa = 'http://www.publico.es' + url_programa
        plugintools.log("url_programa= "+url_programa)
        url = tuerka_link(url_programa)
        plugintools.log("img_programa= "+img_programa)
        plugintools.log("title_programa= "+title_programa)
        plugintools.add_item(action="play", title = title_programa, url = url , thumbnail = img_programa, fanart = 'http://www.latuerka.net/img/bg.jpg' , folder = False , isPlayable = True)



def tuerka_link(url_programa):
    plugintools.log("[PalcoTV-0.3.0].LaTuerka Link " + url_programa)

    data = plugintools.read(url_programa)
    plugintools.log("data= "+data)
    url = plugintools.find_single_match(data, 'stream\:\'(.*?)\',')
    plugintools.log("url= "+url)
    return url
                            
    

    
    

        
        
        
        

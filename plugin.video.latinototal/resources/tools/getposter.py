# -*- coding: utf-8 -*-
#------------------------------------------------------------
# PalcoTV GetPoster (módulo de descarga de posters de películas)
# Version 0.1 (02.11.2014)
#------------------------------------------------------------
# License: GPL (http://www.gnu.org/licenses/gpl-3.0.html)
# Gracias a la librería plugintools de Jesús (www.mimediacenter.info)

# TODO:
# Crear botones de paginación y función de lectura de resultados por páginas: getresults(url)
# Mostrar un multilink con las páginas de resultados. El botón tendría de título: "Ir a la página..."
# Buscar alguna forma (si es posible) de mostrar los thumbnails
# Eliminar logs


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

import re,urllib,urllib2,sys
import plugintools,ioncube


home = xbmc.translatePath(os.path.join('special://home/addons/plugin.video.latinototal/', ''))
art = xbmc.translatePath(os.path.join('special://home/addons/plugin.video.latinototal/art', ''))
tmp = xbmc.translatePath(os.path.join('special://home/addons/plugin.video.latinototal/tmp', ''))
playlists = xbmc.translatePath(os.path.join('special://home/addons/playlists', ''))

icon = art + 'icon.png'
fanart = 'fanart.jpg'

def getposter(title):
    plugintools.log("GetPoster "+title)
   
    try:
        datamovie = {}
        title = title.lower().strip().replace(" ", "+")
        url = 'http://m.imdb.com/find?q='+title
        referer= 'http://m.imdb.com/'
        data = gethttp_referer_headers(url, referer)
        match_movie = plugintools.find_single_match(data, '<div class="title">(.*?)</div>')
        movie_url = plugintools.find_single_match(match_movie, '<a href="([^"]+)')
        movie_url = 'http://m.imdb.com/'+movie_url
        body = gethttp_referer_headers(movie_url,referer)
        poster_url = plugintools.find_single_match(body, '<link rel=\'image_src\' href="([^"]+)')
        datamovie["Poster"] = poster_url.strip()
    except:
        datamovie["Poster"] = ""

    themoviedb(title, datamovie)
    return datamovie      
        




def save_title(title, datamovie, filename):
    plugintools.log("Arena+ Saving data... "+repr(datamovie))

    # Abrimos archivo para guardar datos de película
    plugintools.log("Abriendo archivo... tmp/"+filename)
    imdb_file = open(tmp + filename, "a")
    title = title.strip()   
    imdb_file.write('#EXTINF:-1,'+title+',tvg-logo="'+datamovie["Poster"]+'",tvg-wall="'+datamovie["Fanart"]+'"\n')
    imdb_file.close()


def save_url(url, filename):
    plugintools.log("Arena+ Saving URL...")

    # Abrimos archivo para guardar datos de película
    plugintools.log("Abriendo archivo... tmp/"+filename)
    imdb_file = open(tmp + filename, "a")
    imdb_file.write(url+'\n\n')
    if url == "":
        imdb_file.write('\n')
    imdb_file.close()    

  

def themoviedb(title, datamovie):
    plugintools.log("The Movie Database: "+title)

    try:
        url = 'https://www.themoviedb.org/search?query='+title
        plugintools.log("URL= "+url)
        referer = 'https://www.themoviedb.org/'
        data = gethttp_referer_headers(url,referer)
        matches = plugintools.find_single_match(data, '<ul class="search_results movie">(.*?)</ul>')
        title_film = plugintools.find_single_match(matches, 'title="([^"]+)')
        plugintools.log("title_film= "+title_film)
        url_film = plugintools.find_single_match(matches, '<a href="([^"]+)')
        url_film_fixed = url_film.split("-")
        if len(url_film_fixed) >= 2:
            url_film_fixed = url_film[0]
        else:
            url_film_fixed = url_film
        url_film = 'https://www.themoviedb.org'+url_film+'?language=es'
        url_film = url_film.strip()
        plugintools.log("url_film= "+url_film)
        request_headers=[]
        request_headers.append(["User-Agent","Mozilla/5.0 (Macintosh; Intel Mac OS X 10_8_3) AppleWebKit/537.31 (KHTML, like Gecko) Chrome/26.0.1410.65 Safari/537.31"])
        request_headers.append(["Referer", referer])
        body,response_headers = plugintools.read_body_and_headers(url_film, headers=request_headers)        
        plugintools.log("body= "+body)      
        backdrop = plugintools.find_single_match(body, '<meta name="twitter:image" content="([^"]+)')
        datamovie["Fanart"]=backdrop
        plugintools.log("backdrop= "+backdrop)
        
    except:
        pass
 

def gethttp_referer_headers(url,referer):
    request_headers=[]
    request_headers.append(["User-Agent","Mozilla/5.0 (Macintosh; Intel Mac OS X 10_8_3) AppleWebKit/537.31 (KHTML, like Gecko) Chrome/26.0.1410.65 Safari/537.31"])
    request_headers.append(["Referer", referer])
    body,response_headers = plugintools.read_body_and_headers(url, headers=request_headers)    
    return body



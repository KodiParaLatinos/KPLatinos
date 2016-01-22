# -*- coding: utf-8 -*-
#--------------------------------------------------------
#  creado por quequeQ para PalcoTV
# (http://forum.rojadirecta.es/member.php?1370946-quequeQ)
# (http://xbmcspain.com/foro/miembro/quequino/)
# Version 0.0.1 (26.10.2014)
#--------------------------------------------------------
# License: GPL (http://www.gnu.org/licenses/gpl-3.0.html)

import os,sys,urlparse,urllib,urllib2,re,shutil,zipfile

import xbmc,xbmcgui,xbmcaddon,xbmcplugin

import plugintools,unwise

art = xbmc.translatePath(os.path.join('special://home/addons/plugin.video.palcotv/art', ''))
playlists = xbmc.translatePath(os.path.join('special://home/addons/plugin.video.palcotv/playlists', ''))
tmp = xbmc.translatePath(os.path.join('special://home/addons/plugin.video.palcotv/tmp', ''))

icon = art + 'icon.png'
fanart = 'fanart.jpg'


def shsp(params):
	url = params.get("url")
	thumb = params.get("thumbnail")
	request_headers=[]
	request_headers.append(["User-Agent","Mozilla/4.0 (compatible; MSIE 5.01; Windows NT 5.0)"])
	body,response_headers = plugintools.read_body_and_headers(url, headers=request_headers)
	#os.environ["HTTP_PROXY"]=Proxy
	data=body
	#print "START="+params.get("url")
	import re
	p = re.compile(ur'(<a\sclass="mac".*?<\/div>)', re.DOTALL)
	matches = re.findall(p, data)
	#del matches[0]
	for match in matches:
		#url = scrapedurl.strip()
		#print match
		p = re.compile(ur'<img\ssrc=\'?"?([^\'"]+).*?<span\sclass="mactext">([^<]+).*?\s(<div.*?<\/div>)', re.DOTALL)
		links=re.findall(p, match)
		for imgs,titles,divs in links:
		 title=titles.replace("&nbsp; ","")
		 title=title.replace("&nbsp;","|")
		 #print divs
		 plugintools.add_item( action="shsp2" , title=title , url=divs ,thumbnail=thumb ,fanart=thumb , isPlayable=False, folder=True )
		 
def shsp2(params):
	divs = params.get("url")
	thumb = params.get("thumbnail")
	import re
	p = re.compile(ur'href=\'?"?([^\'"]+).*?>([^<]+)')
	link=re.findall(p, divs)
	#print link
	for lin in link:
	 url="http://showsport-tv.com"+lin[0].replace("/ch/","/update/").replace("php","html");
	 title=lin[1];print url+"\n"+title
	 plugintools.add_item( action="peaktv2" , title=title , url=url , isPlayable=True, folder=False )

def peaktv2(params):
	url = params.get("url")
	title = params.get("title")
	thumb = params.get("thumbnail")
	ref=url
	request_headers=[]
	request_headers.append(["User-Agent","Mozilla/4.0 (compatible; MSIE 5.01; Windows NT 5.0)"])
	body,response_headers = plugintools.read_body_and_headers(url, headers=request_headers)
	#os.environ["HTTP_PROXY"]=Proxy
	data=body
	#print "START="+data
	p = '<script type="text\/javascript">id="([^"]+).*?width="([^"]+).*?height="([^"]+).*?src="([^"]+)'
	matches = find_multiple_matches_multi(data,p)
	for id,width,height,cast in matches:
		url = 'http://xuscacamusca.se/?id='+id+'&width='+width+'&height='+height.strip()
		#print "START="+url
	request_headers=[]
	request_headers.append(["User-Agent","Mozilla/4.0 (compatible; MSIE 5.01; Windows NT 5.0)"])
	request_headers.append(["Referer",ref])
	body,response_headers = plugintools.read_body_and_headers(url, headers=request_headers)
	data=body
	#print "START="+data
	p='src=\'?"?([^\/]+)\/jwplayer\.js\.pagespeed'
	swf = plugintools.find_single_match(data,p)
	swf='http://xuscacamusca.se/'+swf+'/jwplayer.flash.swf'
	print "SWF = "+swf
	p = ';eval(.*?)<\/script>'
	mat = find_multiple_matches_multi(data,p)
	#print "wisenx="+mat[1]
	swfobj=mat[1]
	#print "swfobj="+swfobj
	decr = unwise.unwise_process(data)
	#print "DECR="+decr
	p = ",file:'(.*?)'"
	rtmp = plugintools.find_single_match(decr,p)
	print "PLPATH="+rtmp
	media_url = rtmp+' swfUrl='+swf+' live=1 timeout=15 swfVfy=1 pageUrl='+url
	#plugintools.add_item( action="play_resolved_url" , title=title , url=media_url ,thumbnail=thumb , isPlayable=True, folder=False )
	plugintools.play_resolved_url(media_url)
	print media_url

def pltptc(params):
    url = params.get("url")
    request_headers=[]
    request_headers.append(["User-Agent","Mozilla/4.0 (compatible; MSIE 5.01; Windows NT 5.0)"])
    body,response_headers = plugintools.read_body_and_headers(url, headers=request_headers)
    data=body
    print "START="+params.get("url")
    if params.get("title")=="PonTuCanal" :
	 pattern1 = 'popUp\(\'([^\']+).*src="([^"]+)'
	 pattern2 = "http://canalesgratis.me/canales/"
	 pattern3 = ".php"
    else :
	 pattern1 = 'popUp\(\'([^\']+).*src="([^"]+)'
	 pattern2 = "http://verdirectotv.com/canales/"
	 pattern3 = ".html"
    matches = find_multiple_matches_multi(data,pattern1)
    for scrapedurl, scrapedthumbnail in matches:
		#thumbnail = urlparse.urljoin( params.get("url") , scrapedthumbnail )
		thumbnail = scrapedthumbnail
		url = urlparse.urljoin( params.get("url") , scrapedurl.strip() )
		rep = str.replace(url,pattern2,"")
		title = str.replace(rep,pattern3,"").capitalize()
		plot = ""
		msg = "Resolviendo enlace ... "
		uri=url
		rref = 'http://verdirectotv.com/carrusel/tv.html'
		uri = uri+'@'+title+'@'+rref
		#plugintools.log("URI= "+uri)
		pattern = "\s+"
		import re
		uri = re.sub(pattern,'',uri)
		uri = uri.encode('base64')
		url = 'http://localhost/000/ptc2xbmc.php?page='+uri
		url = re.sub(pattern,'',url)
		plugintools.log("LSP URL= "+url)
		url = 'plugin://plugin.video.live.streamspro/?url='+plugintools.urllib.quote_plus(url)+'&mode=1&name='+plugintools.urllib.quote_plus(title)
		#plugintools.log("LINK= "+url)
		plugintools.add_item( action="runPlugin" , title=title , plot=plot , url=url ,thumbnail=thumbnail , isPlayable=False, folder=True )
	
def find_multiple_matches_multi(text,pattern):
    matches = re.findall(pattern,text, re.MULTILINE)
    return matches	

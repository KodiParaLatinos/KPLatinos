import urllib,urllib2,sys,re,xbmcplugin,xbmcgui,xbmcaddon,xbmc,os

AddonID ='plugin.video.kiddiecartoons'
fanart = xbmc.translatePath(os.path.join('special://home/addons/' + AddonID , 'fanart.jpg'))
icon = xbmc.translatePath(os.path.join('special://home/addons/' + AddonID, 'icon.png'))
  
def Menu():
    channelurl='http://hakancakiroglu.com/cizgifilm/cizgifilmlist_en3.php'
    link=Get_url(channelurl)
    match=re.compile('"id":"(.+?)",".+?":"(.+?)","resim":"(.+?)"').findall(link)
    for idno,name,thumb in match:
        if not 'Shazam' in name:
         if not 'Thundercats' in name:
          if not 'Friends 1' in name:
            thumb = thumb.replace('\/','/')
            name = name.replace('\n','').replace('\r','')
            name = '[COLOR gold]'+name+'[/COLOR]'
            addDir(name,idno,1,thumb,fanart)  
    xbmc.executebuiltin('Container.SetViewMode(500)')

def GetEpisodes(url):
    url = 'http://hakancakiroglu.com/cizgifilmler/'+url+'.json'
    link=Get_url(url)
    match=re.compile('"author":".+?","video":{"id":"(.+?)","uploaded":".+?","updated":".+?","uploader":".+?","category":".+?","title":"(.+?)"').findall(link)
    for ytid,name in match:
        thumb = 'http://i.ytimg.com/vi/'+ytid+'/default.jpg'
        if not 'Private video' in name:
            if not 'Deleted' in name:
                playback_url = 'plugin://plugin.video.youtube/?action=play_video&videoid=%s' % ytid
                print playback_url
                addLink(name,playback_url,100,thumb,fanart)  
    xbmc.executebuiltin('Container.SetViewMode(500)')

def Get_url(url):
    req = urllib2.Request(url)
    req.add_header('User-Agent', 'Apache-HttpClient/UNAVAILABLE (java 1.4)')
    response = urllib2.urlopen(req)
    link=response.read()
    response.close()
    return link
    
def Play(name,url):  
    ok=True
    liz=xbmcgui.ListItem(name, iconImage=icon,thumbnailImage=icon); liz.setInfo( type="Video", infoLabels={ "Title": name } )
    ok=xbmcplugin.addDirectoryItem(handle=int(sys.argv[1]),url=url,listitem=liz)
    xbmc.Player().play(url, liz, False)
    return ok

def addLink(name,url,mode,iconimage,fanart,description=''):
        u=sys.argv[0]+"?url="+urllib.quote_plus(url)+"&mode="+str(mode)+"&name="+urllib.quote_plus(name)+"&description="+str(description)
        ok=True
        liz=xbmcgui.ListItem(name, iconImage="DefaultFolder.png", thumbnailImage=iconimage)
        liz.setInfo( type="Video", infoLabels={ "Title": name, 'plot': description } )
        liz.setProperty('fanart_image', fanart)
        ok=xbmcplugin.addDirectoryItem(handle=int(sys.argv[1]),url=u,listitem=liz,isFolder=False)
        return ok

def addDir(name,url,mode,iconimage,fanart,description=''):
        u=sys.argv[0]+"?url="+urllib.quote_plus(url)+"&mode="+str(mode)+"&name="+urllib.quote_plus(name)+"&description="+str(description)
        ok=True
        liz=xbmcgui.ListItem(name, iconImage="DefaultFolder.png", thumbnailImage=iconimage)
        liz.setInfo( type="Video", infoLabels={ "Title": name, 'plot': description } )
        liz.setProperty('fanart_image', fanart)
        ok=xbmcplugin.addDirectoryItem(handle=int(sys.argv[1]),url=u,listitem=liz,isFolder=True)
        return ok

def get_params():
        param=[]
        paramstring=sys.argv[2]
        if len(paramstring)>=2:
                params=sys.argv[2]
                cleanedparams=params.replace('?','')
                if (params[len(params)-1]=='/'):
                        params=params[0:len(params)-2]
                pairsofparams=cleanedparams.split('&')
                param={}
                for i in range(len(pairsofparams)):
                        splitparams={}
                        splitparams=pairsofparams[i].split('=')
                        if (len(splitparams))==2:
                                param[splitparams[0]]=splitparams[1]    
        return param
           
params=get_params()
url=None
name=None
mode=None
iconimage=None
description=None

try:url=urllib.unquote_plus(params["url"])
except:pass
try:name=urllib.unquote_plus(params["name"])
except:pass
try:mode=int(params["mode"])
except:pass
try:iconimage=urllib.unquote_plus(params["iconimage"])
except:pass
print "Mode: "+str(mode);print "URL: "+str(url);print "Name: "+str(name);print "IconImage: "+str(iconimage)

if mode==None or url==None or len(url)<1:Menu()
elif mode==1:GetEpisodes(url)
elif mode==100:Play(name,url)

xbmcplugin.endOfDirectory(int(sys.argv[1]))

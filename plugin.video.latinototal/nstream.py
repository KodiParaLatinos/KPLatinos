# -*- coding: utf-8 -*-
#--------------------------------------------------------
#  creado por quequeQ para PalcoTV
# (http://forum.rojadirecta.es/member.php?1370946-quequeQ)
# (http://xbmcspain.com/foro/miembro/quequino/)
# Version 0.0.3 (01.11.2014)
#--------------------------------------------------------
# License: GPL (http://www.gnu.org/licenses/gpl-3.0.html)
#--------------------------------------------------------

import re,urllib,urllib2,sys
import plugintools,ioncube
def nstream(url,ref,caster,res,script):
 if caster == '9stream':
    nstr(url,ref,res)
 elif caster == 'ucaster':
    ucaster(url,ref,res)
 elif caster == 'mips':
    mips(url,ref,res)
 elif caster == 'ezcast':
    ezcast(url,ref,res)
 elif caster == 'tvonlinegratis':
    tvonlinegratis(url,ref,res)
 elif caster == 'm3u8':
    m3u8(url,ref,res)
 else:
    print "\nNSCRIPT = "+str(script);print "\nURL = "+url;print "\nREFERER = "+str(ref);print "\nCASTER = "+str(caster);
    #print bodyy;sys.exit()
	
def nstr(url,ref,res):
 p1 = re.compile(ur'embed\/=?\'?"?([^\'"\&,;]+)')
 p2 = re.compile(ur'width=?\'?"?([^\'"\&,;]+)')
 p3 = re.compile(ur'height=?\'?"?([^\'"\&,;]+)')
 f1=re.findall(p1, str(res));f2=re.findall(p2, str(res));f3=re.findall(p3, str(res));#res=list(set(f));
 w=f2[0];h=f3[0];c=f1[0];
 url='http://www.9stream.com/embedplayer.php?width='+w+'&height='+h+'&channel='+c+'&autoplay=true';body='';#
 bodi=curl_frame(url,ref,body)
 tkserv='';strmr='';plpath='';swf='';vala='';
 vals=ioncube.ioncube1(bodi)
 print "URL = "+url;print "REF = "+ref;
 tkserv=vals[0][1];strmr=vals[1][1].replace("\/","/");plpath=vals[2][1].replace(".flv","");swf=vals[3][1];
 ref=url;url=tkserv;bodi=curl_frame(url,ref,body);
 p='token":"([^"]+)';token=plugintools.find_single_match(bodi,p);#print token
 media_url = strmr+'/'+plpath+' swfUrl='+swf+' token='+token+' live=1 timeout=15 swfVfy=1 pageUrl='+ref
 plugintools.play_resolved_url(media_url)
 print "MEDIA URL="+media_url
 
def ezcast(url,ref,res):
 #print "NEDEFINIT";sys.exit()
 p = re.compile(ur'(width|height|channel)=\'?"?([^\,\'"]+)');par=re.findall(p,str(res));#print par;
 w=par[0][1];h=par[1][1];c=par[2][1];ref=url;url='http://www.ezcast.tv/embedded/'+c+'/1/'+w+'/'+h;body='';
 bodi=curl_frame(url,ref,body);
 p ='SWFObject\(\'?"?([^\'"]+)';swf='http://www.ezcast.tv'+plugintools.find_single_match(bodi,p);
 p = 'FlashVars\'?"?,?\s?\'?"?([^\'"]+)';flashvars=plugintools.find_single_match(bodi,p);
 p = re.compile(ur'\&?=([^\&]+)');flvs=re.findall(p,flashvars);id=flvs[0];c=flvs[1];
 lb='http://ezcast.tv:1935/loadbalancer';lb=plugintools.read(lb);lb=plugintools.find_single_match(lb,'redirect=(.*)');
 media_url = 'rtmp://'+lb+'/live/ playpath='+c+'?id='+id+' swfUrl='+swf+' swfVfy=1 conn=S:OK live=true pageUrl='+url
 plugintools.play_resolved_url(media_url)
'''
Si hay mas de un caster,se tiene que cambiar el "estado" del item (de playable=True a False y crear un popup para eligir opcion!!!
 #listitem.setProperty('IsPlayable', 'false');msg="Elige stream:\nezcast";
 #xbmc.Notification("CipQ-TV","ezcast\n9stream",300)
 #return media_url
'''
 
def mips(url,ref,res):
 p = re.compile(ur'(width|height|channel)=\'?"?([^\,\'"]+)');par=re.findall(p,str(res));
 w=par[0][1];h=par[1][1];c=par[2][1];ref=url;url='http://www.mips.tv/embedplayer/'+c+'/1/'+w+'/'+h;body='';
 bodi=curl_frame(url,ref,body);#print bodi
 p ='SWFObject\(\'?"?([^\'"]+)';swf='http://www.mips.tv'+plugintools.find_single_match(bodi,p);
 p = 'FlashVars\'?"?,?\s?\'?"?([^\'"]+)';flashvars=plugintools.find_single_match(bodi,p);
 p = re.compile(ur'\&?.*?=([^\&]+)');flashvars=re.findall(p,flashvars);id=flashvars[0];c=flashvars[1];
 lb='http://mips.tv:1935/loadbalancer';lb=plugintools.read(lb);lb=plugintools.find_single_match(lb,'redirect=(.*)');
 media_url = 'rtmp://'+lb+'/live/ playpath='+c+'?id='+id+' swfUrl='+swf+' swfVfy=1 conn=S:OK live=true pageUrl='+url
 plugintools.play_resolved_url(media_url)
 print "MEDIA URL="+media_url

def tvonlinegratis(url,ref,res):
 print "NSTREAM"+url+ref;body='';
 bodi=curl_frame(url,ref,body);
 try:
  ref=url;p = re.compile(ur'src="(.*tvonlinegratis[^"]+)');url=re.findall(p,bodi);url=str(url[0])
  bodi=curl_frame(url,ref,body);
 except:pass
 try:
  ref=url;url=plugintools.find_single_match(bodi,'href="([^"]+)');
  bodi=curl_frame(url,ref,body);#
 except:pass
 f='fid="([^"]+)';w='width=([^;]+)';h='height=([^;]+)';
 f=plugintools.find_single_match(bodi,f);w=plugintools.find_single_match(bodi,w);h=plugintools.find_single_match(bodi,h);
 ref=url;url='http://www.tvonlinegratis.mobi/player/'+ f +'.php?width='+w+'&height='+h;
 try:
  bodi=curl_frame(url,ref,body);print bodi
 except:pass
 ref=url;url='src="(.*?tvonlinegratis[^"]+)';url=plugintools.find_single_match(bodi,url);
 bodyy=curl_frame(url,ref,body);#print bodi
 from framescrape import jscalpe
 jscalpe(bodyy,url,ref)

def ucaster(url,ref,res):
 p1 = re.compile(ur'channel=?\'?"?([^\'"\&,;]+)');f1=re.findall(p1, str(res));
 p2 = re.compile(ur'width=?\'?"?([^\'"\&,;]+)');f2=re.findall(p2, str(res));
 p3 = re.compile(ur'height=?\'?"?([^\'"\&,;]+)');f3=re.findall(p3, str(res));
 c=f1[0];w=f2[0];h=f3[0];
 url='http://www.ucaster.eu/embedded/'+c+'/1/'+w+'/'+h;body=''
 bodi=curl_frame(url,ref,body)
 p ='SWFObject\(\'?"?([^\'"]+)';swf='http://www.ucaster.eu'+plugintools.find_single_match(bodi,p);
 p = 'FlashVars\'?"?,?\s?\'?"?([^\'"]+)';flashvars=plugintools.find_single_match(bodi,p);print flashvars;
 p = re.compile(ur'\&?.*?=([^\&]+)');flashvars=re.findall(p,flashvars);print flashvars;id=flashvars[0];c=flashvars[1];
 lb='http://www.ucaster.eu:1935/loadbalancer';lb=plugintools.read(lb);lb=plugintools.find_single_match(lb,'redirect=(.*)');
 media_url = 'rtmp://'+lb+'/live/ playpath='+c+'?id='+id+' swfUrl='+swf+' swfVfy=1 conn=S:OK live=true pageUrl='+url
 plugintools.play_resolved_url(media_url)
  
def m3u8(url,ref,res):
 plugintools.play_resolved_url(str(res))
		
def curl_frame(url,ref,body):
	request_headers=[];
	request_headers.append(["User-Agent","Mozilla/5.0 (Macintosh; Intel Mac OS X 10_8_3) AppleWebKit/537.31 (KHTML, like Gecko) Chrome/26.0.1410.65 Safari/537.31"])
	request_headers.append(["Referer",ref])
	body,response_headers=plugintools.read_body_and_headers(url, headers=request_headers);
	return body
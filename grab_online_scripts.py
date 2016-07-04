
#!/usr/bin/env python
# -*- coding: utf-8 -*-


import mechanize
import cookielib
from bs4 import BeautifulSoup
from ConfigParser import SafeConfigParser
from dateutil import parser
import datetime
import time
import pickle
import urllib
import re
from pprint import pprint

def get_br():
    br = mechanize.Browser()
    cj = cookielib.LWPCookieJar()
    br.set_cookiejar(cj)
    br.set_handle_equiv(True)
    br.set_handle_gzip(True)
    br.set_handle_redirect(True)
    br.set_handle_referer(True)
    br.set_handle_robots(False)
    br.set_handle_refresh(mechanize._http.HTTPRefreshProcessor(), max_time=1)
    br.addheaders = [
                            ('User-agent', 'Mozilla/5.0 (Windows NT 6.3; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/49.0.2623.87 Safari/537.36'),
                            ('Accept', '*/*')
                    ]
    return br

def get_soup(link):
    br = get_br()
    html = br.open(link).read()
    ht = ht = re.sub(r'<!--.*-->', '', html)
    soup = BeautifulSoup(ht)
    return soup

def append_href(basic_link, href):
    return basic_link+t.get('href') if not href.startswith('/') else basic_link[:-1]+href


'''
link = 'http://www.imsdb.com/all%20scripts/'

soup = get_soup(link)

#('',{'':''})

temp = soup.find('body').findAll('table',recursive=False)[1].find('tr',recursive=False).findAll('td',recursive=False)[2].findAll('a')

links = [
    append_href('http://www.imsdb.com/', t.get('href')) for t in temp
]


scr_ls = []
i =0
for l in links:
    l = urllib.quote(l,safe=':/')
    soup = get_soup(l)
    tt = soup.find('table',{'class':'script-details'}).findAll('a')[-1]
    if(tt.text.strip() != 'Back to the homepage'):
        s_l = append_href('http://www.imsdb.com/', tt.get('href'))
        scr_ls.append(s_l)
    else:
        print('E: '+l)
    i+=1
    print('Finished '+str(i)+' of '+str(len(links)))

pickle.dump(scr_ls,open('script_links.p','wb'))
'''

scr_ls = pickle.load( open( 'script_links.p', "rb" ) )

i=0
data = []
for scr_l in scr_ls:
    try:
        scr_l = urllib.quote(scr_l,safe=':/')
        soup = get_soup(scr_l)
        script = str(soup.find('td',{'class':'scrtext'}).find('pre'))
        title = soup.find('title').text.replace('Script at IMSDb.','').strip()
        data.append(
        {
            'script':script,
            'title':title,
            'link':scr_l
        }
        )
    except:
        print('Error for link: '+scr_l)
    i+=1
    print('Finished '+str(i)+' of '+str(len(scr_ls)))

pickle.dump(data,open('script_data.p','wb'))


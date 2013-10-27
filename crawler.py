#!/usr/bin/python
# -*- coding: utf-8 -*- 
import urllib2
import parser
import socket
import logging
import conf
import exception
import time

##The speed will enhance when include the header
agent = "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/30.0.1599.66 Safari/537.36"
Accept = "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8"
AcceptLanguage = "en-US,en;q=0.8"
CacheControl = "max-age=0"
Connection = "keep-alive"

HEADERS = {
    "cookie": "", 
    "User-Agent": "", 
    "Accept": Accept, 
    "Accept-Language": AcceptLanguage,
    "Cache-Control": CacheControl,
    "Connection": Connection
    }



##IMDB ratings crawler
def crawlMovie(startID): 
    logging.basicConfig(filename=conf.logPath,format="%(asctime)s:%(levelname)s:%(message)s",level=logging.DEBUG)
    prefix = "http://www.imdb.com/search/title?at=0&count=100&sort=moviemeter,asc&start="
    postfix = "&title_type=feature,tv_series"
    while(True):
        print "sssssssssssssssssssssssssssssssssssssssstartID: " + str(startID)
        logging.info("sssssssssssssssssssssssssssssssssssssssstartID: " + str(startID))
        url = prefix + str(startID) + postfix
        req = urllib2.Request(url, headers=HEADERS)#Without headers is very slow
        
        try:
            page = urllib2.urlopen(req, timeout=10).read()
        except urllib2.URLError:
            print "##crawlMovie: Bad url or timeout, reconnecting..."
            logging.warning("##crawlMovie: Bad url or timeout, reconnecting...")
            continue
        except socket.timeout:
            print "##crawlMovie: Timeout, reconnecting..."
            logging.warning("##crawlMovie: Timeout, reconnecting...")
            continue 
        except socket.error:
            print "##crawlMovie: socket.error, wait " + str(conf.waitTime) + "s to connect again."
            logging.warning("##crawlMovie: socket.error, wait " + str(conf.waitTime) + "s to connect again.")
            time.sleep(conf.waitTime) 
            continue
        
        try:
            flag = parser.parseMovie(page, startID)
        except exception.requestLimitException, e:
            print "##crawlMovie: Request limit, wait " + str(conf.waitTime) + "s to connect again."
            logging.warning("##crawlMovie: Request limit, wait " + str(conf.waitTime) + "s to connect again.")
            time.sleep(conf.waitTime) 
            continue

        if(not flag):
            print "##crawlMovie url: " + url
            logging.warning("##crawlMovie url: " + url)
            break
        else:
            startID = startID + 100


def main():
    startID = conf.startID #Not the movie ID, just the sequence number of the movie
    crawlMovie(startID)

if __name__=='__main__':
	main()
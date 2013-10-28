# -*- coding: utf-8 -*- 
import re
import urllib2
import socket
import logging
import conf
import dbhandler
import sys
import exception
import time

HEADERS = {"User-Agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/30.0.1599.66 Safari/537.36"}

##Extract the movie url
def parseMovie(page, startID):
    logging.basicConfig(filename=conf.logPath,format="%(asctime)s:%(levelname)s:%(message)s",level=logging.DEBUG)
    movie_pat = re.compile(r"<a href=\"/title/tt([\d]*)/\" title=")
    error_pat = re.compile(r"<title>(IMDb: Error)</title>")#To test whether reach error page
    if error_pat.search(page):
        print "##parseMovie: Got error page, maybe it is done crawling"
        logging.warning("##parseMovie: Got error page, maybe it is done crawling")
        return False
    error_pat_2 = re.compile(r"<title>404 Error</title>")
    if error_pat_2.search(page):
        raise exception.requestLimitException("404 Error")
        return False

    for id in movie_pat.finditer(page):
        if conf.movieID != "-1":
            if id.group(1) != conf.movieID:
                continue
            else:
                conf.movieID = "-1" #disable the movieID

    	print "startID: " + str(startID) + " movieID: " + id.group(1)
        logging.info("startID: " + str(startID) + " movieID: " + id.group(1))
        url = "http://www.imdb.com/title/tt%s/"%(id.group(1))
        req = urllib2.Request(url, headers=HEADERS)
        while(True):
            try:
                content = urllib2.urlopen(req, timeout=5).read()
                if parseMovieInfo(content, id.group(1)):
                    if parseRating(id.group(1)):
                        break
                    else:
                        return False
                else:
                    return False
            except urllib2.URLError:
                print "##parseMovie: Bad url or timeout, reconnecting..."
                logging.warning("##parseMovie: Bad url or timeout, reconnecting...")
                continue
            except socket.timeout:
                print "##parseMovie: Timeout, reconnecting..."
                logging.warning("##parseMovie: Timeout, reconnecting...")
                continue 
            except exception.requestLimitException, e:
                print "##parseMovie: Request limit, wait " + str(conf.waitTime) + "s to connect again."
                logging.warning("##parseMovie: Request limit, wait " + str(conf.waitTime) + "s to connect again.")
                time.sleep(conf.waitTime)
                continue
            except socket.error:
                print "##parseMovie: socket.error, wait " + str(conf.waitTime) + "s to connect again."
                logging.warning("##parseMovie: socket.error, wait " + str(conf.waitTime) + "s to connect again.")
                time.sleep(conf.waitTime) 
                continue
    return True

##Extract movie info
def parseMovieInfo(page, movieID):
    logging.basicConfig(filename=conf.logPath,format="%(asctime)s:%(levelname)s:%(message)s",level=logging.DEBUG)

    error_pat_2 = re.compile(r"<title>404 Error</title>")
    if error_pat_2.search(page):
        raise exception.requestLimitException("404 Error")
        return False

    ##movie's title
    title_pat = re.compile(r"<h1 class=\"header\">[^>]*>([^<]*)</span>")
    title_re = title_pat.search(page)

    ##movie's release year
    year_pat_1 = re.compile(r"ref_=tt_ov_inf\" >([\d]*)</a>\)</span>") 
    year_pat_2 = re.compile(r"<span class=\"nobr\">(.*)</span>[^<]*</h1>")
    year_re = year_pat_1.search(page)
    if not year_re:
        year_re = year_pat_2.search(page)

    ##movie's average rating from imdb
    avRating_pat = re.compile(r"star-box-giga-star\">([^<]*)</div>")
    avRating_re = avRating_pat.search(page)

    ##movie's length and type(<=3)
    length_pat_str = r"<div class=\"infobar\">([^<]*<span[^<]*</span>|)[^<]*<time[^>]*>[\s]*(?P<length>[^<\n]*)[\s]*</time>"
    type_pat_str = r"([^<]*<a[^<]*<span[^>]*>([^<]*)</span></a>[^<]*<span[^<]*</span>|)"
    type_pat_str_postfix = r"([^<]*<a[^<]*<span[^>]*>([^<]*)</span></a>|)"
    length_type_pat = re.compile(length_pat_str + type_pat_str + type_pat_str + type_pat_str_postfix)
    length_type_re = length_type_pat.search(page)

    title = ""
    year = ""
    avRating = ""
    length = ""
    type_ = ""

    if title_re: 
        title = title_re.group(1)
    if year_re:
        year = year_re.group(1)
    if avRating_re:
        avRating = avRating_re.group(1)
    if length_type_re:
        length = length_type_re.group("length")
        if length_type_re.group(4):
            type_ = type_ + length_type_re.group(4)
        if length_type_re.group(6):
            type_ = type_ + "|" + length_type_re.group(6)
        if length_type_re.group(8):
            type_ = type_ + "|" + length_type_re.group(8)
    
    ##To avoid the "InvalidStringData" error when we insert the data into the db
    flag = True
    try:
        title_temp = title.decode("unicode_escape")
    except UnicodeDecodeError:
        flag = False

    if flag:
        title = title_temp        
    else:
        title = ""

    info = {
        "title": title,
        "year": year,
        "avRating": avRating,
        "length": length,
        "type": type_,
        "movieID": movieID
        }
    try:
        dbhandler.writeMovieInfo(info)
    except:
        print "##writeMovieInfo db error:", sys.exc_info()[0]
        logging.error("##writeMovieInfo db error: " + str(sys.exc_info()[0]))
        return False

    print "title: " + title
    print "year: " + year
    print "avRating: " + avRating
    print "length: " + length
    print "type: " + type_
    print "movieID: " + movieID
    return True

##Extract the rating url
def parseRating(id):
    logging.basicConfig(filename=conf.logPath,format="%(asctime)s:%(levelname)s:%(message)s",level=logging.DEBUG)
    prefix = "http://www.imdb.com/title/tt"
    postfix = "/reviews?start="
    
    startID = 0
    if conf.ratingStartID != 0:
        startID = conf.ratingStartID
        conf.ratingStartID = 0

    ratingCount = 0
    while(True):
        print "RRRRRRRRRRRRRRRRRRRRRRRRating startID: " + str(startID)
        logging.info("Rating startID: " + str(startID))
        url = prefix + id + postfix + str(startID)
        req = urllib2.Request(url, headers=HEADERS)
        try:
            page = urllib2.urlopen(req, timeout=5).read()
            count = parseRatingInfo(page, id)
            if count == -1:
                print "##parseRating url: " + url
                logging.warning("##parseRating url: " + url)
                return False
            if count != 0:
                startID += 10
                ratingCount += count
                continue
            else:
                print str(ratingCount) + " rating(s) have been crawled"
                logging.info(str(ratingCount) + " rating(s) have been crawled")
                break
        except urllib2.URLError:
            print "##parseRating: Bad url or timeout, reconnecting..."
            logging.warning("##parseRating: Bad url or timeout, reconnecting...")
            continue
        except socket.timeout:
            print "##parseRating: Timeout, reconnecting..."
            logging.warning("##parseRating: Timeout, reconnecting...")
            continue
        except exception.requestLimitException, e:
            print "##parseRating: Request limit, wait " + str(conf.waitTime) + "s to connect again."
            logging.warning("##parseRating: Request limit, wait " + str(conf.waitTime) + "s to connect again.")
            time.sleep(conf.waitTime)
            continue
        except socket.error:
            print "##parseRating: socket.error, wait " + str(conf.waitTime) + "s to connect again."
            logging.warning("##parseRating: socket.error, wait " + str(conf.waitTime) + "s to connect again.")
            time.sleep(conf.waitTime) 
            continue

    return True
        


##Extract the rating info
def parseRatingInfo(page, movieID):
    logging.basicConfig(filename=conf.logPath,format="%(asctime)s:%(levelname)s:%(message)s",level=logging.DEBUG)
    error_pat_2 = re.compile(r"<title>404 Error</title>")
    if error_pat_2.search(page):
        raise exception.requestLimitException("404 Error")
        return -1

    topic_pat_str = r"<h2>([^<]*)</h2>[^<]*<[^a]*"
    rating_pat_str = r"alt=\"([\d]*)/10\"[^>]*><br>[^<]*<b>Author:"
    author_pat_str = r"</b>[^<]*<a href=\"/user/ur([\d]*)/\"[^<]*</a>"

    location_pat_str = r"([^<]*<small>from ([^<]*)</small>|)" #not necessary
    time_pat_str = r"[^s]*small>(?P<time>[^<]*)</small>" 

    pat = re.compile(topic_pat_str + 
                    rating_pat_str + 
                    author_pat_str +
                    location_pat_str +
                    time_pat_str)
    
    count = 0 #To sum up ratings have been crawled
    for result in pat.finditer(page):
        topic = result.group(1)
        rating = result.group(2)
        author = result.group(3)
        location = ""
        if(result.group(5)):
            location = result.group(5)
        time = result.group("time")
        
        ##To avoid the "InvalidStringData" error when we insert the data into the db
        flag = True
        try:
            topic_temp = topic.decode("unicode_escape")
        except UnicodeDecodeError:
            flag = False
        
        if flag:
            topic = topic_temp
        else:
            topic = ""

        print "-------------" + movieID + "---------------"
        print "topic: " + topic
        print "rating: " + rating
        print "author: " + author
        print "location: " + location
        print "time: " + time
        print "movieID: " + movieID
        print "-----------------------------------"

        info = {
            "topic": topic,
            "rating": rating,
            "author": author,
            "location": location,
            "time": time,
            "movieID": movieID
        }
        try:
            dbhandler.writeRatingInfo(info)
        except:
            print "##writeRatingInfo db error:", sys.exc_info()[0]
            logging.error("##writeRatingInfo db error: " + str(sys.exc_info()[0]))
            return -1
        count += 1

    if(count == 0):
        print "Finish crawling ratings of movie: " + movieID
        
    return count


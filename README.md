ImdbCrawler
===========

To crawl ratings from IMDB(http://www.imdb.com/).

##Why ImdbCrawler

Although there are some public datasets from recommendation research. 
Such as netflix and movielens. But they are too old for us to use now. 
IMDB is a professional website for people to share their comments and 
rating about the movies they have watched. So it will be helpful to 
our research if we can take advantage of the data on IMDB. Please 
don't use the data for business.

##Data Format

* All the data will be store in the mongodb. The crawler will automatically
create the database and collections if you have specified the name of the
database in *conf.py*.
* Two collections will be created when the the crawler is running: **MovieInfo**
(store the movie profies) and **Rating**(store the ratings of users).

###MovieInfo

{ "_id" : ObjectId("526e10b4c692561a7f89015d"), "movieID" : "0450345", "title" : "The Wicker Man", "length" : "102 min", "avRating" : " 3.6 ", "year" : "2006", "type" : "Horror|Mystery|Thriller" }

###Rating

{ "_id" : ObjectId("526e10bbc692561a7f89015e"), "rating" : "1", "movieID" : "0450345", "author" : "1616214", "topic" : "Misled by a critic", "location" : "United States", "time" : "6 September 2006" }


* The profile the movie is not crawled totally. I will make the crawler to crawl
more information. You can also change the regular expression in *parser.py* to crawl the information you want.

##Quick Start

You can run the code easily as following:
* Since the code is written by python, you should install python at 
the first place.
* Install mongodb in your machine and start the service.
* Modify the configration file(*conf.py*) if necessary.
* Run the crawler in command line:    >>>>python crawler.py

##More Information

If you have any questions or suggestions, feel free to contact me
(shaoyf2011@gmail.com).

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

{ "_id" : ObjectId("526bec09c69256153b8665ac"), "title" : "From Paris with Love", "length" : "92 min", "avRating" : " 6.4 ", "year" : "2010", "type" : "Action|Crime|Thriller" }

###Rating

{ "_id" : ObjectId("526bec0dc69256153b8665ad"), "rating" : "9", "author" : "22942150", "topic" : "A must see, equal to Taken.", "location" : "Sweden", "time" : "4 March 2010" }

* The profile the movie is not crawled totally. I will make the crawler to crawl
more information. You can also change the regular expression in *parser.py* to crawl the information you want.

##Quick Start

You can run the code easily as following:
* Since the code is written by python, you should install python at 
the first place.
* Install mongodb in your machine and start the service.
* Modify the configration file(conf.py) if necessary.
* Run the crawler in command line:    >>>>python crawler.py

##More Information

If you have any questions or suggestions, feel free to contact me
(shaoyf2011@gmail.com).

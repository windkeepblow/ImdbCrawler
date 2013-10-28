##Configration file of the imdb crawler

logPath = "imdbCrawler.log" #The path of the log file
database = "imdbdb" #The name of the database(mongodb)
waitTime = 60 #When reach the request limit, how many seconds will the program wait for

##Parameters for debug
startID = 2675 #From what sequence number of movie should the crawler begin crawling
ratingStartID = 60 #From what sequence number of comment(rating) to begin crawling
movieID = "0450345" #From what movieID to crawl, -1 is to disable the movieID.(type: String)


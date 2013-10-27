# -*- coding: utf-8 -*-
import pymongo
import conf

def writeMovieInfo(info):
	connection = pymongo.Connection('localhost', 27017)
	db = connection[conf.database]
	movieInfoCol = db.MovieInfo
	movieInfoCol.insert(info)


def writeRatingInfo(info):
	connection = pymongo.Connection('localhost', 27017)
	db = connection[conf.database]
	ratingCol = db.Rating
	ratingCol.insert(info)

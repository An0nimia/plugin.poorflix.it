#!/usr/bin/python

class ScrapingFailed(Exception):
	def __init__(self, message):
		Exception.__init__(self, "Can not scrape %s :(" % message)
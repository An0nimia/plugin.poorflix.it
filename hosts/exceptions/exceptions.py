#!/usr/bin/python

class VideoNotAvalaible(Exception):
	def __init__(self, message):
		Exception.__init__(self, "The video %s isn't avalaible :(" % message)
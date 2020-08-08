#!/usr/bin/python

from re import findall
from requests import get
from exceptions.exceptions import VideoNotAvalaible

class Metadata:
	def __init__(self):
		self.logo = None
		self.icon = None

def get_emb(url):
	if not "embed" in url:
		url = url.split("/")
		del url[-1]
		url[-1] = "embed-%s.html" % url[-1]
		url = "/".join(url)

	return url

def get_video(url):
	url = get_emb(url)
	body = get(url).text

	videos =  findall(
		r"file:[^']'([^']+)',\s*label:[^\"]\"([^\"]+)\"", body
	)

	if not videos:
		raise VideoNotAvalaible(url)

	if videos[1][1] == "HD":
		return videos[1][0]
	elif videos[0][1] == "NORMAL":
		return videos[0][0]
	elif videos[-1][1] == "MOBILE":
		return videos[2][0]
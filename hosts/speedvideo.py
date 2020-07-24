#!/usr/bin/python

from re import findall
from requests import get

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

	video_url =  findall(
		r"file:[^']'([^']+)',\s*label:[^\"]\"([^\"]+)\"", body
	)

	return video_url
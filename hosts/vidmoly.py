#!/usr/bin/python

from requests import get

class Metadata:
	def __init__(self):
		self.logo = "https://vidmoly.net/img/logo-main.png"
		self.icon = "https://vidmoly.net/img/faviconm.ico"

def get_video(url):
	body = get(url).text

	video_url = (
		body
		.split("sources: ")[1]
		.split("file:\"")[1]
		.split("\"")[0]
	)

	return video_url
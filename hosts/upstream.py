#!/usr/bin/python

from requests import get

class Metadata:
	def __init__(self):
		self.logo = "https://upstream.to/mngez/images/logo.png"
		self.icon = "https://upstream.to/mngez/images/favicon.png"

def get_video(url):
	body = get(url).text

	video_url = (
		body
		.split("sources: [{file:\"")[1]
		.split("\"")[0]
	)

	return video_url
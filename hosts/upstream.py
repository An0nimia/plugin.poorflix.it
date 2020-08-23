#!/usr/bin/python

from requests import get
from hosts.exceptions.exceptions import VideoNotAvalaible

class Metadata:
	def __init__(self):
		self.logo = "https://upstream.to/mngez/images/logo.png"
		self.icon = "https://upstream.to/mngez/images/favicon.png"

def get_video(url):
	body = get(url).text

	try:
		video_url = (
			body
			.split("sources: [{file:\"")[1]
			.split("\"")[0]
		)
	except IndexError:
		raise VideoNotAvalaible(url)

	return video_url
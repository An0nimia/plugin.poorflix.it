#!/usr/bin/python

from requests import get
from exceptions.exceptions import VideoNotAvalaible

class Metadata:
	def __init__(self):
		self.logo = "https://cdn.vup.to/apple-touch-icon.png"
		self.icon = "https://cdn.vup.to/favicon-16x16.png"

def get_video(url):
	body = get(url).text

	try:
		video_url = (
			body
			.split("sources: [{src: \"")[1]
			.split("\"")[0]
		)
	except IndexError:
		raise VideoNotAvalaible(url)

	return video_url
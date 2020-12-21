#!/usr/bin/python

from requests import get
from scrapers.utils import headers
from hosts.exceptions.exceptions import VideoNotAvalaible

class Metadata:
	def __init__(self):
		self.logo = "https://vidmoly.net/img/logo-main.png"
		self.icon = "https://vidmoly.net/img/faviconm.ico"

def get_video(url, referer):
	headers['Referer'] = referer
	body = get(url, headers = headers).text

	try:
		video_url = (
			body
			.split("sources: ")[1]
			.split("file:\"")[1]
			.split("\"")[0]
		)
	except IndexError:
		raise VideoNotAvalaible(url)

	return video_url
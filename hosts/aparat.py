#!/usr/bin/python

from requests import get
from scrapers.utils import headers
from hosts.exceptions.exceptions import VideoNotAvalaible

class Metadata:
	def __init__(self):
		self.logo = None
		self.icon = None

def get_video(url, referer):
	headers['Referer'] = referer
	body = get(url, headers = headers).text

	try:
		video_url = (
			body
			.split("sources: [{")[1]
			.split("\"")[1]
			.split("\"")[0]
		)
	except IndexError:
		raise VideoNotAvalaible(url)

	return video_url
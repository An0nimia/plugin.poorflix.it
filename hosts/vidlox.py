#!/usr/bin/python

from requests import get
from scrapers.utils import headers

class Metadata:
	def __init__(self):
		self.logo = None
		self.icon = None

def get_video(url, referer):
	headers['Referer'] = referer
	body = get(url, headers = headers).text

	video_url = (
		body
		.split("sources: [\"")[1]
		.split(",")[3]
		[1:-2]
	)

	return video_url
#!/usr/bin/python

from requests import get
from bs4 import BeautifulSoup
from scrapers.utils import headers

class Metadata:
	def __init__(self):
		self.logo = None
		self.icon = None

def get_video(url, referer):
	headers['Referer'] = referer
	body = get(url, headers = headers).text

	video_url = (
		BeautifulSoup(body, "html.parser")
		.find("p")
		.get_text()
	)

	return "https://verystream.com/gettoken/" + video_url
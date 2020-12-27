#!/usr/bin/python

from requests import get
from bs4 import BeautifulSoup

class Metadata:
	def __init__(self):
		self.logo = None
		self.icon = None

def get_video(url):
	body = get(url).text

	video_url = (
		BeautifulSoup(body, "html.parser")
		.find_all("source")[-1]
		.get("src")
	)

	return video_url
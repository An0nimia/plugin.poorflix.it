#!/usr/bin/python

from requests import get
from bs4 import BeautifulSoup

class Metadata:
	def __init__(self):
		self.logo = "https://streamtape.com/images/Logo@2x.png"
		self.icon = "https://streamtape.com/favicon.ico"

def get_video(url):
	body = get(url).text
	parsing = BeautifulSoup(body, "html.parser")

	video_link = (
		parsing
		.find("div", id = "videolink")
		.get_text()
	)

	video_url = "https:%s" % video_link
	return video_url
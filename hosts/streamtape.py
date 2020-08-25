#!/usr/bin/python

from requests import get
from bs4 import BeautifulSoup
from hosts.exceptions.exceptions import VideoNotAvalaible

class Metadata:
	def __init__(self):
		self.logo = "https://streamtape.com/images/Logo@2x.png"
		self.icon = "https://streamtape.com/favicon.ico"

def get_video(url):
	body = get(url).text
	parsing = BeautifulSoup(body, "html.parser")

	try:
		video_link = (
			parsing
			.find("div", id = "videolink")
			.get_text()
		)
	except AttributeError:
		raise VideoNotAvalaible(url)

	video_url = "https:%s" % video_link
	return video_url
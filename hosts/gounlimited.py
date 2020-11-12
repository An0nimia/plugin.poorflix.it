#!/usr/bin/python

from requests import get
from bs4 import BeautifulSoup
from scrapers.utils import get_piece
from hosts.exceptions.exceptions import VideoNotAvalaible

class Metadata:
	def __init__(self):
		self.logo = "https://gounlimited.to/theme_2/assets/images/logo.png"
		self.icon = "https://gounlimited.to/theme_2/assets/images/favicon.ico"

def get_emb(url):
	if not "embed" in url:
		url = url.split("/")
		url[-1] = "embed-%s.html" % url[-1]
		url = "/".join(url)

	return url

def get_video(url):
	url = get_emb(url)
	body = get(url).text
	pieces = BeautifulSoup(body, "html.parser").find_all("script")

	try:
		piece = get_piece(pieces)
	except UnboundLocalError:
		raise VideoNotAvalaible(url)

	splitted = ["", "", ""]
	splitted += piece.split("|")[3:]

	indexs = (
		piece
		.split("//")[1]
		.split("\"")[0]
	)

	video_url = "http://"

	for a in indexs.split("/"):
		things = a.split(".")

		for b in things:
			if b == "v":
				video_url += "v."
				continue

			index = int(b, 36)
			video_url += splitted[index]

			if b != things[-1]: 
				video_url += "."

		video_url += "/"

	if video_url.endswith("/small3.mp4/"):
		raise VideoNotAvalaible(url)

	return video_url[:-1]
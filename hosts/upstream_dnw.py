#!/usr/bin/python

from requests import get
from bs4 import BeautifulSoup
from scrapers.utils import get_piece, headers
from hosts.exceptions.exceptions import VideoNotAvalaible

class Metadata:
	def __init__(self):
		self.logo = "https://upstream.to/mngez/images/logo.png"
		self.icon = "https://upstream.to/mngez/images/favicon.png"

def get_video(url, referer):
	headers['Referer'] = referer
	body = get(url, headers = headers).text
	print(body)
	pieces = BeautifulSoup(body, "html.parser").find_all("script")

	try:
		piece = get_piece(pieces)
	except UnboundLocalError:
		raise VideoNotAvalaible(url)

	splitted = [""]
	splitted += piece.split("|")[1:]

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

	return video_url[:-1]
#!/usr/bin/python

from requests import get
from bs4 import BeautifulSoup
from scrapers.utils import get_piece, headers
from hosts.exceptions.exceptions import VideoNotAvalaible

class Metadata:
	def __init__(self):
		self.logo = "https://upstream.to/mngez/images/logo.png"
		self.icon = "https://upstream.to/mngez/images/favicon.png"

def get_video(url):
	body = get(url, headers = headers).text
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
		.split("\"}")[0]
	)

	s_indexs = indexs.split("/")
	video_url = "http://"

	for a in range(
		len(s_indexs)
	):
		if a == 0:
			for b in s_indexs[a].split("."):
				index = int(b, 36)
				video_url += "%s." % splitted[index]

			video_url = video_url[:-1]

		elif a == 1:
			index = int(s_indexs[a], 36)
			video_url += splitted[index]

		elif a == 2:
			things = s_indexs[a].split(",")

			for b in things:
				if b == "":
					video_url += ","
					continue

				elif b[0] == ".":
					video_url += "."
					b = b[1:]

				try:
					index = int(b, 36)
					video_url += splitted[index]

					if b != things[-1][1:]:
						video_url += ","
				except ValueError:
					raise VideoNotAvalaible(url)

		elif a == 3:
			things = s_indexs[a].split(".")

			for b in things:
				index = int(b, 36)
				video_url += splitted[index]

				if b != things[-1]:
					video_url += "."

		video_url += "/"

	return video_url[:-1]

#print(get_video("https://upstream.to/embed-5qoz71lnt5ye.html"))
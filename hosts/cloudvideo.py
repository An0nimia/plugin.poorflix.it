#!/usr/bin/python

from requests import get
from bs4 import BeautifulSoup
from scrapers.utils import get_piece

class Metadata:
	def __init__(self):
		self.logo = "https://cloudvideo.tv/static/img/logo5.png"
		self.icon = "https://cloudvideo.tv/favicon.ico"

def get_emb(url):
	if not "embed" in url:
		url = url.split("/")
		url[-1] = "embed-%s" % url[-1]
		url = "/".join(url)

	return url

def get_video(url):
	url = get_emb(url)
	body = get(url).text

	try:
		video_url = (
			body
			.split("sources: [{src: \"")[1]
			.split("\"")[0]
		)
	except IndexError:
		pieces = BeautifulSoup(body, "html.parser").find_all("script")
		piece = get_piece(pieces)
		splitted = [""]
		splitted += piece.split("|")[1:]

		indexs = (
			piece
			.split("//")[1]
			.split("\"")[0]
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
						s_b = b.split(".")
						index = int(s_b[1], 36)
						video_url += "v.%s" % splitted[index]

			elif a == 3:
				things = s_indexs[a].split(".")

				for b in things:
					index = int(b, 36)
					video_url += splitted[index]

					if b != things[-1]:
						video_url += "."

			video_url += "/"

		video_url = video_url[:-1]

	return video_url
#!/usr/bin/python

from requests import get
from bs4 import BeautifulSoup
from scrapers.utils import headers, get_piece

class Metadata:
	def __init__(self):
		self.logo = None
		self.icon = None

def get_emb(url):
	if "fastredirect" in url:
		body = get(url, headers = headers).text
		parse = BeautifulSoup(body, "html.parser")
		path = parse.find("form").get("action")
		url = "https://wstream.video%s" % path

	if not "video6zvimpy52" in url:
		url = url.split("/")
		url[-1] = url[-1].replace(".html", "")
		url[-2] = "video6zvimpy52"
		url = "/".join(url)

	return url

def get_video(url):
	url = get_emb(url)
	body = get(url, headers = headers).text

	pieces = BeautifulSoup(body, "html.parser").find_all("script")
	piece = get_piece(pieces)
	splitted = [""]
	splitted += piece.split("|")[1:]

	indexs = (
		piece
		.split("//")[2]
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

				index = int(b, 36)
				video_url += splitted[index]

				if b != things[-1][1:]:
					video_url += ","

		elif a == 3:
			things = s_indexs[a].split(".")

			for b in things:
				index = int(b, 36)
				video_url += splitted[index]

				if b != things[-1]:
					video_url += "."

		video_url += "/"

	return video_url[:-1]
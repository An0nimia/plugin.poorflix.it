#!/usr/bin/python

from time import sleep
from bs4 import BeautifulSoup
from requests import post, get
from scrapers.utils import get_piece

class Metadata:
	def __init__(self):
		self.logo = None
		self.icon = None

def get_video(url):
	body = get(url)
	parsing = BeautifulSoup(body.text, "html.parser").find_all("input")
	op = parsing[3].get("value")
	code = parsing[4].get("value")
	hashs = parsing[5].get("value")

	data = {
		"op": op,
		"code": code,
		"hash": hashs
	}

	sleep(5)
	ids = body.url.split("/")[-1]
	url = "https://vidtome.stream/plays/%s" % ids
	body = post(url, data).text
	pieces = BeautifulSoup(body, "html.parser").find_all("script")
	piece = get_piece(pieces)

	splitted = (
		piece
		.split(",'")[2]
		.split("|")
	)

	indexs = (
		piece
		.split("//")[1]
		.split("\\")[0]
	)

	video_url = "http://"

	for a in indexs:
		if a.isalpha() or a.isdigit():
			index = int(a, 36)
			what = splitted[index]

			if what == "":
				video_url += a
			else:
				video_url += what
		else:
			video_url += a

	return video_url
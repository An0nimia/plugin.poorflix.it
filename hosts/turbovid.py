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
	op = parsing[0].get("value")
	ids = parsing[2].get("value")
	fname = parsing[3].get("value")
	hashs = parsing[5].get("value")

	data = {
		"op": op,
		"id": ids,
		"fname": fname,
		"hash": hashs,
	}

	sleep(5)
	body = post(body.url, data).text
	pieces = BeautifulSoup(body, "html.parser").find_all("script")

	for a in pieces:
		c = str(a)

		if "var player" in c:
			piece = c
			break

	video_url = (
		piece
		.split(":")[2]
		.split("\"]")[0]
	)

	return "http:%s" % video_url
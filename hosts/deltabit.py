#!/usr/bin/python

from time import sleep
from bs4 import BeautifulSoup
from requests import post, get
from scrapers.utils import get_piece
from hosts.exceptions.exceptions import VideoNotAvalaible

class Metadata:
	def __init__(self):
		self.logo = "http://deltabit.co/img/logo.png"
		self.icon = "https://deltabit.co/images/favicon/favicon-16x16.png"

def get_video(url):
	body = get(url)
	parsing = BeautifulSoup(body.text, "html.parser").find_all("input")
	op = parsing[0].get("value")
	ids = parsing[2].get("value")
	fname = parsing[3].get("value")

	try:
		hashs = parsing[5].get("value")
	except IndexError:
		raise VideoNotAvalaible(url)

	data = {
		"op": op,
		"id": ids,
		"fname": fname,
		"hash": hashs,
	}

	sleep(5)
	body = post(body.url, data).text
	pieces = BeautifulSoup(body, "html.parser").find_all("script")
	piece = get_piece(pieces, 1)
	splitted = ["", "", ""]
	splitted += piece.split("|")[3:]

	indexs = (
		piece
		.split("//")[1]
		.split("\"]")[0]
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
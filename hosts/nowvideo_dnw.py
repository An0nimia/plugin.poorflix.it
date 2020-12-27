#!/usr/bin/python

from bs4 import BeautifulSoup
from requests import post, get
from scrapers.utils import get_piece, headers

class Metadata:
	def __init__(self):
		self.logo = "http://nowvid.online/images/logo.png"
		self.icon = "http://nowvid.online/images/favicon.ico"

def get_video(url, referer):
	headers['Referer'] = referer
	body = get(url, headers = headers)
	parsing = BeautifulSoup(body.text, "html.parser").find_all("input")
	op = parsing[0].get("value")
	code = parsing[1].get("value")
	hashs = parsing[2].get("value")
	url = "http://nowvid.online/videos/%s" % code

	data = {
		"op": op,
		"code": code,
		"hash": hashs
	}

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

print(get_video("http://nowvid.online/play/r1ipk5ur9hhv", ""))
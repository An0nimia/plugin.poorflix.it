#!/usr/bin/python

from requests import get
from bs4 import BeautifulSoup
from scrapers.utils import headers, get_piece

class Metadata:
	def __init__(self):
		self.logo = "https://wstream.video/img/logo.png"
		self.icon = "https://wstream.video/favicon.ico"

def decode_nored(url):
	body = get(url, headers = headers).text
	parse = BeautifulSoup(body, "html.parser")

	script = str(
		parse.find_all("script")[-1]
	)

	array = eval(
		script
		.split("=")[2]
		.split(";")[0]
	)

	magic_number = int(
		script
		.split("- ")[1]
		.split(")")[0]
	)

	iframe = ""

	for a in array:
		num = a - magic_number
		char = chr(num)
		iframe += char

	parse = BeautifulSoup(iframe, "html.parser")
	url = parse.find("iframe").get("src")
	return url

def get_emb(url):
	if "nored" in url:
		url = decode_nored(url)

	if not "video6zvimpy52" in url:
		url = url.split("/")
		url[-1] = url[-1].replace(".html", "")
		url[-2] = "video6zvimpy52"
		url = "/".join(url)

	return url

def get_video(url, referer):
	headers['Referer'] = referer

	#if not "fastredirect" in url:
		#url = get_emb(url)

	body = get(url, headers = headers).text
	
	"""
	video_url = (
		body
		.split("sources: [{")[1]
		.split("\"")[1]
		.split("\"")[0]
	)

	return video_url
	"""

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

				index = int(b, 36)
				video_url += splitted[index]

				if b != things[-1][1:]:
					video_url += ","

		elif a == 3:
			things = s_indexs[a].split(".")
			things1 = things[1].split("?")
			things2 = things1[1].split("=")
			index = int(things[0], 36)
			video_url += splitted[index]
			video_url += "."
			index = int(things1[0], 36)
			video_url += splitted[index]
			video_url += "?"
			index = int(things2[0], 36)
			video_url += splitted[index]
			video_url += "="
			index = int(things2[1], 36)
			video_url += splitted[index]

		video_url += "/"

	return video_url[:-1]
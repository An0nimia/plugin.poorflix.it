#!/usr/bin/python

from bs4 import BeautifulSoup
from requests import post, get
from exceptions.exceptions import VideoNotAvalaible

class Metadata:
	def __init__(self):
		self.logo = None
		self.icon = None

def get_video(url):
	body = get(url).text
	parse = BeautifulSoup(body, "html.parser")

	title = (
		parse
		.find("title")
		.get_text()
	)

	try:
		token = (
			body
			.split("var token=\"")[1]
			.split("\"")[0]
		)
	except IndexError:
		raise VideoNotAvalaible(url)

	csrf = (
		body
		.split("var crsf=\"")[1]
		.split("\"")[0]
	)

	data = {
		"gone": token,
		"oujda": csrf
	}

	video_api = "https://vidload.net/vid/"
	response = post(video_api, data).text[:-2]

	video_url = (
		"%s/%s"
		% (
			"/".join(
				response.split("/")[:-1]
			),
			title
		)
	)

	return video_url
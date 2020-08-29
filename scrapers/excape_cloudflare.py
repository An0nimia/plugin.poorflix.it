#!/usr/bin/python

from requests import get

proxy = "https://web.archive.org/save/%s"

class ex_Cloudflare:
	def __init__(self, url):
		self.link = proxy % url

	def get_body(self, timeout = 30):
		body = get(self.link, timeout = timeout).text

		body = (
			body
			.replace("/save/_embed/", "")
			.replace("/save/", "")
		)

		return body
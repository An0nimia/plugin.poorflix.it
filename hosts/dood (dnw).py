#!/usr/bin/python
#Thanks to URLResolver https://github.com/tvaddonsco/script.module.urlresolver/blob/master/lib/urlresolver/plugins/doodstream.py

from time import time
from math import floor
from requests import get
from random import random

class Metadata:
	def __init__(self):
		self.logo = "https://i.doodcdn.com/img/logo-s.png"
		self.icon = "https://doodstream.com/favicon.ico"

def decode(token):
	a = ""
	t = "ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789"
	n = len(t)

	for b in range(10):
		index = floor(
			random() * n
		)

		a += t[index]

	url = "?token{}{}".format(
		token, time()
	)

	return url

def get_video(url):
	body = get(url).text

	token = (
		body
		.split("token")[4]
		.split("\"")[0]
	)

	pathkey = (
		body
		.split("$.get('")[1]
		.split("'")[0]
	)

	urlkey = "https://dood.to%s" % pathkey

	headers = {
		"Referer": url
	}

	domain = get(urlkey, headers = headers).text
	path = decode(token)
	video_url = domain + path
	return video_url
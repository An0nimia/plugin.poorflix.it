#!/usr/bin/python
#Thanks to URLResolver https://github.com/tvaddonsco/script.module.urlresolver/blob/master/lib/urlresolver/plugins/doodstream.py

from time import time
from math import floor
from requests import get
from random import random

IE_USER_AGENT = 'User-Agent: Mozilla/5.0 (Windows NT 10.0; WOW64; Trident/7.0; rv:11.0) like Gecko'
FF_USER_AGENT = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:77.0) Gecko/20100101 Firefox/77.0'
OPERA_USER_AGENT = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/80.0.3987.132 Safari/537.36 OPR/67.0.3575.97'
IOS_USER_AGENT = 'Mozilla/5.0 (iPhone; CPU iPhone OS 13_3_1 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/13.0.5 Mobile/15E148 Safari/604.1'
ANDROID_USER_AGENT = 'Mozilla/5.0 (Linux; Android 9; SM-G973F) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/81.0.4044.138 Mobile Safari/537.36'
EDGE_USER_AGENT = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/70.0.3538.102 Safari/537.36 Edge/18.18363'
CHROME_USER_AGENT = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/84.0.4136.7 Safari/537.36'
SAFARI_USER_AGENT = 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_4) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/13.1 Safari/605.1.15'

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
	import string
	import random
	import re
	from scrapers.utils import headers
	from six.moves import urllib_parse, urllib_request
	_USER_AGENTS = [FF_USER_AGENT, OPERA_USER_AGENT, EDGE_USER_AGENT, CHROME_USER_AGENT, SAFARI_USER_AGENT]
	RAND_UA = random.choice(_USER_AGENTS)
	def dood_decode(data):
		t = string.ascii_letters + string.digits
		return data + ''.join([random.choice(t) for _ in range(10)])
	def append_headers(headers):
		return '|%s' % '&'.join(['%s=%s' % (key, urllib_parse.quote_plus(headers[key])) for key in headers])
	body = get(url).text
	headers['User-Agent'] = RAND_UA
	match = re.search(r'''dsplayer\.hotkeys[^']+'([^']+).+?function\s*makePlay.+?return[^?]+([^"]+)''', body, re.DOTALL)
	token = match.group(2)
	url = 'https://dood.to' + match.group(1)
	print(url)
	headers['Referer'] = "dood.to"
	body = get(url, headers = headers).text
	print(body)
	print(token)
	print(dood_decode(body))
	alls = dood_decode(body) + token + str(int(time() * 1000)) + append_headers(headers)
	print(get(alls).text)
	print(alls)
	return

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

#print(get_video("https://dood.to/e/a3k6i0ebtcsu"))
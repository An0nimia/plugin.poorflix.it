#!/usr/bin/python
# Thanks to DrZ3r0, but he doesn't know this

from re import findall
from requests import get
from scrapers import utils
from bs4 import BeautifulSoup

class Metadata:
	def __init__(self):
		self.logo = None
		self.icon = None

def decode(encoded, code):
	_0x59b81a = ""
	k = "ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789+/="[::-1]
	count = 0

	while count < len(encoded):
		_0x4a2f3a = k.index(encoded[count])
		count += 1
		_0x29d5bf = k.index(encoded[count])
		count += 1
		_0x3b6833 = k.index(encoded[count])
		count += 1
		_0x426d70 = k.index(encoded[count])
		count += 1
		_0x2e4782 = (_0x4a2f3a << 2) | (_0x29d5bf >> 4)
		_0x2c0540 = (_0x29d5bf & 15) << 4 | (_0x3b6833 >> 2)
		_0x5a46ef = (_0x3b6833 & 3) << 6 | _0x426d70
		_0x2e4782 = _0x2e4782 ^ code
		_0x59b81a = str(_0x59b81a) + chr(_0x2e4782)

		if _0x3b6833 != 64:
			_0x59b81a = str(_0x59b81a) + chr(_0x2c0540)

		if _0x3b6833 != 64:
			_0x59b81a = str(_0x59b81a) + chr(_0x5a46ef)

	return _0x59b81a

def get_video(url):
	body = get(url, headers = utils.headers).text

	matches = findall(
		"type:\"video/([^\"]+)\",src:d\('([^']+)',(.*?)\).+?height:(\d+)", body
	)

	for extension, encoded, code, quality in matches:

		video_url = decode(
			encoded, int(code)
		)

		while video_url.endswith("@"):
			video_url = video_url[:-1]

		if not video_url.startswith("http"):
			video_url = "http:" + video_url

		return video_url
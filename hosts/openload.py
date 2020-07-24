#!/usr/bin/python
# Thanks to DrZ3r0, but he doesn't know this

from math import pow
from re import findall
from requests import get
from bs4 import BeautifulSoup
from scrapers.utils import headers

class Metadata:
	def __init__(self):
		self.logo = None
		self.icon = None

def decode(code, parseInt, _0x59ce16, _1x4bfb36):
	_0x1bf6e5 = ""
	ke = []

	for i in range(
		0, len(code[0:9 * 8]), 8
	):
		ke.append(
			int(code[i:i + 8], 16)
		)

	_0x439a49 = 0
	_0x145894 = 0

	while _0x439a49 < len(code[9 * 8:]):
		_0x5eb93a = 64
		_0x896767 = 0
		_0x1a873b = 0
		_0x3c9d8e = 0

		while True:
			if _0x439a49 + 1 >= len(code[9 * 8:]):
				_0x5eb93a = 143

			_0x3c9d8e = int(
				code[9 * 8 + _0x439a49:9 * 8 + _0x439a49 + 2], 16
			)

			_0x439a49 += 2

			if _0x1a873b < 6 * 5:
				_0x332549 = _0x3c9d8e & 63
				_0x896767 += _0x332549 << _0x1a873b
			else:
				_0x332549 = _0x3c9d8e & 63

				_0x896767 += int(
					_0x332549 * pow(2, _0x1a873b)
				)

			_0x1a873b += 6

			if not _0x3c9d8e >= _0x5eb93a:
				break

		_0x30725e = _0x896767 ^ ke[_0x145894 % 9] ^ int(parseInt) ^ _1x4bfb36
		_0x2de433 = _0x5eb93a * 2 + 127

		for i in range(4):
			_0x3fa834 = chr(
				(
					(_0x30725e & _0x2de433) >> (9 * 8 // 9) * i
				) - 1
			)

			if _0x3fa834 != '$':
				_0x1bf6e5 += _0x3fa834

			_0x2de433 = _0x2de433 << (9 * 8 // 9)

		_0x145894 += 1

	url = "https://openload.co/stream/%s?mime=true" % _0x1bf6e5
	return url

def get_video(url):
	find = get(url, headers = headers).text

	try:
		code = (
			BeautifulSoup(find, "html.parser")
			.find("p")
			.get_text()
		)

		_0x59ce16 = eval(
			findall('_0x59ce16=([^;]+)', find)[0]
		)

		_1x4bfb36 = eval(
			findall('_1x4bfb36=([^;]+)', find)[0]
			.replace('parseInt', 'int')
		)

		parseInt = eval(
			findall('_0x30725e,(\(parseInt.*?)\),', find)[0]
			.replace('parseInt', 'int')
		)
		
		video_url = decode(code, parseInt, _0x59ce16, _1x4bfb36)
		return video_url
	except AttributeError:

		url = (
			BeautifulSoup(find, "html.parser")
			.find("iframe")
			.get("src")
		)

		return get_video(url)
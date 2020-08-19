#!/usr/bin/python

from requests import get
from bs4 import BeautifulSoup
from scrapers.utils import get_piece
from hosts.exceptions.exceptions import VideoNotAvalaible

class Metadata:
	def __init__(self):
		self.logo = "https://supervideo.tv/assets/images/logow.svg"
		self.icon = "https://supervideo.tv/assets/images/favicon/favicon-16x16.png"

def rep_string(string):
	string = (
		string
		.replace(".slice", "")
		.replace(".substr", "")
		.replace(".charAt", "")
		.replace("(", "[")
		.replace(")", "]")
		.replace(",", ":")
	)

	return string

def js_to_py(string):
	todo = ""

	if "String.fromCharCode" in string:
		todo += eval(
			string
			.replace("String.fromCharCode", "chr")
		)
	else:
		string = rep_string(string)
		s_string = string.split(":")

		if len(s_string) == 2:
			num1 = s_string[0][-1]
			num2 = s_string[1][1]

			if num1 > num2:
				string = (
					"{}{}]".format(
						s_string[0][:-1], num1
					)
				)

		todo += eval(
			rep_string(string)
		)

	return todo

def get_cookie(url):
	url = get_emb(url)
	body = get(url).text

	s = {}
	c, U, r, i, l = 0, 0, 0, 0, 0

	try:
		S = (
			body
			.split("S='")[1]
			.split("'")[0]
		)
	except IndexError:
		return

	L = len(S)  - 27
	U = 0
	r = ""
	A = "ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789+/"

	for a in range(64):
		s[A[a]] = a

	for a in range(L):
		c = s[S[a]]
		U = (U << 6) + c
		l += 6

		while l >= 8:
			l -= 8

			a = (
				(
					U >> l
				) & 0xff
			)

			if i < (L - 2):
				r += chr(a)

	n_variable = r[0]
	todo = ""
	alls = r[2:].split(";document.cookie=")

	for a in alls[0].split("+"):
		todo += js_to_py(a)

	cookie = ""

	for a in alls[1][:-1].split("+"):
		if a[1] == n_variable:
			cookie += todo
		else:
			cookie += js_to_py(a)

	return cookie

def get_emb(url):
	if not "/e/" in url and not "embed" in url:
		s_url = url.split("/")
		url = "/".join(s_url[:-1])
		url += "/e/%s" % s_url[-1]  

	return url

def get_video(url):
	url = get_emb(url)

	headers = {
		"Cookie": get_cookie(url)
	}

	body = get(url, headers = headers).text
	pieces = BeautifulSoup(body, "html.parser").find_all("script")

	try:
		piece = get_piece(pieces)
	except UnboundLocalError:
		raise VideoNotAvalaible(url)

	splitted = [""]
	splitted += piece.split("|")[1:]

	indexs = (
		piece
		.split("//")[1]
		.split("\"}")[0]
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

				try:
					index = int(b, 36)
					video_url += splitted[index]

					if b != things[-1][1:]:
						video_url += ","
				except ValueError:
					raise VideoNotAvalaible(url)

		elif a == 3:
			things = s_indexs[a].split(".")

			for b in things:
				index = int(b, 36)
				video_url += splitted[index]

				if b != things[-1]:
					video_url += "."

		video_url += "/"

	return video_url[:-1]
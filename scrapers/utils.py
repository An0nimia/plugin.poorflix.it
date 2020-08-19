#!/usr/bin/python

from base64 import b64decode
from bs4 import BeautifulSoup
from requests import post, get

headers = {
	"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:79.0) Gecko/20100101 Firefox/79.0"
}

def recognize_mirror(mirror):
	mirror = mirror.lower()

	if mirror == "akvid":
		mirror = "akvideo"

	elif mirror == "vidto":
		mirror = "vidtome"

	elif mirror == "gountimited":
		mirror = "gounlimited"

	elif mirror == "ciao":
		mirror = "vidmoly"

	return mirror

def recognize_link(link_mirror):
	if not link_mirror.startswith("http"):
		link_mirror = "http:%s" % link_mirror

	return link_mirror

def get_piece(pieces, typee = 0):
	if_is = "(p,a,c,k,e,d)"

	for a in pieces:
		c = str(a)

		if if_is in c:
			piece = c.split("'.split('|')")[0]

			if typee == 0:
				break

	return piece

def decode_middle_encrypted(encrypted):
	#old
	"""
	length_encrypted_middle = len(encrypted) // 2

	decoded = b64decode(
		(
			encrypted[-length_encrypted_middle:] + encrypted[:length_encrypted_middle]
		)[::-1]
	).decode()
	"""

	decoded = b64decode(encrypted).decode()
	return decoded

def adfly_decode(url):
	url1 = get(url).url

	url = "/".join(
		url1.split("/")[6:]
	).split("?")[0]

	if not url:
		return url1

	return url

def vcrypt_decode(url):
	body = get(url, headers = headers)

	if not "vcrypt" in body.url:
		return body.url

	parse = BeautifulSoup(body.text, "html.parser")

	if "wss" in url:
		url = (
			str(
				parse.find("meta")
			)
			.split("=")[2]
			.split("\"")[0]
		)

		url = get(url, headers = headers).url
	else:
		key = (
			parse
			.find("form")
			.get("action")
		)

		url_post = "http://vcrypt.net/fastshield/" + key

		post_data = {
			"go": "go"
		}

		url = post(
			url_post, post_data,
			headers = headers
		).url

	return url

def snip_decode(url):
	key = (
		get(url)
		.url
		.split("/")[-1]
	)

	url_post = "https://4snip.pw/outlink/" + key

	post_data = {
		"url": key
	}

	url = post(url_post, post_data).url
	return url

def buckler_decode(url):
	body = get(url, headers = headers)

	if not "buckler" in body.url:
		return body.url

	url = (
		body.text
		.split("MDCore.share_fb('")[1]
		.split("'")[0]
	)

	return url

def fasturl_decode(url):
	url = get(url).url
	return url

def m_identify(link):
	try:
		if not link.endswith("/"):
			link = decode_middle_encrypted(
				link.split("/")[-1]
			)
	except:
		pass

	link = link.replace("\r", "")

	c_supported = [
		"", "fasturl", "buckler",
		"vcrypt", "snip", "linkup",
		"gatustox", "cowner", "rweasy"
	]

	indexed = c_supported.index("linkup")
	times = 0
	link1 = ""

	while (
		any(
			a in link
			for a in c_supported
		) and times != 8
	):
		if link == "":
			link = link1
			break

		elif "vcrypt" in link:
			link1 = link
			link = vcrypt_decode(link)

		elif any(
			a in link
			for a in c_supported[indexed:]
		):
			link1 = link
			link = adfly_decode(link)

		elif "snip" in link:
			link1 = link
			link = snip_decode(link)

		elif "buckler" in link:
			link1 = link
			link = buckler_decode(link)

		elif "fasturl" in link:
			link1 = link1
			link = fasturl_decode(link)

		times += 1

	return link
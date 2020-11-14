#!/usr/bin/python

from hosts import host_files
from base64 import b64decode
from bs4 import BeautifulSoup
from requests import post, get
from difflib import SequenceMatcher

headers = {
	"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:79.0) Gecko/20100101 Firefox/79.0"
}

mirrors = []

for a in range(
	len(host_files)
):
	if host_files[a].endswith(".py"):
		mirrors.append(
			host_files[a][:-3]
		)

def check_mirror(mirror):
	array1 = []
	array2 = []

	for a in mirrors:
		ratio = SequenceMatcher(
			a = a,
			b = mirror
		).ratio()

		array1.append(a)
		array2.append(ratio)

	max_value = max(array2)

	if max_value <= 0.5:
		return ""

	index = array2.index(max_value)
	mirror = array1[index]
	return mirror	

def recognize_mirror(mirror):
	mirror = mirror.lower()
	mirror = mirror.replace(" ", "")

	if mirror == "ciao":
		mirror = "vidmoly"

	if not mirror in host_files:
		mirror = check_mirror(mirror)

	return mirror

def recognize_link(link_mirror):
	if not link_mirror.startswith("http"):
		link_mirror = "http:%s" % link_mirror

	return link_mirror

def recognize_title(title):
	title = (
		title
		.replace(" Serie Tv", "")
		.replace(" Serie TV", "")
		.replace(" streaming", "")
		.replace("la Serie", "La Serie")
	)

	return title

def get_domain(link):
	link = (
		link
		.split(".")[0]
		.split("//")[1]
	)

	return link

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

	if "open" in url:
		url = parse.find("iframe").get("src")

	elif "wss" in url:
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

	try:
		url = (
			body.text
			.split("MDCore.share_fb('")[1]
			.split("'")[0]
		)
	except IndexError:
		parse = BeautifulSoup(body.text, "html.parser")

		url = (
			str(
				parse.find_all("script")[4]
			)
			.split("href\",\"")[2]
			.split("\"")[0]
		)

	return url

def fasturl_decode(url):
	url = get(url).url
	return url

def linkhub_decode(url):
	body = get(url).text
	parse = BeautifulSoup(body, "html.parser")

	href = (
		parse
		.find("a", id = "get_btn")
		.get("href")[2:]
	)

	url = "https://www.linkhub.icu%s" % href
	body = get(url).text
	parse = BeautifulSoup(body, "html.parser")

	url = (
		parse
		.find("div", id = "text-url")
		.find("a")
		.get("href")
	) 

	return url

def rapidcrypt_decode(url):
	body = get(url).text
	parse = BeautifulSoup(body, "html.parser")

	url = (
		parse
		.find("a", class_ = "push_button blue")
		.get("href")
	)

	return url

def get_from_cloudflare(url):
	url = recognize_link(
		url.split("https:")[2]
	)

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
	link = link.replace(" ", "")

	c_supported = [
		"", "fasturl", "buckler",
		"vcrypt", "snip", "linkhub", "rapidcrypt",
		"linkup", "gatustox", "cowner", "rweasy"
	]

	functions = [
		"", fasturl_decode, buckler_decode,
		vcrypt_decode, snip_decode, linkhub_decode,
		rapidcrypt_decode
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

		elif any(
			a in link
			for a in c_supported[indexed:]
		):
			link1 = link
			link = adfly_decode(link)

		for a in c_supported[1:indexed]:
			if a in link:
				link1 = link
				index = c_supported.index(a)
				link = functions[index](link)
				break

		times += 1

	return link
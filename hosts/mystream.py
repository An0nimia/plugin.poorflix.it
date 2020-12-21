#!/usr/bin/python
#code a lot inspired from mystream of Plugin for URLResolver, thanks a lot to the devs =) https://github.com/tvaddonsco/script.module.urlresolver/blob/master/lib/urlresolver/plugins/mystream.py

from requests import get
from re import search, DOTALL
from scrapers.utils import headers
from hosts.exceptions.exceptions import VideoNotAvalaible

class Metadata:
	def __init__(self):
		self.logo = None
		self.icon = "https://mystream.to/favicon.ico"

def decode(data):
	startpos = data.find('"\\""+') + 5
	endpos = data.find('"\\"")())()')
	first_group = data[startpos:endpos]
	pos = search(r"(\(!\[\]\+\"\"\)\[.+?\]\+)", first_group)

	if pos:
		first_group = (
			first_group
			.replace(pos.group(1), 'l')
			.replace('$.__+', 't')
			.replace('$._+', 'u')
			.replace('$._$+', 'o')
		)

		tmplist = []
		js = search(r'(\$={.+?});', data)

		if js:
			js_group = js.group(1)[3:][:-1]
			second_group = js_group.split(',')

			i = -1
			for x in second_group:
				a, b = x.split(':')

				if b == '++$':
					i += 1
					tmplist.append(("$.{}+".format(a), i))

				elif b == '(![]+"")[$]':
					tmplist.append(("$.{}+".format(a), 'false'[i]))

				elif b == '({}+"")[$]':
					tmplist.append(("$.{}+".format(a), '[object Object]'[i]))

				elif b == '($[$]+"")[$]':
					tmplist.append(("$.{}+".format(a), 'undefined'[i]))

				elif b == '(!""+"")[$]':
					tmplist.append(("$.{}+".format(a), 'true'[i]))

			tmplist = sorted(tmplist, key = lambda z: str(z[1]))

			for x in tmplist:
				first_group = first_group.replace(x[0], str(x[1]))

			first_group = (
				first_group
				.replace('\\"', '\\')
				.replace("\"\\\\\\\\\"", "\\\\")
				.replace('\\"', '\\')
				.replace('"', '')
				.replace("+", "")
			)

		try:
			final_data = first_group.encode('ascii').decode('unicode-escape').encode('ascii').decode('unicode-escape')
			return final_data
		except:
			return False

def get_emb(url):
	if not "embed" in url:
		ids = url.split("/")[-1]
		url = "https://embed.mystream.to/%s" % ids

	return url

def get_video(url, referer):
	url = get_emb(url)
	headers['Referer'] = referer
	body = get(url, headers = headers).text

	try:
		match = search(r'(\$=.+?;)\s*<', body, DOTALL).group(1)
	except AttributeError:
		raise VideoNotAvalaible(url)

	sdata = decode(match)
	video_url = search(r"src',\s*'([^']+)", sdata).group(1)
	return video_url
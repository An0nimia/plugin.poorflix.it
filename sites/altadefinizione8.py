#!/usr/bin/python

from hosts import hosts
from sys import version_info
from bs4 import BeautifulSoup
from requests import post, get
from hosts.exceptions.exceptions import VideoNotAvalaible

from scrapers.utils import (
	recognize_link, recognize_mirror,
	m_identify, get_domain, headers
)

try:
	from utils import new_way
except ImportError:
	from sites.utils import new_way

host = "https://www.altadefinizione.name/"
excapes = ["Back", "back", ""]
timeout = 4
is_cloudflare = False

if version_info.major < 3:
	input = raw_input

def search_film(film_to_search):
	search_data = {
		"story": film_to_search,
		"do": "search",
		"subaction": "search",
		"titleonly": "3"
	}

	body = post(
		host,
		params = search_data,
		headers = headers,
		timeout = timeout
	).text

	parsing = BeautifulSoup(body, "html.parser")

	json = {
		"results": []
	}

	how = json['results']

	for a in parsing.find_all("div", class_ = "col-lg-3 col-md-3 col-xs-4"):
		image = a.find("img").get("src")
		link = a.find("a").get("href")
		title = a.find("h2").get_text()

		data = {
			"title": title,
			"link": link,
			"image": host + image
		}

		how.append(data)

	return json

def search_mirrors(film_to_see):
	try:
		json = new_way(film_to_see)
		return json
	except:
		pass

	domain = get_domain(film_to_see)
	body = get(film_to_see, headers = headers).text
	parsing = BeautifulSoup(body, "html.parser")
	mirrors = parsing.find("ul", id = "mirrors")

	json = {
		"results": []
	}

	datas = json['results']

	for a in mirrors.find_all("li"):
		c = a.find("a")

		if not c:
			continue

		mirror = recognize_mirror(
			c.get_text()
		)

		try:
			hosts[mirror]
			quality = "720p"

			link_mirror = recognize_link(
				c.get("data-target")
			)

			data = {
				"mirror": mirror,
				"quality": quality,
				"link": link_mirror,
				"domain": domain
			}

			datas.append(data)
		except KeyError:
			pass

	return json

def identify(info):
	link = info['link']
	mirror = info['mirror']
	domain = info['domain']
	link = m_identify(link)
	return hosts[mirror].get_video(link, domain)

def menu():
	while True:
		try:
			ans = input("Type the film title which you would search: ")
			result = search_film(ans)['results']

			while True:
				for a in range(
					len(result)
				):
					print(
						"%d): %s" % 
						(
							a + 1,
							result[a]['title']
						)
					)

				ans = input("What film do you want to see?: ")

				if ans in excapes:
					break

				index = int(ans) - 1
				film_to_see = result[index]['link']
				datas = search_mirrors(film_to_see)['results']

				while True:
					for a in range(
						len(datas)
					):
						print(
							"%s): %s (%s)"
							% (
								a + 1,
								datas[a]['mirror'],
								datas[a]['quality']
							)
						)

					ans = input("What film do you want to see?: ")

					if ans in excapes:
						break

					index = int(ans) - 1

					try:
						video = identify(datas[index])
					except VideoNotAvalaible as a:
						print(a)
						continue

					print(video)
		except KeyboardInterrupt:
			break

if __name__ == "__main__":
	menu()
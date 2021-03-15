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

host = "https://altadefinizione01.house/"
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

	for a in parsing.find_all("div", class_ = "col-lg-3 col-md-3 col-sm-4 col-xs-6 col-item"):
		image = host + a.find("img").get("src")
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
	domain = get_domain(film_to_see)
	body = get(film_to_see, headers = headers).text
	parsing = BeautifulSoup(body, "html.parser")
	mirrors = parsing.find("ul", class_ = "playernav")

	json = {
		"results": []
	}

	datas = json['results']

	for a in mirrors.find_all("li"):
		mirror = recognize_mirror(
			a.get_text()[1:-1]
		)

		try:
			hosts[mirror]

			link_mirror = recognize_link(
				a.find("a").get("data-target")
			)

			data = {
				"mirror": mirror,
				"quality": "720p",
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
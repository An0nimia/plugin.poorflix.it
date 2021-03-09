#!/usr/bin/python

from hosts import hosts
from sys import version_info
from bs4 import BeautifulSoup
from requests import post, get
from hosts.exceptions.exceptions import VideoNotAvalaible

from scrapers.utils import (
	recognize_link, recognize_mirror,
	m_identify, decode_middle_encrypted,
	get_domain, headers
)

try:
	from utils import new_way
except ImportError:
	from sites.utils import new_way	

host = "https://cineblog01.bid/"
excapes = ["Back", "back", ""]
timeout = 4
is_cloudflare = False

if version_info.major < 3:
	input = raw_input

def search_film(film_to_search):
	search_data = {
		"story": film_to_search,
		"do": "search",
		"subaction": "search"
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

	for a in parsing.find_all("div", class_ = "story-cover"):
		image = host + a.find("img").get("data-src")
		some = a.find("a")
		link = some.get("href")
		title = some.get("title")

		data = {
			"title": title,
			"link": link,
			"image": image
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
	parsing = parsing.find("div", class_ = "col-xs-6 col-md-4")
	array = parsing.find_all("a")
	del array[0]

	json = {
		"results": []
	}

	datas = json['results']

	for a in array:

		link_enc = (
			a
			.get("href")
			.split("link=")[1]
			.split("&")[0]
		)

		link_mirror = recognize_link(
			decode_middle_encrypted(link_enc)
		)

		mirror = recognize_mirror(
			a
			.get_text()
			.lower()
		)

		quality = "720p"

		try:
			hosts[mirror]

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
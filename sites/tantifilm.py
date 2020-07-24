#!/usr/bin/python

from hosts import hosts
from requests import get
from sys import version_info
from bs4 import BeautifulSoup

host = "https://www.tantifilm.cam/"
excapes = ["Back", "back", ""]

if version_info.major < 3:
	input = raw_input

def search_film(film_to_search):
	search_url = "{}?s={}".format(host, film_to_search)
	body = get(search_url).text
	parsing = BeautifulSoup(body, "html.parser")

	json = {
		"results": []
	}

	how = json['results']

	for a in parsing.find_all("div", class_ = "film film-2"):
		image = a.find("img").get("src")
		link = a.find("a").get("href")
		title = a.find("p").get_text()

		data = {
			"title": title,
			"link": link,
			"image": image
		}

		how.append(data)

	return json

def search_mirrors(film_to_see):
	body = get(film_to_see).text
	parsing = BeautifulSoup(body, "html.parser")
	mirrors = []

	for a in parsing.find_all("li", id = "wpwm-tabmob"):
		mirror = (
			a
			.find("a")
			.get_text()
			.split(" ")[0]
			.lower()
		)

		mirrors.append(mirror)

	json = {
		"results": []
	}

	datas = json['results']
	array = parsing.find_all("div", class_ = "float-left")

	for a in range(
		len(array)
	):

		link_mirror = (
			array[a]
			.find("iframe")
			.get("src")
		)

		quality = "720p"
		mirror = mirrors[a]

		try:
			hosts[mirror]

			if not link_mirror.startswith("http"):
				link_mirror = "http:%s" % link_mirror 

			data = {
				"mirror": mirror,
				"quality": quality,
				"link": link_mirror
			}

			datas.append(data)
		except KeyError:
			pass

	return json

def identify(info):
	link = info['link']
	mirror = info['mirror']
	return hosts[mirror](link)

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
					video = identify(datas[index])
					print(video)
		except KeyboardInterrupt:
			break

if __name__ == "__main__":
	menu()
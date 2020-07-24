#!/usr/bin/python

from hosts import hosts
from sys import version_info
from bs4 import BeautifulSoup
from requests import post, get

host = "https://altadefinizione01.bid/"
excapes = ["Back", "back", ""]

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
		timeout = 8
	).text

	parsing = BeautifulSoup(body, "html.parser")

	json = {
		"results": []
	}

	how = json['results']

	for a in parsing.find_all("div", class_ = "cover_kapsul ml-mask"):
		image = a.find("img").get("data-src")
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
	body = get(film_to_see).text
	parsing = BeautifulSoup(body, "html.parser")
	mirrors = parsing.find_all("ul", class_ = "host")[1]

	json = {
		"results": []
	}

	datas = json['results']

	for a in mirrors.find_all("a"):
		mirror = (
			a
			.find("span", class_ = "b")
			.get_text()
			.lower()[1:]
			.split(" ")[0]
		)

		link_mirror = a.get("data-link")
		quality = a.find("span", class_ = "d").get_text()

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
	return hosts[mirror].get_video(link)

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
#!/usr/bin/python

from hosts import hosts
from requests import get
from sys import version_info
from bs4 import BeautifulSoup
from hosts.exceptions.exceptions import VideoNotAvalaible

from scrapers.utils import (
	recognize_link, recognize_mirror, m_identify
)

host = "https://www.piratestreaming.movie/"
excapes = ["Back", "back", ""]
timeout = 4

if version_info.major < 3:
	input = raw_input

def search(to_search):
	search_url = "{}?s={}".format(host, to_search)
	body = get(search_url, timeout = timeout).text
	parsing = BeautifulSoup(body, "html.parser")

	json = {
		"results": []
	}

	how = json['results']

	for a in parsing.find_all("div", class_ = "container-index-post col-xs-4 col-sm-3 col-md-2-5 col-lg-2"):
		image = a.find("img").get("src")
		link = a.find("a").get("href")
		title = a.find("h2").get_text()

		data = {
			"title": title,
			"link": link,
			"image": image
		}

		how.append(data)

	return json

def search_film(film_to_search):
	json = search(film_to_search)
	results = json['results']

	for a in results:
		body = get(a['link']).text
		parsing = BeautifulSoup(body, "html.parser")
		iframes = parsing.find_all("iframe")

		if not iframes:
			results.remove(a)

	return json

def search_mirrors(film_to_see):
	body = get(film_to_see).text
	parsing = BeautifulSoup(body, "html.parser")
	iframes = parsing.find_all("iframe")
	mirrors = parsing.find_all("h3")
	avalaible_mirrors = []

	for a in mirrors:
		try:
			mirror = recognize_mirror(
				a
				.get_text()
				.split("su ")[1]
			)
		except IndexError:
			index = mirrors.index(a)
			del iframes[index]
			continue

		avalaible_mirrors.append(mirror)

	json = {
		"results": []
	}

	datas = json['results']

	for a in range(
		len(iframes)
	):
		mirror = avalaible_mirrors[a]

		try:
			hosts[mirror]
			quality = "720p"
			link_mirror = iframes[a].get("src")

			data = {
				"mirror": mirror,
				"quality": quality,
				"link": link_mirror
			}

			datas.append(data)
		except KeyError:
			pass

	return json

def search_serie(serie_to_search):
	json = search(serie_to_search)
	results = json['results']

	for a in results:
		body = get(a['link']).text
		parsing = BeautifulSoup(body, "html.parser")
		titles = parsing.find_all("div", class_ = "su-spoiler-title")

		if not titles:
			results.remove(a)

	return json

def seasons(serie_to_see):
	body = get(serie_to_see).text
	parsing = BeautifulSoup(body, "html.parser")
	titles = parsing.find_all("div", class_ = "su-spoiler-title")
	episodes = parsing.find_all("div", class_ = "su-link-ep")

	episodes_per_season = [
		[] for a in titles
	]

	for a in episodes:
		title = a.find("span").get_text()

		season = (
			title
			.split("x")[0]
			.replace(" ", "")
		)

		index = int(season) - 1
		episodes_per_season[index].append(a)

	json = {
		"results": []
	}

	datas = json['results']

	for a in range(
		len(titles)
	):
		title_season = titles[a].get_text()[1:]

		datas.append(
			{
				"title": "{} {}".format(title_season, a + 1),
				"episodes": []
			}
		)

		list_episodes_season = episodes_per_season[a]
		how = datas[a]['episodes']

		for b in list_episodes_season:
			episode = b.find("span").get_text()

			infos = {
				"episode": episode,
				"mirrors": []
			}

			for c in b.find_all("a"):
				mirror = recognize_mirror(
					c.get_text()[1:-1]
				)

				how1 = infos['mirrors']

				try:
					hosts[mirror]

					link_mirror = recognize_link(
						c.get("newlink")
					)

					data = {
						"mirror": mirror,
						"quality": "720p",
						"link": link_mirror
					}

					how1.append(data)
				except KeyError:
					pass

			how.append(infos)

	return json

def identify(info):
	link = info['link']
	mirror = info['mirror']
	link = m_identify(link)
	return hosts[mirror].get_video(link)

def f_menu():
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

def s_menu():
	while True:
		try:
			ans = input("Type the serie title which you would search: ")
			result = search_serie(ans)['results']

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

				ans = input("What serie do you want to see?: ")

				if ans in excapes:
					break

				index = int(ans) - 1
				serie_to_see = result[index]['link']
				seasonss = seasons(serie_to_see)['results']

				while True:
					for a in range(
						len(seasonss)
					):
						print(
							"%d): %s" % 
							(
								a + 1,
								seasonss[a]['title']
							)
						)

					ans = input("Which season do you want to see?: ")

					if ans in excapes:
						break

					index = int(ans) - 1
					episodes = seasonss[index]['episodes']

					while True:
						for a in range(
							len(episodes)
						):
							print(
								"%d): %s" % 
								(
									a + 1,
									episodes[a]['episode']
								)
							)

						ans = input("Which episode do you want to see?: ")

						if ans in excapes:
							break

						index = int(ans) - 1
						mirrors = episodes[index]['mirrors']

						while True:
							for a in range(
								len(mirrors)
							):
								print(
									"%s): %s (%s)"
									% (
										a + 1,
										mirrors[a]['mirror'],
										mirrors[a]['quality']
									)
								)

							ans = input("What service do you want to see?: ")

							if ans in excapes:
								break

							index = int(ans) - 1

							try:
								video = identify(mirrors[index])
							except VideoNotAvalaible as a:
								print(a)
								continue

							print(video)
		except KeyboardInterrupt:
			break

def menu():
	print("1): Film")
	print("2): Serie Tv")
	ans = input("Choose: ")

	if ans == "1":
		f_menu()
	
	elif ans == "2":
		s_menu()

if __name__ == "__main__":
	menu()
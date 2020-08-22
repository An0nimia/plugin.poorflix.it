#!/usr/bin/python

from hosts import hosts
from requests import get
from sys import version_info
from bs4 import BeautifulSoup
from hosts.exceptions.exceptions import VideoNotAvalaible

from scrapers.utils import (
	recognize_mirror, m_identify, get_domain
)

host = "https://www.guardaserie.fit/"
excapes = ["Back", "back", ""]
timeout = 4

if version_info.major < 3:
	input = raw_input

def search_serie(serie_to_search):
	search_url = "{}?s={}".format(host, serie_to_search)
	body = get(search_url, timeout = timeout).text
	parsing = BeautifulSoup(body, "html.parser")

	json = {
		"results": []
	}

	how = json['results']

	for a in parsing.find_all("div", class_ = "col-xs-6 col-sm-2-5"):
		link = a.find("a").get("href")
		image = a.find("img").get("src")
		title = a.find("p").get_text()

		data = {
			"title": title,
			"link": link,
			"image": image
		}

		how.append(data)

	return json

def seasons(serie_to_see):
	body = get(serie_to_see).text
	parsing = BeautifulSoup(body, "html.parser")

	titles = (
		parsing
		.find("ul", class_ = "ul-list-seasons")
		.find_all("li")
	)

	del titles[-1]

	episodes = (
		parsing
		.find("div", class_ = "container container-row-stagioni")
		.find_all("div", class_ = "row")
	)

	json = {
		"results": []
	}

	datas = json['results']

	for a in range(
		len(titles)
	):
		title_season = (
			titles[a]
			.find("a")
			.get_text()[1:-1]
		)

		datas.append(
			{
				"title": title_season,
				"episodes": []
			}
		)

		list_episodes_season = episodes[a].find_all("div", class_ = "col-xs-6 col-sm-3")
		how = datas[a]['episodes']

		for b in list_episodes_season:
			episode = (
				b
				.find("div", class_ = "number-episodes-on-img")
				.get_text()[1:]
			)

			episode += " {}".format(
				b.find("span").get_text()
			)

			infos = {
				"episode": episode,
				"mirrors": []
			}

			how1 = infos['mirrors']
			where = b.find("span", class_ = "player-overlay")

			for c in range(1, 6):
				if c == 1:
					getter = "meta-embed"
				else:
					getter = "meta-embed%d" % c

				link = where.get(getter)

				if link == "":
					continue

				link_mirror = m_identify(link)
				mirror = get_domain(link_mirror)

				try:
					hosts[mirror]

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
	return hosts[mirror].get_video(link)

def menu():
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

if __name__ == "__main__":
	menu()
#!/usr/bin/python
# -*- coding: utf-8 -*-

from hosts import hosts
from requests import get
from sys import version_info
from bs4 import BeautifulSoup
from hosts.exceptions.exceptions import VideoNotAvalaible

from scrapers.utils import (
	recognize_link, recognize_mirror,
	recognize_title, m_identify, get_domain
)

host = "https://www.eurostreaming.camp/"
excapes = ["Back", "back", ""]
timeout = 4
is_cloudflare = False

if version_info.major < 3:
	input = raw_input
	special_char = "–".decode("utf-8")
else:
	special_char = "–"

def search_serie(serie_to_search):
	search_url = "{}?s={}".format(host, serie_to_search)
	body = get(search_url, timeout = timeout).text
	parsing = BeautifulSoup(body, "html.parser")

	json = {
		"results": []
	}

	how = json['results']

	for a in parsing.find_all("div", class_ = "container-index-post col-xs-6 col-sm-4 col-md-2-5 col-lg-2-5"):
		image = a.find("img").get("src")
		link = a.find("a").get("href")

		title = recognize_title(
			a
			.find("h2")
			.get_text()
		)

		data = {
			"title": title,
			"link": link,
			"image": image
		}

		how.append(data)

	return json

def seasons(serie_to_see):
	domain = get_domain(serie_to_see)
	body = get(serie_to_see).text
	parsing = BeautifulSoup(body, "html.parser")
	titles = parsing.find_all("div", class_ = "su-spoiler-title")
	episodes = parsing.find_all("div", class_ = "su-spoiler-content")

	json = {
		"results": []
	}

	datas = json['results']

	for a in range(
		len(titles)
	):
		title_season = titles[a].get_text()[2:]

		datas.append(
			{
				"title": title_season,
				"episodes": []
			}
		)

		how = datas[a]['episodes']
		list_episodes_season = episodes[a]

		for b in list_episodes_season.find_all("div"):
			episode = b.find("a").get_text()

			infos = {
				"episode": episode,
				"mirrors": []
			}

			how1 = infos['mirrors']
			times = True

			for c in b.find_all("a"):
				if times:
					mirror = "speedvideo"
					times = False
				else:
					mirror = recognize_mirror(
						c.get_text()
					)

				link_mirror = c.get("newlink")

				if not link_mirror:
					link_mirror = None
				else:
					link_mirror = recognize_link(link_mirror)

				try:
					hosts[mirror]

					data = {
						"mirror": mirror,
						"quality": "720p",
						"link": link_mirror,
						"domain": domain
					}

					how1.append(data)
				except KeyError:
					continue

			how.append(infos)

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
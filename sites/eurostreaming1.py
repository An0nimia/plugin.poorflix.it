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

host = "https://eurostreaming.page/"
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

	for a in parsing.find_all("div", class_ = "post-thumb"):
		image = a.find("img").get("src")
		some = a.find("a")
		link = some.get("href")

		title = recognize_title(
			some.get("title")
		)

		data = {
			"title": title,
			"link": link,
			"image": image
		}

		how.append(data)

	return json

def is_episodes_page(link):
	body = get(link).text
	parsing = BeautifulSoup(body, "html.parser")

	if "CLICCA QUI" in str(parsing):
		try:
			link = (
				parsing
				.find("div", class_ = "entry-content")
				.find_all("a")[-1]
				.get("href")
			)

			if not host in link:
				raise AttributeError("")

		except (AttributeError, IndexError):
			for a in parsing.find_all("script"):
				c = str(a)

				if "go_to" in c:
					link = (
						c
						.split("\"go_to\":\"")[1]
						.split("\"")[0]
						.replace("\\", "")
					)

					break

	return link

def seasons(serie_to_see):
	serie_to_see = is_episodes_page(serie_to_see)
	domain = get_domain(serie_to_see)
	body = get(serie_to_see).text
	parsing = BeautifulSoup(body, "html.parser")
	titles = parsing.find_all("div", class_ = "su-spoiler-title")
	episodes = parsing.find_all("div", class_ = "su-spoiler-content su-u-clearfix su-u-trim")

	json = {
		"results": []
	}

	datas = json['results']

	for a in range(
		len(titles)
	):
		title_season = titles[a].get_text()

		datas.append(
			{
				"title": title_season,
				"episodes": []
			}
		)

		list_episodes_season = episodes[a]
		links = []

		for b in list_episodes_season.find_all("a"):
			mirror = recognize_mirror(
				b.get_text()
			)

			link_mirror = b.get("href")

			if not link_mirror:
				link_mirror = None
			else:
				link_mirror = recognize_link(link_mirror)

			links.append(
				("720p", mirror, link_mirror)
			)

		title_episodes_season = (
			list_episodes_season
			.get_text()
			.split("\n")
		)

		del title_episodes_season[0]
		del title_episodes_season[-1]
		how = datas[a]['episodes']

		for episode in title_episodes_season:
			episode_string_splited = episode.split(special_char)
			episode = episode_string_splited[0]
			del episode_string_splited[0]

			infos = {
				"episode": episode,
				"mirrors": []
			}

			how1 = infos['mirrors']
			length_avalaible_mirrors = len(episode_string_splited)

			for c in range(length_avalaible_mirrors):
				try:
					mirror = links[0][1]

					c_mirror = recognize_mirror(
						episode_string_splited[c]
						.replace(" ", "")
					)

					if c_mirror != mirror:
						continue

					hosts[mirror]

					data = {
						"mirror": mirror,
						"quality": links[0][0],
						"link": links[0][2],
						"domain": domain
					}

					how1.append(data)

				except KeyError:
					pass

				except IndexError:
					break

				del links[0]

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
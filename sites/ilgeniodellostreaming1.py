#!/usr/bin/python
# -*- coding: utf-8 -*-

from hosts import hosts
from requests import get
from sys import version_info
from bs4 import BeautifulSoup
from scrapers.excape_cloudflare import ex_Cloudflare

from scrapers.utils import (
	recognize_link, recognize_mirror,
	m_identify, get_from_cloudflare, get_domain
)

host = "https://ilgeniodellostreaming.cat/"
excapes = ["Back", "back", ""]
timeout = 30
is_cloudflare = True

if version_info.major < 3:
	input = raw_input
	special_char = "–".decode("utf-8")
else:
	special_char = "–"

def search(to_search):
	search_url = "{}?s={}".format(host, to_search)

	if is_cloudflare:
		ex_cloud = ex_Cloudflare(search_url)
		body = ex_cloud.get_body(timeout)
	else:
		body = get(
			search_url,
			timeout = timeout
		).text

	parsing = BeautifulSoup(body, "html.parser")

	json = {
		"results": []
	}

	how = json['results']

	for a in parsing.find_all("div", class_ = "result-item"):
		image = a.find("img").get("src")
		some = a.find_all("a")[1]
		link = some.get("href")
		title = some.get_text()

		data = {
			"title": title,
			"link": link,
			"image": image
		}

		how.append(data)

	return json

def search_film(film_to_search):
	json = search(film_to_search)
	return json

def search_serie(serie_to_search):
	json = search(serie_to_search)
	return json

def search_mirrors(film_to_see):
	if is_cloudflare:
		film_to_see = get_from_cloudflare(film_to_see)

	domain = get_domain(film_to_see)
	body = get(film_to_see).text
	parsing = BeautifulSoup(body, "html.parser")
	parsing1 = parsing.find("ul", class_ = "idTabs")

	json = {
		"results": []
	}

	datas = json['results']

	for a in parsing1.find_all("a"):
		t_splitted = (
			a
			.get_text()
			.split(" ")
		)

		mirror = t_splitted[0].lower()
		quality = t_splitted[1]

		option_index = (
			a
			.get("href")
			.replace("#", "")
		)

		link_mirror = (
			parsing
			.find("div", id = option_index)
			.find("iframe")
			.get("src")
		)

		try:
			hosts[mirror]
			link_mirror = recognize_link(link_mirror)

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

def seasons(serie_to_see):
	body = get(serie_to_see).text
	domain = get_domain(serie_to_see)
	parsing = BeautifulSoup(body, "html.parser")
	titles = parsing.find_all("span", style = "color: #ff0000;")
	titles += parsing.find_all("span", style = "color: #3366ff;")
	episodes = parsing.find_all("p")[3:-1]

	for a in episodes:
		string = str(a)

		if any(
			b.get_text() in string
			for b in titles
		):

			episodes.remove(a)

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
				b.get_text().lower()
			)

			link_mirror = b.get("href")

			links.append(
				("720p", mirror, link_mirror)
			)

		manicomy = (
			list_episodes_season
			.get_text()
			.replace("\xa0", " ")
			.split(" ")
		)

		title_episodes_season = []

		while True:
			if len(manicomy) == 0:
				break

			ep_title = ""
			times = 0

			for some in manicomy:
				times += 1

				if special_char in some:
					ep_title = "{}{}{}".format(ep_title, special_char, some)
					title_episodes_season.append(ep_title)
					del manicomy[:times]
					break

				ep_title += "%s " % some

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
						.lower()
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
					video = identify(datas[index])
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
							video = identify(mirrors[index])
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
#!/usr/bin/python

from hosts import hosts
from requests import get
from sys import version_info
from bs4 import BeautifulSoup
from scrapers.utils import decode_middle_encrypted

host = "https://www.seriehd.digital/"
excapes = ["Back", "back", ""]

if version_info.major < 3:
	input = raw_input

def search_serie(serie_to_search):
	search_url = "{}?s={}".format(host, serie_to_search)
	body = get(search_url).text
	parsing = BeautifulSoup(body, "html.parser")

	json = {
		"results": []
	}

	how = json['results']

	for a in parsing.find_all("div", class_ = "col-xl-3 col-lg-3 col-md-3 col-sm-6 col-6"):
		link = a.find("a").get("href")
		image = a.find("img").get("src")
		title = a.find("h2").get_text()

		data = {
			"title": title,
			"link": link,
			"image": image
		}

		how.append(data)

	return json

def seasons(serie_to_see):
	body = get(serie_to_see).text

	link_api = (
		BeautifulSoup(body, "html.parser")
		.find("iframe")
		.get("src")
		.split("&")[0]
	)

	body = get(link_api).text

	parsing = (
		BeautifulSoup(body, "html.parser")
		.find("ul")
		.find_all("li")
	)

	n_seasons = [
		(
			"STAGIONE %d" % (a + 1),
			parsing[a].find("a").get("href")
		) for a in range(
			len(parsing)
		)
	]

	return n_seasons

def get_episodes(season):
	body = get(season).text

	parsing = (
		BeautifulSoup(body, "html.parser")
		.find_all("ul")[1]
		.find_all("li")
	)

	n_episodes = [
		(
			"EPISODIO %d" % (a + 1),
			parsing[a].find("a").get("href")
		) for a in range(
			len(parsing)
		)
	]

	return n_episodes

def get_mirrors(episode):
	body = get(episode).text

	parsing = (
		BeautifulSoup(body, "html.parser")
		.find("ul", class_ = "buttons-list d-flex")
		.find_all("li")
	)

	link_mirrors = []

	for a in parsing:
		usha = a.find("a")
		quality = a.find("a").get_text()
		link = usha.get("href")
		body = get(link).text

		mirrors = (
			BeautifulSoup(body, "html.parser")
			.find_all("ul", class_ = "buttons-list d-flex")[1]
			.find_all("li")
		)

		for b in mirrors:
			c = b.find("a")
			link = c.get("href")
			mirror = c.get_text().lower()
			body = get(link).text

			link_mirror = decode_middle_encrypted(
				BeautifulSoup(body, "html.parser")
				.find("iframe")
				.get("custom-src")
			)

			try:
				hosts[mirror]

				if link_mirror != "":
					link_mirrors.append(
						(quality, mirror, link_mirror)
					)
			except KeyError:
				pass

	return link_mirrors

def identify(link, mirror):
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
							video = identify(mirrors[index])
							print(video)
		except KeyboardInterrupt:
			break

if __name__ == "__main__":
	menu()
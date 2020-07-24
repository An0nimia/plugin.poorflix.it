#!/usr/bin/python

from hosts import hosts
from requests import get
from sys import version_info
from bs4 import BeautifulSoup

host = "https://animepertutti.com/"
excapes = ["Back", "back", ""]

if version_info.major < 3:
	input = raw_input

def search_serie(serie_to_search):
	search_url = "{}?s={}".format(host, serie_to_search)
	body = get(search_url).text
	parsing = BeautifulSoup(body, "html.parser").find_all("a", class_ = "mh-thumb-icon mh-thumb-icon-small-mobile")
	serie_images = []
	serie_links = []
	serie_titles = []

	for a in parsing:
		image = a.find("img").get("src")
		serie_images.append(image)
		title = a.get("title")
		serie_titles.append(title)
		link = a.get("href")
		serie_links.append(link)

	return serie_images, serie_links, serie_titles

def episodes(serie_to_see):
	body = get(serie_to_see).text

	try:
		num_episodes = int(
			BeautifulSoup(body, "html.parser")
			.find_all("span", class_ = "pagelink")[-1]
			.get_text()
		)
	except IndexError:
		num_episodes = 1

	episodes = []

	for a in range(1, num_episodes + 1):
		link = "{}/{}".format(serie_to_see, a)
		episode = "EPISODE %d" % a 

		episodes.append(
			(episode, link)
		)

	return episodes

def to_see(episode_to_see):
	body = get(episode_to_see).text
	mirrors = BeautifulSoup(body, "html.parser").find_all("a", rel = "noopener")
	link_mirrors = []

	for a in mirrors:
		mirror = a.get_text().lower()
		link = a.get("href")

		try:
			hosts[mirror]

			link_mirrors.append(
				("720p", mirror, link)
			)
		except KeyError:
			pass

	return link_mirrors

def identify(link, mirror):
	return hosts[mirror](link)

def menu():
	while True:
		try:
			ans = input("Type the serie title which you would search: ")
			serie_images, serie_links, serie_titles = search_serie(ans)

			while True:
				for a in range(
					len(serie_titles)
				):
					print(
						"%d): %s" % 
						(
							a + 1,
							serie_titles[a]
						)
					)

				ans = input("What serie do you want to see?: ")

				if ans in excapes:
					break
					
				index = int(ans) - 1
				serie_to_see = serie_links[index]
				episodess = episodes(serie_to_see)

				while True:
					for a in range(
						len(episodess)
					):
						print(
							"%d): %s" % 
							(
								a + 1,
								episodess[a][0]
							)
						)

					ans = input("Which season do you want to see?: ")

					if ans in excapes:
						break

					index = int(ans) - 1

					to_seee = to_see(
						episodess[index][1]
					)

					while True:
						for a in range(
							len(to_seee)
						):
							print(
								"%s): %s (%s)"
								% (
									a + 1,
									to_seee[a][1],
									to_seee[a][0]
								)
							)

						ans = input("What service do you want to use?: ")

						if ans in excapes:
							break

						index = int(ans) - 1
						video = identify(to_seee[index][2], to_seee[index][1])
						print(video)
		except KeyboardInterrupt:
			break

if __name__ == "__main__":
	menu()
#!/usr/bin/python

from hosts import hosts
from requests import get
from sys import version_info
from bs4 import BeautifulSoup

host = "https://www.serietvu.link/"
excapes = ["Back", "back", ""]

if version_info.major < 3:
	input = raw_input

def search_serie(serie_to_search):
	search_url = "{}?s={}".format(host, serie_to_search)
	body = get(search_url).text
	parsing = BeautifulSoup(body, "html.parser")

	json = {
		"result": []
	}

	how = json['result']

	for a in parsing.find_all("div", class_ = "item"):
		some = a.find("a")
		link = some.get("href")
		image = some.get("data-original")
		
		title = (
			a.find("div", class_ = "title")
			.get_text()
			.split("\n")[0]
		)

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
	titles = parsing.find_all("option")
	episodes = parsing.find_all("div", class_ = "list")
	datas = []

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

		list_episodes_season = episodes[a].find_all("div", class_ = "item")
		how = datas[a]['episodes']
		
		for b in list_episodes_season:
			link_mirror = b.find("a").get("data-href")

			data = {
				"mirror": "speedvideo",
				"quality": "720p",
				"link": link_mirror
			}

			episode = b.find("div", class_ = "title").get_text()

			infos = {
				"episode": episode,
				"mirrors": [data]
			}

			how.append(infos)

	return datas

def identify(info):
	link = info['link']
	mirror = info['mirror']
	return hosts[mirror](link)

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
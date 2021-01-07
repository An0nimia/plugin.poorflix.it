#!/usr/bin/python

from hosts import hosts
from requests import get
from bs4 import BeautifulSoup
from scrapers.utils import get_domain, recognize_mirror, recognize_link

def new_way(film_to_see):
	domain = get_domain(film_to_see)
	body = get(film_to_see).text
	parsing = BeautifulSoup(body, "html.parser")

	iframe = (
		parsing
		.find_all("iframe")[1]
		.get("src")
	)

	body = get(iframe).text
	parsing = BeautifulSoup(body, "html.parser")

	json = {
		"results": []
	}

	datas = json['results']
	mirrors = parsing.find("ul", class_ = "storages")

	for a in mirrors.find_all("li"):
		mirror = recognize_mirror(
			a.get_text()
		)

		try:
			hosts[mirror]
			quality = "720p"

			link_mirror = recognize_link(
				a.get("data-link")
			)

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
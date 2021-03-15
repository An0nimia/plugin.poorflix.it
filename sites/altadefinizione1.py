#!/usr/bin/python

from hosts import hosts
from requests import get
from sys import version_info
from bs4 import BeautifulSoup
from scrapers.excape_cloudflare import ex_Cloudflare
from hosts.exceptions.exceptions import VideoNotAvalaible

from scrapers.utils import (
	recognize_link, recognize_mirror,
	m_identify, get_from_cloudflare,
	get_domain, decode_middle_encrypted, headers
)

host = "https://altadefinizione.capital/"
excapes = ["Back", "back", ""]
timeout = 30
is_cloudflare = False

if version_info.major < 3:
	input = raw_input

def search_film(film_to_search):
	search_url = "{}?s={}".format(host, film_to_search)

	if is_cloudflare:
		ex_cloud = ex_Cloudflare(search_url)
		body = ex_cloud.get_body(timeout)
	else:
		body = get(
			search_url,
			headers = headers,
			timeout = timeout
		).text

	parsing = BeautifulSoup(body, "html.parser")

	json = {
		"results": []
	}

	how = json['results']

	for a in parsing.find_all("div", class_ = "col-lg-3 col-md-4 col-xs-4 mb-30"):
		image = a.find("img").get("src")
		link = a.find("a").get("href")

		title = (
			a
			.find("h5")
			.get_text()
			.split(" [")[0]
		)

		data = {
			"title": title,
			"link": link,
			"image": image
		}

		how.append(data)

	return json

def search_mirrors(film_to_see):
	if is_cloudflare:
		film_to_see = get_from_cloudflare(film_to_see)

	body = get(film_to_see, headers = headers).text
	parse = BeautifulSoup(body, "html.parser")

	film_id_url = (
		parse
		.find("iframe", id = "iframeVid")
		.get("src")
		.split("&")[0]
	)

	domain = get_domain(film_id_url)
	body = get(film_id_url).text
	parse = BeautifulSoup(body, "html.parser")

	parsing = (
		parse
		.find("ul", class_ = "buttons-list d-flex")
		.find_all("li")
	)

	json = {
		"results": []
	}

	datas = json['results']

	for a in parsing:
		usha = a.find("a")
		quality = a.find("a").get_text()
		link = usha.get("href")
		body = get(link).text
		parse = BeautifulSoup(body, "html.parser")

		mirrors = (
			parse
			.find_all("ul", class_ = "buttons-list d-flex")[1]
			.find_all("li")
		)

		for b in mirrors:
			c = b.find("a")

			mirror = recognize_mirror(
				c.get_text()
			)

			try:
				hosts[mirror]
				link = c.get("href")
				body = get(link).text
				parse = BeautifulSoup(body, "html.parser")

				link_enc = decode_middle_encrypted(
					parse
					.find("iframe")
					.get("custom-src")
				)

				if not link_enc:
					continue

				link_mirror = recognize_link(link_enc)

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

def identify(info):
	link = info['link']
	mirror = info['mirror']
	domain = info['domain']
	#print(link, mirror, domain)
	link = m_identify(link)
	return hosts[mirror].get_video(link, domain)

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

					try:
						video = identify(datas[index])
					except VideoNotAvalaible as a:
						print(a)
						continue

					print(video)
		except KeyboardInterrupt:
			break

if __name__ == "__main__":
	menu()
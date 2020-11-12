#!/usr/bin/python

from requests import get
from importlib import import_module

where = "https://raw.githubusercontent.com/An0nimia/plugin.poorflix.it/master/sites.json"
sites = get(where).json()
sites_film = []
sites_serietv = []

films = [
	"altadefinizione7", "altadefinizione1", "ilgeniodellostreaming2",
	"altadefinizione3", "altadefinizione5", "ilgeniodellostreaming1"
	"altadefinizione4", "altadefinizione2", "piratestreaming", "cineblog01"
]

serietvs = [
	"eurostreaming1", "piratestreaming",
	"italiaserie", "serietvu"
]

for a in films:
	library = import_module("sites.%s" % a)
	c =  sites['sites'][a]
	library.host = c['link']
	library.timeout = c['timeout']
	library.is_cloudflare = c['is_cloudflare']
	sites_film.append(library)

for a in serietvs:
	library = import_module("sites.%s" % a)
	c = sites['sites'][a]
	library.host = c['link']
	library.timeout = c['timeout']
	library.is_cloudflare = c['is_cloudflare']
	sites_serietv.append(library)
#!/usr/bin/python

from requests import get
from importlib import import_module

where = "https://raw.githubusercontent.com/An0nimia/plugin.poorflix.it/master/sites.json"
sites = get(where).json()
sites_film = []
sites_serietv = []

films = [
	"altadefinizione7", "altadefinizione1",
	"altadefinizione3", "altadefinizione2", "altadefinizione6",
	"piratestreaming", "cineblog01", "altadefinizione8"
]

serietvs = [
	"eurostreaming1", "eurostreaming2", "eurostreaming3",
	"piratestreaming", "serietvu"
]

for a in films:
	library = import_module("sites.%s" % a)
	c = sites['sites'][a]
	works = c['works']

	if not works:
		continue

	library.host = c['link']
	library.timeout = c['timeout']
	library.is_cloudflare = c['is_cloudflare']
	sites_film.append(library)

for a in serietvs:
	library = import_module("sites.%s" % a)
	c = sites['sites'][a]
	works = c['works']

	if not works:
		continue

	library.host = c['link']
	library.timeout = c['timeout']
	library.is_cloudflare = c['is_cloudflare']
	sites_serietv.append(library)
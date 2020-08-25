#!/usr/bin/python

from requests import get
from importlib import import_module

where = "https://raw.githubusercontent.com/An0nimia/plugin.poorflix.it/master/sites.json"
sites = get(where).json()
sites_film = []
sites_serietv = []

films = [
	"altadefinizione7", "ilgeniodellostreaming2", "altadefinizione6",
	"altadefinizione3", "altadefinizione5", "altadefinizione4",
	"altadefinizione2", "cineblog01", "piratestreaming"
]

serietvs = [
	"eurostreaming1", "italiaserie",
	"piratestreaming", "serietvu"
]

for a in films:
	library = import_module("sites.%s" % a)
	library.host = sites['sites'][a]
	sites_film.append(library)

for a in serietvs:
	library = import_module("sites.%s" % a)
	library.host = sites['sites'][a]
	sites_serietv.append(library)
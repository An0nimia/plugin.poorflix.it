#!/usr/bin/python

from importlib import import_module

sites_film = []
sites_serietv = []

films = [
	"altadefinizione2", "altadefinizione3", "altadefinizione4",
	"altadefinizione6", "ilgeniodellostreaming2", "cineblog01"
]

serietvs = [
	"eurostreaming1"
]

for a in films:
	library = import_module("sites.%s" % a)
	sites_film.append(library)

for a in serietvs:
	library = import_module("sites.%s" % a)
	sites_serietv.append(library)
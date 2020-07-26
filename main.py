# -*- coding: utf-8 -*-
# Author: An0nimia

import xbmc
import xbmcgui
import settings
import xbmcaddon
import xbmcplugin
import get_media_metadata
from urllib import urlencode
from urlparse import parse_qsl
from sys import argv, version_info
from TheMovieDB import MovieDB, utils as moviedbutils

_url = argv[0]
_handle = int(argv[1])
moviedb = MovieDB(settings.movieDB_api_key)
addon = xbmcaddon.Addon()
addon_id = addon.getAddonInfo("id")
kodi_path = xbmc.translatePath("special://home")
addon_path = "%s/addons/" % kodi_path
image_path = "{}{}/%s".format(addon_path, addon_id)
messages = settings.messages
print(version_info)

def show_keyboard():
	keyboard = xbmc.Keyboard()
	keyboard.doModal()

	if keyboard.isConfirmed():
		topic = keyboard.getText()
		return topic

def get_url(**kwargs):
	url = "{}?{}".format(
		_url, urlencode(kwargs)
	)

	return url

def initialize(items):
	xbmcplugin.setPluginCategory(_handle, "Menu")

	for a in items:
		name = a[0]
		image = a[1]
		list_item = xbmcgui.ListItem(label = name)

		metadata = {
			"fanart": image_path % "back.jpg",
			"poster": image_path % image,
		}

		list_item.setArt(metadata)
		url = get_url(action = name)
		is_folder = True
		xbmcplugin.addDirectoryItem(_handle, url, list_item, is_folder)

	xbmcplugin.endOfDirectory(_handle)

def show_genres(which):
	xbmcplugin.setPluginCategory(_handle, "Result")
	xbmcplugin.setContent(_handle, which)

	if which == "movies":
		genres = moviedb.get_genre_movie("it")
	elif which == "tvshows":
		genres = moviedb.get_genre_tvshow("it")

	genres = genres['genres']

	for a in genres:
		name = a['name']
		list_item = xbmcgui.ListItem(label = name)

		metadata = {
			"fanart": image_path % "back.jpg",
			"poster": image_path % settings.movie_genres_image,
		}

		waste = {
			"mediatype": "movie"
		}

		list_item.setArt(metadata)
		list_item.setInfo("video", waste)

		url = get_url(
			action = "%sgenre" % which,
			genre = name
		)

		is_folder = True
		xbmcplugin.addDirectoryItem(_handle, url, list_item, is_folder)

	xbmcplugin.endOfDirectory(_handle)

def show_years(which):
	from datetime import datetime

	xbmcplugin.setPluginCategory(_handle, "Result")
	xbmcplugin.setContent(_handle, which)
	year = datetime.now().year

	for a in range(year, 1900, -1):
		c_year = str(a)
		list_item = xbmcgui.ListItem(label = c_year)

		metadata = {
			"fanart": image_path % "back.jpg",
			"poster": image_path % settings.movie_years_image,
		}

		waste = {
			"mediatype": "movie"
		}

		list_item.setArt(metadata)
		list_item.setInfo("video", waste)

		url = get_url(
			action = "%syear" % which,
			year = c_year
		)

		is_folder = True
		xbmcplugin.addDirectoryItem(_handle, url, list_item, is_folder)

	xbmcplugin.endOfDirectory(_handle)

def search_movie(mode = 0, topic = None, genre = None, year = None):
	xbmcplugin.setPluginCategory(_handle, "Result")
	xbmcplugin.setContent(_handle, "movies")

	if mode == 1:
		results = moviedb.get_movie_popular("it")
		message = messages['movie']['popular']
	elif mode == 2:
		results = moviedb.get_movie_top_rated("it")
		message = messages['movie']['top_rated']
	elif mode == 3:
		results = moviedb.get_movie_discover("it")
		message = messages['movie']['discover']
	elif mode == 4:
		results = moviedb.get_movie_discover("it", genres = [genre])
		message = messages['movie']['genre']
	elif mode == 5:
		results = moviedb.get_movie_discover("it", year = year)
		message = messages['movie']['year']
	else:
		results = moviedb.search_movie(topic, "it")
		message = messages['movie']['default']

	results = results['results']
	pDialog = xbmcgui.DialogProgress()

	pDialog.create(
		messages['start_search']['title'],
		messages['start_search']['text']
	)

	l_results = len(results)
	times = 1

	for result in results:
		if pDialog.iscanceled():
			return

		progress = 100 * times // l_results
		pDialog.update(progress, message)
		title = result['title']
		movie_id = result['id']
		list_item = xbmcgui.ListItem(label = title)
		metadata_art, metadata_movie, metadata_cast = get_media_metadata.get_infos_movie(movie_id)
		list_item.setArt(metadata_art)
		list_item.setCast(metadata_cast)
		list_item.setInfo("video", metadata_movie)

		try:
			url = get_url(
				action = "listing movies", title = title,
				metadata_art = metadata_art,
				metadata_movie = metadata_movie,
				metadata_cast = metadata_cast
			)

			is_folder = True
			xbmcplugin.addDirectoryItem(_handle, url, list_item, is_folder)
		except UnicodeEncodeError:
			pass

		times += 1

	pDialog.close()
	xbmcplugin.endOfDirectory(_handle)

def search_tvshow(mode = 0, topic = None, genre = None, year = None):
	xbmcplugin.setPluginCategory(_handle, "Result")
	xbmcplugin.setContent(_handle, "tvshows")

	if mode == 1:
		results = moviedb.get_tvshow_popular("it")
		message = messages['tvshow']['popular']
	elif mode == 2:
		results = moviedb.get_tvshow_top_rated("it")
		message = messages['tvshow']['top_rated']
	elif mode == 3:
		results = moviedb.get_tvshow_discover("it")
		message = messages['tvshow']['discover']
	elif mode == 4:
		results = moviedb.get_tvshow_discover("it", genres = [genre])
		message = messages['tvshow']['genre']
	elif mode == 5:
		results = moviedb.get_tvshow_discover("it", year = year)
		message = messages['tvshow']['year']
	else:
		results = moviedb.search_tvshow(topic, "it")
		message = messages['tvshow']['default']

	results = results['results']
	pDialog = xbmcgui.DialogProgress()

	pDialog.create(
		messages['start_search']['title'],
		messages['start_search']['text']
	)

	l_results = len(results)
	times = 1

	for result in results:
		if pDialog.iscanceled():
			return

		progress = 100 * times // l_results
		pDialog.update(progress, message)
		title = result['name']
		tvshow_id = result['id']
		list_item = xbmcgui.ListItem(label = title)
		data = get_media_metadata.get_infos_tvshow(tvshow_id)
		metadata_art = data[0]
		metadata_movie = data[1]
		metadata_cast = data[2]
		seasons = data[3]
		list_item.setArt(metadata_art)
		list_item.setCast(metadata_cast)
		list_item.setInfo("video", metadata_movie)

		try:
			url = get_url(
				action = "show seasons", title = title,
				tvshow_id = tvshow_id, seasons = seasons
			)

			is_folder = True
			xbmcplugin.addDirectoryItem(_handle, url, list_item, is_folder)
		except UnicodeEncodeError:
			pass

		times += 1

	pDialog.close()
	xbmcplugin.endOfDirectory(_handle)

def search_person(person, which):
	xbmcplugin.setPluginCategory(_handle, "Result")
	xbmcplugin.setContent(_handle, "people")
	results = moviedb.search_person(person, "it")['results']
	pDialog = xbmcgui.DialogProgress()

	pDialog.create(
		messages['start_search']['title'],
		messages['start_search']['text']
	)

	l_results = len(results)
	times = 1

	for result in results:
		if pDialog.iscanceled():
			return

		progress = 100 * times // l_results
		pDialog.update(progress, messages['person'])
		name = result['name']
		list_item = xbmcgui.ListItem(label = name)

		metadata_art = {
			"poster": moviedbutils.get_image(result['profile_path']),
			"fanart": image_path % "back.jpg"
		}

		waste = {
			"mediatype": "movie"
		}

		list_item.setArt(metadata_art)
		list_item.setInfo("video", waste)

		try:
			url = get_url(
				action = "show %s person" % which,
				person_id = result['id'],
			)

			is_folder = True
			xbmcplugin.addDirectoryItem(_handle, url, list_item, is_folder)
		except UnicodeEncodeError:
			pass

		times += 1

	xbmc.sleep(800)
	pDialog.close()
	xbmcplugin.endOfDirectory(_handle)

def list_film_person(person_id):
	xbmcplugin.setPluginCategory(_handle, "Result")
	xbmcplugin.setContent(_handle, "movies")
	results = moviedb.get_person_movie_credits(person_id, "it")['cast']
	pDialog = xbmcgui.DialogProgress()

	pDialog.create(
		messages['start_search']['title'],
		messages['start_search']['text']
	)

	l_results = len(results)
	times = 1

	for result in results:
		if pDialog.iscanceled():
			return

		progress = 100 * times // l_results
		pDialog.update(progress, messages['movie_list'])
		title = result['title']
		movie_id = result['id']
		list_item = xbmcgui.ListItem(label = title)
		metadata_art, metadata_movie, metadata_cast = get_media_metadata.get_infos_movie(movie_id)
		list_item.setArt(metadata_art)
		list_item.setCast(metadata_cast)
		list_item.setInfo("video", metadata_movie)

		try:
			url = get_url(
				action = "listing movies", title = title,
				metadata_art = metadata_art,
				metadata_movie = metadata_movie,
				metadata_cast = metadata_cast
			)

			is_folder = True
			xbmcplugin.addDirectoryItem(_handle, url, list_item, is_folder)
		except UnicodeEncodeError:
			pass

		times += 1

	pDialog.close()
	xbmcplugin.endOfDirectory(_handle)

def list_tvshow_person(person_id):
	xbmcplugin.setPluginCategory(_handle, "Result")
	xbmcplugin.setContent(_handle, "tvshows")
	results = moviedb.get_person_tvshow_credits(person_id, "it")['cast']
	pDialog = xbmcgui.DialogProgress()

	pDialog.create(
		messages['start_search']['title'],
		messages['start_search']['text']
	)

	l_results = len(results)
	times = 1

	for result in results:
		if pDialog.iscanceled():
			return

		progress = 100 * times // l_results
		pDialog.update(progress, messages['tvshow_list'])
		title = result['name']
		tvshow_id = result['id']
		list_item = xbmcgui.ListItem(label = title)
		data = get_media_metadata.get_infos_tvshow(tvshow_id)
		metadata_art = data[0]
		metadata_movie = data[1]
		metadata_cast = data[2]
		seasons = data[3]
		list_item.setArt(metadata_art)
		list_item.setCast(metadata_cast)
		list_item.setInfo("video", metadata_movie)

		try:
			url = get_url(
				action = "show seasons", title = title,
				tvshow_id = metadata_movie['setid'], seasons = seasons
			)

			is_folder = True
			xbmcplugin.addDirectoryItem(_handle, url, list_item, is_folder)
		except UnicodeEncodeError:
			pass

		times += 1

	pDialog.close()
	xbmcplugin.endOfDirectory(_handle)

def list_seasons(title, tvshow_id, seasons):
	seasons = eval(seasons)
	xbmcplugin.setPluginCategory(_handle, "Result")
	xbmcplugin.setContent(_handle, "tvshows")

	for a in seasons:
		metadata_art, metadata_movie, metadata_cast = get_media_metadata.get_infos_season(tvshow_id, a)
		list_item = xbmcgui.ListItem(label = metadata_movie['title'])
		metadata_art['fanart'] = image_path % "back.jpg"
		list_item.setArt(metadata_art)
		list_item.setCast(metadata_cast)
		list_item.setInfo("video", metadata_movie)

		url = get_url(
			action = "show episodes", title = title,
			tvshow_id = tvshow_id, season = a['season_number']
		)

		is_folder = True
		xbmcplugin.addDirectoryItem(_handle, url, list_item, is_folder)

	xbmcplugin.endOfDirectory(_handle)

def list_episodes(title, tvshow_id, season):
	xbmcplugin.setPluginCategory(_handle, "Result")
	xbmcplugin.setContent(_handle, "episodes")
	results = moviedb.get_season(tvshow_id, season, "it")['episodes']

	for a in results:
		list_item = xbmcgui.ListItem(label = a['name'])
		metadata_art, metadata_movie, metadata_cast = get_media_metadata.get_infos_episode(tvshow_id, a)
		metadata_art['fanart'] = image_path % "back.jpg"
		list_item.setArt(metadata_art)
		list_item.setCast(metadata_cast)
		list_item.setInfo("video", metadata_movie)

		url = get_url(
			action = "listing_tvshow",
			title = title,
			season = season,
			episode = a['episode_number'],
			metadata_art = metadata_art,
			metadata_movie = metadata_movie,
			metadata_cast = metadata_cast
		)

		is_folder = True
		xbmcplugin.addDirectoryItem(_handle, url, list_item, is_folder)

	xbmcplugin.endOfDirectory(_handle)

def list_mirros_episode(
	title, season,
	episode, metadata_art,
	metadata_movie, metadata_cast
):
	from sites import sites_serietv

	episode = int(episode)
	metadata_art = eval(metadata_art)
	metadata_art['fanart'] = image_path % "back.jpg"
	metadata_movie = eval(metadata_movie)
	metadata_cast = eval(metadata_cast)
	xbmcplugin.setPluginCategory(_handle, "Mirror")
	xbmcplugin.setContent(_handle, "tvshows")
	pDialog = xbmcgui.DialogProgress()

	pDialog.create(
		messages['start_search']['title'],
		messages['start_search']['text']
	)

	l_results = len(sites_serietv)
	times = 1
	mirrors = []

	for a in sites_serietv:
		if pDialog.iscanceled():
			return

		progress = 100 * times // l_results

		try:
			link = a.search_serie(title)['results'][0]['link']
			seasons = a.seasons(link)['results']

			for b in seasons:
				if season in b['title']:
					current_mirrors = b['episodes'][episode - 1]['mirrors']
					mirrors += current_mirrors

			pDialog.update(progress, messages['episode'])
		except IndexError:
			pass

		times += 1

	xbmc.sleep(800)
	pDialog.close()
	title = metadata_movie['title']
	del metadata_movie['title']

	for mirror in mirrors:
		list_item = xbmcgui.ListItem(
			label = "[B]{} | {}[/B]".format(
				mirror['mirror'], mirror['quality']
			)
		)

		list_item.setArt(metadata_art)
		list_item.setCast(metadata_cast)
		list_item.setInfo("video", metadata_movie)
		list_item.setProperty("IsPlayable", "true")
		list_item.addStreamInfo("codec", "h264")

		url = get_url(
			action = "play", video = mirror['link'],
			mirror =  mirror['mirror'], title = title
		)

		is_folder = False
		xbmcplugin.addDirectoryItem(_handle, url, list_item, is_folder)

	xbmcplugin.endOfDirectory(_handle)

def list_mirros_movie(title, metadata_art, metadata_movie, metadata_cast):
	from hosts import hosts
	from sites import sites_film

	metadata_art = eval(metadata_art)
	metadata_movie = eval(metadata_movie)
	metadata_cast = eval(metadata_cast)
	del metadata_movie['title']
	xbmcplugin.setPluginCategory(_handle, "Mirror")
	xbmcplugin.setContent(_handle, "movies")
	pDialog = xbmcgui.DialogProgress()

	pDialog.create(
		messages['start_search']['title'],
		messages['start_search']['text']
	)

	l_results = len(sites_film)
	times = 1
	mirrors = []

	qualities = [
		[0, "[COLOR red]0[/COLOR]", "360p"],
		[0, "[COLOR red]0[/COLOR]", "480p"],
		[0, "[COLOR red]0[/COLOR]", "720p"],
		[0, "[COLOR red]0[/COLOR]", "1080p"],
		[0, "[COLOR red]0[/COLOR]", "4k"],
		[0, "[COLOR red]0[/COLOR]"]
	]

	short_title = " ".join(
		title.split(" ")[0:]
	)

	for a in sites_film:
		if pDialog.iscanceled():
			return

		progress = 100 * times // l_results

		try:
			results = a.search_film(title)['results']

			for b in results:
				if short_title == b['title']:
					link = b['link']
					break

			current_mirrors = a.search_mirrors(link)['results']
		
			for b in current_mirrors:
				for c in qualities[:-1]:
					if b['quality'] == c[2]:
						c[0] += 1
						c[1] = "[COLOR green]%d[/COLOR]" % c[0]
						break

				alls = qualities[-1]
				alls[0] += 1
				alls[1] = "[COLOR green]%d[/COLOR]" % alls[0]

				new_string = (
					"4k: %s | 1080p: %s | 720p: %s | 480p: %s | 360p: %s | Total: %s"
					% (
						qualities[4][1],
						qualities[3][1],
						qualities[2][1],
						qualities[1][1],
						qualities[0][1],
						alls[1]
					)
				)

				pDialog.update(progress, new_string)

			mirrors += current_mirrors
		except (IndexError, AttributeError, UnboundLocalError):
			pass

		times += 1

	pDialog.close()

	for mirror in mirrors:
		list_item = xbmcgui.ListItem(
			label = "[B]{} | {}[/B]".format(
				mirror['mirror'], mirror['quality']
			)
		)

		source = mirror['mirror']
		icon = hosts[source].Metadata().icon
		metadata_art['icon'] = icon
		metadata_art['banner'] = icon
		list_item.setArt(metadata_art)
		list_item.setCast(metadata_cast)
		list_item.setInfo("video", metadata_movie)
		list_item.setProperty("IsPlayable", "true")
		list_item.addStreamInfo("codec", "h264")

		url = get_url(
			action = "play", video = mirror['link'],
			mirror =  mirror['mirror'], title = title
		)

		is_folder = False
		xbmcplugin.addDirectoryItem(_handle, url, list_item, is_folder)

	xbmcplugin.endOfDirectory(_handle)

def play_video(link, mirror, title):
	from hosts import hosts
	from scrapers.utils import m_identify
	from hosts.exceptions.exceptions import VideoNotAvalaible

	try:
		link = m_identify(link)
		path = hosts[mirror].get_video(link)

		play_item = xbmcgui.ListItem(
			path = path,
			label = title
		)

		xbmcplugin.setResolvedUrl(_handle, True, play_item)
	except VideoNotAvalaible:
		dialog = xbmcgui.Dialog()

		dialog = dialog.ok(
			messages['stream']['error_stream_title'],
			messages['stream']['error_stream_text']
		)

def router(paramstring):
	params = dict(
		parse_qsl(paramstring)
	)

	if params:
		if params['action'] == settings.menu_items[0][0]:
			initialize(settings.film_menu_items)

		elif params['action'] == settings.menu_items[1][0]:
			initialize(settings.tvshow_menu_items)

		elif params['action'] == settings.film_menu_items[0][0]:
			topic = show_keyboard()

			if not topic:
				return

			search_movie(topic = topic)

		elif params['action'] == settings.film_menu_items[1][0]:
			topic = show_keyboard()

			if not topic:
				return

			search_person(topic, "movies")

		elif params['action'] == settings.film_menu_items[2][0]:
			search_movie(1)

		elif params['action'] == settings.film_menu_items[3][0]:
			search_movie(2)

		elif params['action'] == settings.film_menu_items[4][0]:
			search_movie(3)

		elif params['action'] == settings.film_menu_items[5][0]:
			show_years("movies")

		elif params['action'] == "moviesyear":
			search_movie(5, year = params['year'])

		elif params['action'] == settings.film_menu_items[6][0]:
			show_genres("movies")

		elif params['action'] == "moviesgenre":
			search_movie(4, genre = params['genre'])

		elif params['action'] == settings.tvshow_menu_items[0][0]:
			topic = show_keyboard()

			if not topic:
				return

			search_tvshow(topic = topic)

		elif params['action'] == settings.tvshow_menu_items[1][0]:
			topic = show_keyboard()

			if not topic:
				return

			search_person(topic, "tvshows")

		elif params['action'] == settings.tvshow_menu_items[2][0]:
			search_tvshow(1)

		elif params['action'] == settings.tvshow_menu_items[3][0]:
			search_tvshow(2)

		elif params['action'] == settings.tvshow_menu_items[4][0]:
			search_tvshow(3)

		elif params['action'] == settings.tvshow_menu_items[5][0]:
			show_years("tvshows")

		elif params['action'] == "tvshowsyear":
			search_tvshow(5, year = params['year'])

		elif params['action'] == settings.tvshow_menu_items[6][0]:
			show_genres("tvshows")

		elif params['action'] == "tvshowsgenre":
			search_tvshow(4, genre = params['genre'])

		elif params['action'] == "show seasons":
			list_seasons(
				params['title'], params['tvshow_id'],
				params['seasons']
			)

		elif params['action'] == "show episodes":
			list_episodes(
				params['title'], params['tvshow_id'],
				params['season']
			)

		elif params['action'] == "show movies person":
			list_film_person(params['person_id'])

		elif params['action'] == "show tvshows person":
			list_tvshow_person(params['person_id'])

		elif params['action'] == "listing movies":
			list_mirros_movie(
				params['title'], params['metadata_art'],
				params['metadata_movie'], params['metadata_cast']
			)

		elif params['action'] == "listing_tvshow":
			list_mirros_episode(
				params['title'], params['season'],
				params['episode'], params['metadata_art'],
				params['metadata_movie'], params['metadata_cast']
			)

		elif params['action'] == "play":
			play_video(
				params['video'], params['mirror'],
				params['title']
			)
	else:
		initialize(settings.menu_items)

if __name__ == "__main__":
	router(argv[2][1:])
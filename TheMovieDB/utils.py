#!/usr/bin/python3

api_image = "https://image.tmdb.org/t/p/original%s"

def get_image(path):
	url = api_image % path
	return url

def get_genres(genres):
	genres_name = [
		a['name']
		for a in genres
	]

	return genres_name

def get_countries(countries):
	countries_name = [
		a['name']
		for a in countries
	]

	return countries_name

def get_companies(companies):
	companies_name = [
		a['name']
		for a in companies
	]

	return companies_name

def get_cast_tuple(cast):
	cast_tuple = [
		(a['name'], a['character'])
		for a in cast
	]

	return cast_tuple

def get_cast_dict(cast):
	cast_dict = []

	for a in cast:
		json = {
			"name": a['name'],
			"role": a['character'],
			"thumbnail": api_image % a['profile_path'],
			"order": a['order']
		}

		cast_dict.append(json)

	return cast_dict

def get_id(result, title, these):
	for a in result:
		try:
			c_title = a['original_title']
		except KeyError:
			c_title = a['name']

		if not c_title in these:
			movie_id = a['id']
			break

	return movie_id

def get_creators(creators):
	creators_name = [
		a['name']
		for a in creators
	]

	return creators_name
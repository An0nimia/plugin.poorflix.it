#!/usr/bin/python3

from requests import get

api_infos = "https://api.themoviedb.org/3%s"

class MovieDB:
	def __init__(self, api_key):
		self.api_key = api_key

	def search_movie(
		self, query,
		language = "en-US",
		page = 1,
		include_adult = False
	):
		params = (
			"?api_key=%s&language=%s&query=%s&page=%s&include_adult=%s"
			% (
				self.api_key,
				language,
				query,
				page,
				include_adult
			)
		)

		path = "/search/movie%s" % params
		url = api_infos % path
		result = get(url).json()
		return result

	def search_tvshow(
		self, query,
		language = "en-US",
		page = 1,
		include_adult = False
	):
		params = (
			"?api_key=%s&language=%s&query=%s&page=%s&include_adult=%s"
			% (
				self.api_key,
				language,
				query,
				page,
				include_adult
			)
		)

		path = "/search/tv%s" % params
		url = api_infos % path
		result = get(url).json()
		return result

	def search_person(
		self, query,
		language = "en-US",
		page = 1,
		include_adult = False
	):
		params = (
			"?api_key=%s&language=%s&query=%s&page=%s&include_adult=%s"
			% (
				self.api_key,
				language,
				query,
				page,
				include_adult
			)
		)

		path = "/search/person%s" % params
		url = api_infos % path
		result = get(url).json()
		return result

	def get_movie(self, movie_id, language = "en-US"):
		params = (
			"%s?api_key=%s&language=%s"
			% (
				movie_id,
				self.api_key,
				language
			)
		)

		path = "/movie/%s" % params
		url = api_infos % path
		result = get(url).json()
		return result

	def get_movie_popular(self, language = "en-US"):
		params = (
			"?api_key=%s&language=%s"
			% (
				self.api_key,
				language
			)
		)

		path = "/movie/popular%s" % params
		url = api_infos % path
		result = get(url).json()
		return result

	def get_movie_top_rated(self, language = "en-US"):
		params = (
			"?api_key=%s&language=%s"
			% (
				self.api_key,
				language
			)
		)

		path = "/movie/top_rated%s" % params
		url = api_infos % path
		result = get(url).json()
		return result

	def get_movie_discover(
		self,
		language = "en-US",
		year = None,
		genres = []
	):
		genres_ids = []

		if genres:
			avalaible_genres = self.get_genre_movie(language)['genres']

			for a in genres:
				for b in avalaible_genres:
					if b['name'] == a:
						genres_ids.append(b['id'])
						break

		genres = ", ".join(
			map(str, genres_ids)
		)

		params = (
			"?api_key=%s&language=%s&year=%s&with_genres=%s"
			% (
				self.api_key,
				language,
				year,
				genres
			)
		)

		path = "/discover/movie%s" % params
		url = api_infos % path
		result = get(url).json()
		return result

	def get_tvshow(self, tvshow_id, language = "en-US"):
		params = (
			"%s?api_key=%s&language=%s"
			% (
				tvshow_id,
				self.api_key,
				language
			)
		)

		path = "/tv/%s" % params
		url = api_infos % path
		result = get(url).json()
		return result

	def get_tvshow_popular(self, language = "en-US"):
		params = (
			"?api_key=%s&language=%s"
			% (
				self.api_key,
				language
			)
		)

		path = "/tv/popular%s" % params
		url = api_infos % path
		result = get(url).json()
		return result

	def get_tvshow_top_rated(self, language = "en-US"):
		params = (
			"?api_key=%s&language=%s"
			% (
				self.api_key,
				language
			)
		)

		path = "/tv/top_rated%s" % params
		url = api_infos % path
		result = get(url).json()
		return result

	def get_tvshow_discover(
		self,
		language = "en-US",
		year = None,
		genres = []
	):
		genres_ids = []

		if genres:
			avalaible_genres = self.get_genre_tvshow(language)['genres']

			for a in genres:
				for b in avalaible_genres:
					if b['name'] == a:
						genres_ids.append(b['id'])
						break

		genres = ", ".join(
			map(str, genres_ids)
		)

		params = (
			"?api_key=%s&language=%s&first_air_date_year=%s&with_genres=%s"
			% (
				self.api_key,
				language,
				year,
				genres
			)
		)

		path = "/discover/tv%s" % params
		url = api_infos % path
		result = get(url).json()
		return result

	def get_season(
		self, tvshow_id, season,
		language = "en-US"
	):
		params = (
			"%s?api_key=%s&language=%s"
			% (
				season,
				self.api_key,
				language
			)
		)

		path = "/tv/{}/season/{}".format(tvshow_id, params)
		url = api_infos % path
		result = get(url).json()
		return result

	def get_cast_movie(self, movie_id):
		params = "credits?api_key=%s" % self.api_key
		path = "/movie/{}/{}".format(movie_id, params)
		url = api_infos % path
		result = get(url).json()
		return result

	def get_cast_tvshow(self, tvshow_id):
		params = "credits?api_key=%s" % self.api_key
		path = "/tv/{}/{}".format(tvshow_id, params)
		url = api_infos % path
		result = get(url).json()
		return result

	def get_cast_season(
		self, tvshow_id, season,
		language = "en-US"
	):
		params = (
			"credits?api_key=%s&language=%s"
			% (
				self.api_key,
				language
			)
		)

		path = "/tv/{}/season/{}/{}".format(tvshow_id, season, params)
		url = api_infos % path
		result = get(url).json()
		return result

	def get_cast_episode(
		self, tvshow_id, 
		season, episode,
		language = "en-US"
	):
		params = (
			"credits?api_key=%s&language=%s"
			% (
				self.api_key,
				language
			)
		)

		path = (
			"/tv/{}/season/{}/episode/{}/{}".format(
				tvshow_id, season, episode, params
			)
		)

		url = api_infos % path
		result = get(url).json()
		return result

	def get_person_movie_credits(self, person_id, language = "en-US"):
		params = (
			"movie_credits?api_key=%s&language=%s"
			% (
				self.api_key,
				language
			)
		)

		path = "/person/{}/{}".format(person_id, params)
		url = api_infos % path
		result = get(url).json()
		return result

	def get_person_tvshow_credits(self, person_id, language = "en-US"):
		params = (
			"tv_credits?api_key=%s&language=%s"
			% (
				self.api_key,
				language
			)
		)

		path = "/person/{}/{}".format(person_id, params)
		url = api_infos % path
		result = get(url).json()
		return result

	def get_languages(self):
		params = "?api_key=%s" % self.api_key
		path = "/configuration/languages%s" % params
		url = api_infos % path
		result = get(url).json()
		return result

	def get_iso_language(self, language):
		result = self.get_languages()
		iso = result[0]['iso_639_1']

		for a in result:
			if a['english_name'] == language.capitalize():
				iso = a['iso_639_1']
				break

		return iso

	def get_genre_movie(self, language = "en-US"):
		params = (
			"?api_key=%s&language=%s"
			% (
				self.api_key,
				language
			)
		)

		path = "/genre/movie/list%s" % params
		url = api_infos % path
		result = get(url).json()
		return result

	def get_genre_tvshow(self, language = "en-US"):
		params = (
			"?api_key=%s&language=%s"
			% (
				self.api_key,
				language
			)
		)

		path = "/genre/tv/list%s" % params
		url = api_infos % path
		result = get(url).json()
		return result

#from pprint import pprint
#start = MovieDB("8804be4f30f706e9e0ec40c32d961635")
#pprint(start.get_tvshow_discover("it", 2019))
#pprint(start.get_tvshow("48866", "it"))
#film_id = start.get_person_movie_credits("118340")
#pprint(film_id)
from settings import movieDB_api_key
from TheMovieDB import MovieDB, utils as moviedbutils

moviedb = MovieDB(movieDB_api_key)

def get_infos_movie(movie_id):
	movie_data = moviedb.get_movie(movie_id, "it")
	cast_data = moviedb.get_cast_movie(movie_id)['cast']
	poster = moviedbutils.get_image(movie_data['poster_path'])
	fanart = moviedbutils.get_image(movie_data['backdrop_path'])

	metadata_art = {
		"poster": poster,
		"fanart": fanart
	}

	metadata_movie = {
		"genre": moviedbutils.get_genres(movie_data['genres']),
		"country": moviedbutils.get_countries(movie_data['production_countries']),
		"rating": movie_data['vote_average'],
		"plot": movie_data['overview'],
		"duration": movie_data['runtime'],
		"imdbnumber": movie_data['imdb_id'],
		"studio": moviedbutils.get_companies(movie_data['production_companies']),
		"tagline": movie_data['tagline'],
		"title": movie_data['original_title'],
		"aired": movie_data['release_date'],
		"votes": movie_data['vote_count'],
		"mediatype": "movie"
	}

	metadata_cast = moviedbutils.get_cast_dict(cast_data)
	return metadata_art, metadata_movie, metadata_cast

def get_infos_tvshow(tvshow_id):
	tvshow_data = moviedb.get_tvshow(tvshow_id, "it")
	cast_data = moviedb.get_cast_tvshow(tvshow_id)['cast']
	poster = moviedbutils.get_image(tvshow_data['poster_path'])
	fanart = moviedbutils.get_image(tvshow_data['backdrop_path'])

	metadata_art = {
		"poster": poster,
		"fanart": fanart
	}

	metadata_movie = {
		"episode": tvshow_data['number_of_episodes'],
		"season": tvshow_data['number_of_seasons'],
		"rating": tvshow_data['vote_average'],
		"plot": tvshow_data['overview'],
		"studio": moviedbutils.get_companies(tvshow_data['production_companies']),
		"writer": moviedbutils.get_creators(tvshow_data['created_by']),
		"tvshowtitle": tvshow_data['name'],
		"status": tvshow_data['status'],
		"aired": tvshow_data['first_air_date'],
		"votes": tvshow_data['vote_count'],
		"mediatype": "tvshow"
	}

	metadata_cast = moviedbutils.get_cast_dict(cast_data)
	seasons = tvshow_data['seasons']

	for a in seasons:
		if a['season_number'] < 1:
			seasons.remove(a)

	return metadata_art, metadata_movie, metadata_cast, seasons

def get_infos_season(tvshow_id, season):
	season_number = season['season_number']
	cast_data = moviedb.get_cast_season(tvshow_id, season_number)['cast']
	image_season = moviedbutils.get_image(season['poster_path'])

	metadata_art = {
		"poster": image_season
	}

	metadata_movie = {
		"episode": season['episode_count'],
		"season": 1,
		"plot": season['overview'],
		"title": season['name'],
		"aired": season['air_date'],
		"mediatype": "tvshow"
	}

	metadata_cast = moviedbutils.get_cast_dict(cast_data)
	return metadata_art, metadata_movie, metadata_cast

def get_infos_episode(tvshow_id, episode):
	season_number = episode['season_number']
	episode_number = episode['episode_number']
	cast_data = moviedb.get_cast_episode(tvshow_id, season_number, episode_number)['cast']
	image_episode = moviedbutils.get_image(episode['still_path'])

	metadata_art = {
		"thumb": image_episode
	}

	metadata_movie = {
		"rating": episode['vote_average'],
		"plot": episode['overview'],
		"title": episode['name'],
		"votes": episode['vote_count'],
		"aired": episode['air_date'],
		"mediatype": "episode"
	}

	metadata_cast = moviedbutils.get_cast_dict(cast_data)
	return metadata_art, metadata_movie, metadata_cast

def get_infos_person(person_id):
	result = moviedb.get_person(person_id)
	biography = result['biography']

	metadata = {
		"plot": biography,
		"mediatype": "movie"
	}

	return metadata
# -*- coding: utf-8 -*-

movie_genres_image = "images/genres.png"
tvshow_genres_image = "images/genres_tvshow.png"
movie_highly_rated_image = "images/highly-rated.png"
tvshow_highly_rated_image = "images/highly-rated_tvshow.png"
movie_most_popular_image = "images/most-popular.png"
tvshow_most_popular_image = "images/most-popular_tvshow.png"
movie_most_voted_image = "images/most-voted.png"
tvshow_most_voted_image = "images/most-voted_tvshow.png"
movie_image = "images/movies.png"
search_movie_image = "images/search_movie.png"
movie_search_people_image = "images/search_people.png"
tvshow_search_people_image = "images/search_people_tvshow.png"
search_tvshow_image = "images/search_tvshow.png"
tvshow_image = "images/tvshows.png"
movie_years_image = "images/years.png"
tvshow_years_image = "images/years_tvshow.png"
movieDB_api_key = "8804be4f30f706e9e0ec40c32d961635"

menu_items = [
	("Film", movie_image),
	("Serie TV", tvshow_image),
]

film_menu_items = [
	("Ricerca film", search_movie_image),
	("Ricerca persona film", movie_search_people_image),
	("Film famosi", movie_most_popular_image),
	("Film votati belli", movie_most_voted_image),
	("Scopri film", movie_highly_rated_image),
	("Film dell'anno ?", movie_years_image),
	("Film per genere", movie_genres_image)
]

tvshow_menu_items = [
	("Ricerca serie TV", search_tvshow_image),
	("Ricerca persona serie TV", tvshow_search_people_image),
	("Serie TV famosi", tvshow_most_popular_image),
	("Serie TV votati belli", tvshow_most_voted_image),
	("Scopri serie TV", tvshow_highly_rated_image),
	("Serie TV dell'anno ?", tvshow_years_image),
	("Serie TV per genere", tvshow_genres_image)
]

messages = {
	"start_search": {
		"title": "E' partito fratellì",
		"text": "Inizio ricerca..."
	},

	"movie": {
		"popular": "Ricerca film famosi in corso...",
		"top_rated": "Ricerca film più votati in corso...",
		"discover": "Oddio sto togliendo la coperta ai film. Capito? Sto scoprendo nuovi film =)",
		"genre": "Ricerca film per genere in corso...",
		"year": "Ricerca film per anno in corso...",
		"default": "Sto cercando film con questo titolo"
	},

	"tvshow": {
		"popular": "Ricerca serie tv famosi in corso...",
		"top_rated": "Ricerca serie tv più votati in corso...",
		"discover": "Cosa pensi che ripeterò la battuta?",
		"genre": "Ricerca serie tv per genere in corso...",
		"year": "Ricerca serie tv per anno in corso...",
		"default": "Sto cercando serie tv con questo titolo"
	},

	"stream": {
		"error_stream_title": "HO SFONDATO IL MURO",
		"error_stream_text": "MA FARES... STO C... DEVI FUNZIONARE"
	},

	"person": "Se cercavi Bugo, spoiler non c'è =)",
	"movie_list": "Ma quanto mi fai sgobbare?",
	"tvshow_list": "Stai per ritrovarti nella selva oscura",
	"episode": "Sei consapevole del fatto che andrai a dormire alle 4 del mattino, no?",
}
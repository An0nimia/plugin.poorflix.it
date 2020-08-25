waste = {
	"plot": "EHY TU. SEI BELLISSIMO =)",
	"mediatype": "movie"
}

def optimize_title(title):
	title = (
		title
		.encode("utf-8")
		.lower()
		.replace("and", "&")
		.replace("&amp;", "&")
	)
	
	return title
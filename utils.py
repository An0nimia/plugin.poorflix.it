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

def check_word_sentence(word, sentence):
	s_sentence = sentence.split(" ")
	there_is = False

	for a in s_sentence:
		if word == a:
			there_is = True
			break

	return there_is
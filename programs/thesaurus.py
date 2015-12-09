import json
import urllib2

cache = {}

def get_synonyms(word, POS):
	if word in cache:
		print "cache"
		return cache[word]
	else:
		url = "http://words.bighugelabs.com/api/2/a3ac0f829c4bc4960c74078b6e4ed9b1/" + word + "/json"
		data = json.load(urllib2.urlopen(url))
		synonyms = list(data[POS]["syn"])
		cache[word] = synonyms
		return synonyms

print get_synonyms("boy", "noun")
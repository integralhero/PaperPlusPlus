import lxml.html
from lxml.cssselect import CSSSelector
import requests

no_replace = ["you", "the", "is", "that", "i", "a", "this", "am", "and", "was", "to", "too", "it", "not", "no", "with", "these", "those", "who", "any", "how", "why", "either", "neither", "an", "or"]
def browseWord(word):
	url = "http://www.thesaurus.com/browse/"+ word
	r = requests.get(url)
	tree = lxml.html.fromstring(r.text)
	sub_tree = lxml.html.fromstring(r.text)
	sel = CSSSelector('#synonyms-0 .relevancy-block .relevancy-list ul li a span.text')
	no_res_sel = CSSSelector('#words-gallery-no-results')
	results = sel(tree)
	if len(results) == 0 or len(no_res_sel(sub_tree)) > 0 or word in no_replace:
		return [word]
	match = results[0]
	data = [result.text for result in results]
	return list(data)
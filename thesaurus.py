import lxml.html
from lxml.cssselect import CSSSelector
import requests

def browseWord(word):
	url = "http://www.thesaurus.com/browse/"+ word
	r = requests.get(url)
	tree = lxml.html.fromstring(r.text)
	sel = CSSSelector('.relevancy-block .relevancy-list ul li a span.text')
	results = sel(tree)
	match = results[0]
	data = [result.text for result in results]
	return list(data)
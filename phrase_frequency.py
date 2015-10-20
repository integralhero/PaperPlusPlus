import re, math
import lxml.html
from lxml.cssselect import CSSSelector
import requests

def computePhraseFrequencies(text):
	print "Generating phrases..."
	text = text.lower()
	phrases = re.split("[.,?;:!]", text)
	for i, phrase in enumerate(phrases):
		phrases[i] = phrase.strip()

	print "Generated {} phrases, analyzing phrase-gram frequencies...".format(len(phrases))
	frequencies = {}
	for phrase in phrases:

		if len(phrase) == 0:
			continue
		words = phrase.split(" ")
		if len(words) == 1:
			continue
		for b in range(1, 4):
			for a in range(1, 4):
				for start in range(0, len(words) - (a + b) + 1):
					gramDelimit = start + a
					first = " ".join(words[start:gramDelimit])
					second = " ".join(words[gramDelimit:gramDelimit + b])
					gramPair = (first, second)
					if gramPair in frequencies:
						frequencies[gramPair] += 1
					else:
						frequencies[gramPair] = 1
	print "Finished analyzing."
	return frequencies

COST_MAX = 100.0
def bigramCost(a, b, data):
	if (a, b) not in data:
		return COST_MAX
	return 1/(math.log(dict[(a,b)])+1)
def unigramCost(a):
	return 1/(math.log(len(a))+1)

def readCorpus(filename):
	with open(filename) as corpusFile:
		text = corpusFile.read()
		data = computePhraseFrequencies(text)
		return data
	return None

def pullCorpus():
	domain = "https://archive.org"
	root_url = "https://archive.org"
	url = "https://archive.org/details/gutenberg"
	r = requests.get(url)
	tree = lxml.html.fromstring(r.text)
	sel = CSSSelector('#ikind--downloads .item-ia .item-ttl a')
	results = sel(tree)

	text_files = []
	top_level = []
	for x in results:
		top_level.append(x.get("href"))
	for i in top_level:
		complete_url = root_url + i
		ar = requests.get(complete_url)
		book_tree = lxml.html.fromstring(ar.text)
		book_sel = CSSSelector('#quickdown3 .format-file a')
		for n in book_sel(book_tree):
			link_to = n.get("href")
			download_url = domain + link_to
			if download_url[-4:] == ".txt":
				text_files.append(download_url)

	texts = []
	for dl_url in text_files:
		og = requests.get(dl_url)
		texts.append(og.text)
	return texts
		

	# match = results[0]
	# data = [result.text for result in results]
	# return list(data)


#data = readCorpus("alice_in_wonderland.txt")
# dict = computePhraseFrequencies("my name is brian. is brian home?")
#print bigramCost("they", "both", data)

pullCorpus()

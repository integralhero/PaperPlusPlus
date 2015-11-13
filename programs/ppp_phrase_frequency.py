import re, math, os
import lxml.html
from lxml.cssselect import CSSSelector
import requests
import urllib2
import string
import thesaurus
from random import randint

def computeSingleWordFreq(text, data):
	if data is None:
		frequencies = {}
	else:
		frequencies = data
	print "    Generating phrases..."
	text = text.lower()
	phrases = re.split("[.,?;:!]", text)
	for i, phrase in enumerate(phrases):
		phrases[i] = phrase.strip()
	for phrase in phrases:
		words = phrase.split(" ")
		for word in words:
			if word in frequencies:
				frequencies[word] += 1
			else:
				frequencies[word] = 1
	return frequencies

def computePhraseFrequencies(text, data):
	print "    Generating phrases..."
	text = text.lower()
	phrases = re.split("[.,?;:!]", text)
	for i, phrase in enumerate(phrases):
		phrases[i] = phrase.strip()

	print "    Generated {} phrases, analyzing phrase-gram frequencies...".format(len(phrases))
	if data is None:
		frequencies = {}
	else:
		frequencies = data
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
	print "    Finished analyzing."
	return frequencies

COST_MAX = 100.0
def bigramCost(a, b, data):
	if (a, b) not in data:
		return COST_MAX
	return 1/(math.log(data[(a,b)])+1)
def unigramCost(a, data):
	if a.lower() not in data:
		return COST_MAX

	return 1/(math.log(data[(a.lower())])+1)

def readCorpus(filename, data):
	print ">>> Reading corpus ({})".format(filename)
	with open(filename) as corpusFile:
		text = corpusFile.read()
		# computePhraseFrequencies(text, data)
		computeSingleWordFreq(text, data)

def readAllCorpuses():
	corpusesFolder = "corpuses"
	corpusFiles = []
	for filename in os.listdir(corpusesFolder):
		if filename.endswith(".txt"):
			corpusFiles.append(corpusesFolder + "/" + filename)
	data = {}
	for corpus in corpusFiles:
		readCorpus(corpus, data)
	return data

def testStr(str, dict):
	avg = 0.0
	words = str.split(" ")
	for i in range(0, len(words)):
		cost = unigramCost(words[i], dict)
		avg += cost
	return avg / float(len(words))





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

# text_files = pullCorpus()
# for i in range(0, len(text_files)):
# 	s = text_files[i]
# 	output = open('test' + str(i) + '.txt','wb')
# 	output.write(s.encode("ascii", errors="ignore"))
# 	output.close()

def baseline(text):
	# text = text.translate(text.maketrans("",""), string.punctuation)
	words = text.lower().split(" ")
	newstr = []
	for i, word in enumerate(words):
		print "Processing word {} out of {}".format(i + 1, len(words))
		replacements = thesaurus.browseWord(word)
		if len(replacements) > 0:
			newstr.append(replacements[randint(0,len(replacements)-1)])
	replacedSentence = " ".join(newstr)
	print ""
	print text.lower()
	print replacedSentence
	return replacedSentence

print "Reading in corpuses in /corpuses\n"
dictFreq = readAllCorpuses()
inputThing = ""
while(True):
	inputThing = raw_input("Type a phrase: ")
	if len(inputThing) == 0:
		break
	newsentence = baseline(inputThing)
	print "Cost for orig: " + str(testStr(inputThing, dictFreq))
	print "Cost for mod: " + str(testStr(newsentence, dictFreq))


import re, math, os

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
	return 1 / (math.log(data[(a,b)]) + 1)

def readCorpus(filename, data):
	print ">>> Reading corpus ({})".format(filename)
	with open(filename) as corpusFile:
		text = corpusFile.read()
		computePhraseFrequencies(text, data)

corpusesFolder = "corpuses"
corpusFiles = []
for filename in os.listdir(corpusesFolder):
	if filename.endswith(".txt"):
		corpusFiles.append(corpusesFolder + "/" + filename)
data = {}
for corpus in corpusFiles:
	readCorpus(corpus, data)

# data = readCorpus("leo-will.txt", None)
# dict = computePhraseFrequencies("my name is brian. is brian home?")

print bigramCost("for", "the past", data)
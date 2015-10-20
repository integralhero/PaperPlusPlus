import re, math

def computePhraseFrequencies(text):
	phrases = re.split("[.,?;:!]", text)
	for i, phrase in enumerate(phrases):
		phrases[i] = phrase.strip()

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
	return frequencies

COST_MAX = 1000.0
def bigramCost(a, b, dict):
	if (a,b) not in dict:
		return COST_MAX
	return 1/(math.log(dict[(a,b)])+1)



dict = computePhraseFrequencies("my name is brian. is brian home?")
print bigramCost("is","brian", dict)
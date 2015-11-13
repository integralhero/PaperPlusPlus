import lxml.html
import lxml.cssselect
from lxml.cssselect import CSSSelector
import requests
import pprint
import numpy
from glove import Glove
from glove import Corpus

MODEL_FILE = "glove.model"
IGNORE_WORDS = ["you", "the", "is", "that", "i", "a", "this", "am", "and", "was", "so", "to", "too", "it", "not", "no", "with", "these", "those", "who", "any", "how", "why", "either", "neither", "an", "or", "for"]

class PaperPlusPlus:
	
	def __init__(self):
		self.glove = None

	def getSynonyms(self, word):
		url = "http://www.thesaurus.com/browse/"+ word
		r = requests.get(url)
		tree = lxml.html.fromstring(r.text)
		sub_tree = lxml.html.fromstring(r.text)
		sel = CSSSelector('#synonyms-0 .relevancy-block .relevancy-list ul li a span.text')
		no_res_sel = CSSSelector('#words-gallery-no-results')
		results = sel(tree)
		if len(results) == 0 or len(no_res_sel(sub_tree)) > 0 or word in IGNORE_WORDS:
			return [word]
		match = results[0]
		data = [result.text for result in results]
		return list(data)
		
	def loadGloveModel(self, modelFile = MODEL_FILE):
		print("Loading pre-trained GloVe model \"{}\"...").format(modelFile)
		self.glove = Glove.load(modelFile)
		print("Done loading.")
		print("")

	def getWordVector(self, word):
		if self.glove is None:
			print("GloVe object is None, loading model")
			loadGloveModel(MODEL_FILE)
		return self.glove.get_word_vector(word)

	def computeVectorDistance(self, vector1, vector2):
		if vector1 is None or vector2 is None:
			return 5
		return numpy.linalg.norm(vector1 - vector2)

# ppp = PaperPlusPlus()
# ppp.loadGloveModel(MODEL_FILE)
# query1 = "however"
# query2 = "although"
# query3 = "likely"
# vector1 = ppp.getWordVector(query1)
# vector2 = ppp.getWordVector(query2)
# vector3 = ppp.getWordVector(query3)

# print("{}: {} {}").format(query1, len(vector1), vector1)
# print("")
# print("{}: {} {}").format(query2, len(vector2), vector2)
# print("")
# print("{}: {} {}").format(query3, len(vector3), vector3)

# print("")
# print("Distance v1 and v2: {}").format(ppp.computeVectorDistance(vector1, vector2))
# print("Distance v1 and v3: {}").format(ppp.computeVectorDistance(vector1, vector3))

# pprint.pprint(glove.most_similar("however", number = 100))
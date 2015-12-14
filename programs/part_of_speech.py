import gensim, logging, nltk

# logging.basicConfig(format = '%(asctime)s : %(levelname)s : %(message)s', level = logging.INFO)

# sentences = [['first', 'sentence'], ['second', 'sentence']]
# model = gensim.models.Word2Vec(sentences, min_count = 1)
# model.save('mymodel')

print "Importing model (takes about 2 minutes)..."
model = gensim.models.Word2Vec.load_word2vec_format("/Users/brian/Downloads/GoogleNews-vectors-negative300.bin", binary=True)
print "Ready!"
while(True):
	print ""
	a = raw_input("Type first word/phrase: ")
	if len(a) == 0:
		break
	b = raw_input("Type second word/phrase: ")
	if len(b) == 0:
		break
	print "Similarity: {}".format(model.similarity(a, b))

# nltk.data.path.append('/Users/brian/Downloads/nltk_data')
# sentence = 'the mana curve is too low'
# tokenized = nltk.word_tokenize(sentence)
# tagged = nltk.pos_tag(tokenized)
# print tagged
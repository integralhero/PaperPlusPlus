import gensim, logging, nltk

# logging.basicConfig(format = '%(asctime)s : %(levelname)s : %(message)s', level = logging.INFO)

# sentences = [['first', 'sentence'], ['second', 'sentence']]
# model = gensim.models.Word2Vec(sentences, min_count = 1)
# model.save('mymodel')

nltk.data.path.append('/Users/brian/Downloads/nltk_data')
sentence = 'the mana curve is too low'
tokenized = nltk.word_tokenize(sentence)
tagged = nltk.pos_tag(tokenized)
print tagged
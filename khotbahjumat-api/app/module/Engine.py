import string
import numpy as np
import numpy.linalg as LA
import math
from Sastrawi.Stemmer.StemmerFactory import StemmerFactory
from Sastrawi.StopWordRemover.StopWordRemoverFactory import StopWordRemoverFactory
from nltk.corpus import stopwords
from nltk.stem import PorterStemmer
from sklearn.feature_extraction.text import CountVectorizer

stemmer = StemmerFactory().create_stemmer()  # Object stemmer
remover = StopWordRemoverFactory().create_stop_word_remover()  # objek stopword
translator = str.maketrans('', '', string.punctuation)


def stemmerEN(text):
    porter = PorterStemmer()
    stop = set(stopwords.words('english'))
    text = text.lower()
    text = [i for i in text.lower().split() if i not in stop]
    text = ' '.join(text)
    preprocessed_text = text.translate(translator)
    text_stem = porter.stem(preprocessed_text)
    return text_stem


def preprocess(text):
    text = text.lower()
    text_clean = remover.remove(text)
    text_stem = stemmer.stem(text_clean)
    text_stem = stemmerEN(text_stem)
    return text_stem


class Engine:
    def __init__(self):
        self.cosine_score = []
        self.train_set = []  # Documents
        self.test_set = []  # Query

    def addDocument(self, word):
        self.train_set.append(word)

    def setQuery(self, word):
        self.test_set.append(word)

    def process_score(self):
        vectorizer = CountVectorizer()

        trainVectorizerArray = vectorizer.fit_transform(self.train_set).toarray()
        testVectorizerArray = vectorizer.transform(self.test_set).toarray()

        cx = lambda a, b: round(np.inner(a, b) / (LA.norm(a) * LA.norm(b)), 3)
        # print testVectorizerArray
        output = []
        for i in range(0, len(testVectorizerArray)):
            output.append([])

        for vector in trainVectorizerArray:
            # print vector
            u = 0
            for testV in testVectorizerArray:
                # print testV
                cosine = cx(vector, testV)
                if math.isnan(cosine):
                    cosine = 0
                # self.cosine_score.append(cosine)
                # pembulatan = (round(cosine),2)
                output[u].append((cosine))
                u = u + 1
        return output
        # return testVectorizerArray

    def check_tag(self, tag, tags):
        # data_tag = tag.split(',')
        # data_tags = tags.split(',')
        stat = False
        if tag in tags:
            stat = True
        return stat

__author__ = 'nikita'
from application.lsi.similarities import *


class DetectSentiment:
    def __init__(self, query):
        self.query = query

    def detect_sentiment(self):
        model_lda = MyModel(dict_file='serialise/vocabulary.dict',
                            corpus_file='serialise/corpus.mm')
        model_lda.lda()
        similarity_model = SimilarityLDA(model_lda, self.query, normalise_func=MyMorphy.normal_morph_static)
        similarity = similarity_model.similarities()
        return similarity_model.rank_priorities(similarity)
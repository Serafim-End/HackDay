# -*- coding: utf-8 -*-
from gensim import similarities

__author__ = 'nikita'


class Similarity:
    def __init__(self, my_model, query, normalise_func):
        self.model = my_model
        self.query = query
        self.normalise_func = normalise_func

        self.vector_model = None
        self.vector_bow = None

    @staticmethod
    def rank_priorities(similarities_vector):
        similarities_vector = {i + 1: similarities_vector[i] for i in xrange(len(similarities_vector))}
        return sorted([(value, key) for (key, value) in similarities_vector.items()], reverse=True)


class SimilarityLSI(Similarity):
    def similarities(self):
        if self.model.lsi_model:
            self.vector_bow = self.model.dictionary.doc2bow(self.normalise_func(self.query))
            self.vector_model = self.model.lsi_model[self.vector_bow]
            index = similarities.MatrixSimilarity(self.model.lsi_model[self.model.corpus])
            return index[self.vector_model]
        else:
            raise "lsi model not initialised"


class SimilarityLDA(Similarity):
    def similarities(self):
        if self.model.lda_model:
            self.vector_bow = self.model.dictionary.doc2bow(self.normalise_func(self.query))
            self.vector_model = self.model.lda_model[self.vector_bow]
            index = similarities.MatrixSimilarity(self.model.lda_model[self.model.corpus])
            return index[self.vector_model]
        else:
            raise "lda model not initialised"


if __name__ == '__main__':
    # vocabulary = MyDictionary.load_dictionary(language='ru')
    # corpus = MyCorpusFiles.load_corpus('serialise/corpus.mm')
    model = MyModel(dict_file='serialise/vocabulary.dict', corpus_file='serialise/corpus.mm')
    model.lsi()

    print "dictionary: ", model.dictionary

    similarity_model = SimilarityLSI(model, u'Человек родился в машине', normalise_func=MyMorphy.normal_morph_static)
    similarity = similarity_model.similarities()
    print "lsi model: ", similarity_model.rank_priorities(similarity)

    model.lda()
    similarity_model = SimilarityLDA(model, u'Человек родился в машине', normalise_func=MyMorphy.normal_morph_static)
    similarity = similarity_model.similarities()
    print "lda model: ", similarity_model.rank_priorities(similarity)

# -*- coding: utf-8 -*-
__author__ = 'nikita'
from gensim import corpora, models
from gensim.models.lsimodel import LsiModel


class MyModel:
    def __init__(self, dict_file=None, corpus_model=None, corpus_file=None):
        self.dict_file = dict_file
        self.dictionary = None
        self.corpus = None

        if dict_file is not None:
            self.dictionary = corpora.Dictionary.load(dict_file)
        if corpus_model:
            self.corpus = self.corpus_model
        elif corpus_file:
            self.corpus = corpora.MmCorpus(corpus_file)

        self.tf_idf_model = None
        self.corpus_tf_idf = None
        self.lsi_model = None
        self.corpus_lsi = None

        self.lda_model = None
        self.corpus_lda = None

    def tf_idf(self):
        self.tf_idf_model = models.TfidfModel(corpus=self.corpus, normalize=True)
        # corpus_vector = [vector for vector in self.corpus]
        self.corpus_tf_idf = self.tf_idf_model[self.corpus]

    def lsi(self):
        self.tf_idf()
        if self.corpus_tf_idf and self.dictionary:
            self.lsi_model = LsiModel(self.corpus_tf_idf, num_topics=2)
            self.corpus_lsi = self.lsi_model[self.corpus_tf_idf]
            print self.lsi_model.print_topic(2)
        elif self.corpus_tf_idf:
            self.lsi_model = LsiModel(self.corpus_tf_idf, num_topics=2)
            self.corpus_lsi = self.lsi_model[self.corpus_tf_idf]

    def lda(self):
        self.lda_model = models.LsiModel(corpus=self.corpus)
        self.corpus_lda = self.lda_model[self.corpus]

    def add_document_lsi(self, addition_corpus_tf_idf, addition_vector_tf_idf):
        self.lsi_model.add_documents(addition_corpus_tf_idf)
        lsi_vector = self.lsi_model[addition_vector_tf_idf]
        return lsi_vector

    def save_lsi(self, name='/serialise/model.lsi'):
        self.lsi_model.save(name)

    def save_lda(self, name='/serialise/model.lda'):
        self.lda_model.save(name)

    @staticmethod
    def load_lsi(name='/tmp/model.lsi'):
        my_model = MyModel()
        my_model.lsi_model = models.LsiModel.load(name)
        return my_model



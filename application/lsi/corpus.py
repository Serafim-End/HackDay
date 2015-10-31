# -*- coding: utf-8 -*-
__author__ = 'nikita'

import os

from gensim import corpora, utils

from application.lsi import MyDictionary


def iter_documents(top_directory):
    """Iterate over all documents, yielding a document (=list of utf8 tokens) at a time."""
    for root, dirs, files in os.walk(top_directory):
        for file in filter(lambda file: file.endswith('.txt'), files):
            document = open(os.path.join(root, file)).read()  # read the entire document, as one big string
            yield utils.tokenize(document, lower=True)  # or whatever tokenization suits you


class MyCorpusFiles(object):
    def __init__(self, dictionary=None, top_dir="files"):
        self.top_dir = top_dir
        self.serialise_filename = 'serialise/corpus.mm'
        self.corpus = None
        self.dictionary = corpora.Dictionary(iter_documents(self.top_dir)) if not dictionary else dictionary

    def __iter__(self):
        for tokens in iter_documents(self.top_dir):
            yield self.dictionary.doc2bow(tokens)

    def serialise_corpus(self):
        corpus_model = MyCorpusFiles(self.top_dir)
        self.dictionary = corpora.Dictionary(iter_documents(self.top_dir))
        self.dictionary.filter_extremes(no_below=1, keep_n=300000)
        self.corpus = [corpus_vector for corpus_vector in corpus_model]
        corpora.MmCorpus.serialize(self.serialise_filename, self.corpus)

    @staticmethod
    def serialise_corpus_dictionary(corpus_name='serialise/corpus.mm'):
        corpus_model = MyCorpusFiles()
        dictionary_model = MyDictionary(language='ru')
        corpus_model.dictionary.save(dictionary_model.save_name)
        corpora.MmCorpus.serialize(corpus_name, corpus_model)

    @staticmethod
    def load_corpus(serialise_filename):
        corpus_model = corpora.MmCorpus(serialise_filename)
        corpus = [vector for vector in corpus_model]
        return corpus

    def __str__(self):
        if self.corpus is not None:
            print self.corpus
        return str()


if __name__ == '__main__':
    MyCorpusFiles.serialise_corpus_dictionary()


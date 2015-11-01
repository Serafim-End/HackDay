# -*- coding: utf-8 -*-
import os

from gensim import corpora

from application.lsi.morph import MyMorphy

__author__ = 'nikita'


class MyDictionary:
    def __init__(self, documents=None, stop_list=None,
                 save_name='serialise/vocabulary.dict',
                 normalise_func=MyMorphy.morph_split,
                 language='en'):

        self.documents = documents
        self.dictionary = None
        self.normalise_func = normalise_func
        self.save_name = save_name
        self.morph = None

        self.language = language
        if self.language == 'en':
            self.stop_list = set(u'for a of the and to in'.split()) if stop_list is None else stop_list
        if self.language == 'ru':
            self.morph = MyMorphy()
            self.stop_list = MyMorphy.stop_list() if stop_list is None else stop_list

        self.prepared_text = None

    def save_dictionary(self):
        if self.dictionary is not None:
            self.dictionary.save(self.save_name)

    @staticmethod
    def load_dictionary(language='en'):
        dictionary_model = MyDictionary(language=language)
        dictionary_model.dictionary = corpora.Dictionary.load(dictionary_model.save_name)

    def add_document(self, filename):
        normal_document = []
        if self.language == 'ru':
            for line in open(filename):
                # print line
                for word in self.morph.normal_morph(line, stop_list=self.stop_list):
                    normal_document.append(word)

            if self.dictionary:
                dictionary = corpora.Dictionary(documents=[normal_document])
                self.dictionary.merge_with(dictionary)
            else:
                self.dictionary = corpora.Dictionary(documents=[normal_document])

    def add_documents(self):
        if isinstance(self.documents, list):
            for filename in self.documents:
                self.add_document(filename)
        elif isinstance(self.documents, str):  # In my opinion it is a directory
            for root, dirs, files in os.walk(self.documents):
                for file in filter(lambda f: f.endswith('.txt'), files):
                    self.add_document(self.documents + '/' + file)
                    print vocabulary1

    def normalise_frequency(self):
        if self.dictionary:
            stop_ids = [self.dictionary.token2id[stop_word] for stop_word in self.stop_list
                        if stop_word in self.dictionary.token2id]

            once_ids = [token_id for token_id, doc_freq in self.dictionary.dfs.iteritems() if doc_freq == 1]
            self.dictionary.filter_tokens(stop_ids + once_ids)
            self.dictionary.compactify()

    def __str__(self):
        return str(self.dictionary)

if __name__ == '__main__':
    vocabulary1 = MyDictionary(documents='files', language='ru')
    vocabulary1.add_documents()
    vocabulary1.normalise_frequency()
    print vocabulary1





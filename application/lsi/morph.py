# -*- coding: utf-8 -*-
__author__ = 'nikita'
import pymorphy2


class MyMorphy:
    def __init__(self, morph=None):
        self.morph = morph if morph is not None else pymorphy2.MorphAnalyzer()

    @staticmethod
    def morph(line):
        if isinstance(line, str) or isinstance(line, unicode):
            return line.lower()

    @staticmethod
    def stop_list(language='ru'):
        if language == 'ru':
            return [word.split()[0].decode('utf-8') for word in open('serialise/stopwords.txt')]
        elif language == 'en':
            return [word for word in u'for a of the and to in'.split()]
        else:
            return []

    @staticmethod
    def morph_split(line):
        return MyMorphy.morph(line).split()

    def normal_morph(self, line=None, word=None, language='ru'):
        stop_list = MyMorphy.stop_list() if language == 'ru' else []
        if line:
            line = line.decode(encoding='utf-8')
            return [self.morph.parse(item.lower())[0].normal_form for item in line.split()
                    if item not in stop_list]
        elif word:
            if word not in stop_list:
                return self.morph.parse(word)[0].normal_form

    @staticmethod
    def normal_morph_static(line=None, word=None, language='ru'):
        morph = pymorphy2.MorphAnalyzer()
        stop_list = MyMorphy.stop_list() if language == 'ru' else []
        if line:
            if not isinstance(line, unicode):
                line = line.decode(encoding='utf-8')
            return [morph.parse(item.lower())[0].normal_form for item in line.split()
                    if item not in stop_list]
        elif word:
            if word not in stop_list:
                return morph.parse(word)[0].normal_form


if __name__ == '__main__':
    pass
    # analyser = MyMorphy()
    # array = analyser.normal_morph(line=u'Тэд Уильямс', stop_list=[u'и'])

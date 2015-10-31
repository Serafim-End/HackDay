# -*- coding: utf-8 -*-
__author__ = 'nikita'
import unittest
from random import randint
from pymorphy2 import MorphAnalyzer


class MorphTest(unittest.TestCase):
    def __init__(self, document_vector):
        self.document = None
        self.documents = document_vector
        self.morph = MorphAnalyzer()

    # def setUp(self):
    #     self.document = documents[randint(0, len(documents))]

    def testMorph(self):
        self.document = self.document if not None else self.documents[0]
        morph_array = [self.morph.parse(word)[0].normal_form for word in self.document]
        print morph_array
        self.assertTrue(True, msg=None)





documents = [u'Условная вероятность P(tag|word) оценивается на основе корпуса'
             u'щутся все неоднозначные слова со снятой неоднозначностью, для каждого слова считается,'
             u' сколько раз ему был сопоставлен данный тег, и на основе этих частот вычисляется '
             u'условная вероятность тега (с исползованием сглаживания Лапласа). '
             u'На данный момент оценки P(tag|word) на основе OpenCorpora есть примерно для 20 тыс. слов'
             u' (исходя из примерно 250тыс. наблюдений). Для тех слов, для которых такой оценки нет,'
             u' вероятность P(tag|word) либо считается равномерной (для словарных слов),'
             u' либо оценивается на основе эмпирических правил (для несловарных слов).'
             u'На практике это означает, что первый разбор из тех, что возвращают методы MorphAnalyzer.parse() и '
             u'MorphAnalyzer.tag(), более вероятен, чем остальные. Для слов (без учета пунктуации и т.д.) цифры такие:'
             u'случай выбранный разбор (из допустимых) верен примерно в 66% случаев;'
             u'первый словарю разбор (pymorphy2 < 0.4) верен примерно в 72% случаев;'
             u'разбор, который выдает pymorphy2 == 0.4, выбранный на основе оценки P(tag|word), верен примерно в 79% случаев.']
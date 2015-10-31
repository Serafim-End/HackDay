# -*- coding: utf-8 -*-
__author__ = 'nikita'
import itertools
from parser_transactions_csv import TransactionsModel
import json


class RankComment:
    def __init__(self, mc_model):
        self.mc_model = mc_model
        self.comments_list = self.mc_model.comments_list
        self.stop_words = RankComment.parse_swear_words()
        self.transactions_model = RankComment.transactions_load()

    @staticmethod
    def transactions_load():
        trans_dict = open('transactions_simple.json').read()
        return json.loads(trans_dict)

    @staticmethod
    def parse_swear_words():
        swear_words = []
        for line in open('swearwords.txt'):
            swear_words.append((line.split()[0]).decode(encoding='utf-8'))
        return swear_words

    def filter_swear_words(self):
        lex_comments = []
        swear_comments = []
        for comment in self.comments_list:
            is_comment_lex = True
            for word in comment.message.split():
                word = word.decode(encoding='utf-8')
                if word in self.stop_words:
                    is_comment_lex = False
            if is_comment_lex:
                lex_comments.append(comment)
            else:
                swear_comments.append(comment)
        return lex_comments, swear_comments

    def filter_length_comment(self):
        lex_comment, swear_comments = self.filter_swear_words()
        lex_comment = sorted(lex_comment, key=lambda comment: -len(comment.message.split()))
        swear_comments = sorted(swear_comments, key=lambda comment: -len(comment.message.split()))
        self.comments_list = itertools.chain(lex_comment, swear_comments)
        return self.comments_list

    def filter_func(self, comment, alpha):
        multiplier = 1
        if comment.user_id in self.transactions_model:
            multiplier = alpha * self.transactions_model[comment.user_id]
        return -len(comment.message.split()) * multiplier

    def filter_length_weight_comment(self):
        lex_comment, swear_comments = self.filter_swear_words()
        lex_comment = sorted(lex_comment,
                             key=lambda comment:self.filter_func(comment, 0.25))

        swear_comments = sorted(swear_comments, key=lambda comment: self.filter_func(comment, 0.5))
        self.comments_list = itertools.chain(lex_comment, swear_comments)

    def __str__(self):
        self.filter_length_weight_comment()
        for comment in self.comments_list:
            print comment.message

        print
        print
        return str()


class RankComments:
    def __init__(self, mc_models):
        self.mc_array = mc_models

    def rank_comments(self):
        for item in self.mc_array:
            rank_comment = RankComment(item)
            item.comments_list = rank_comment.comments_list
            # rank_comment.__str__()

    def model_to_json(self):
        json_array = RankList(self.mc_array)
        json_file = open("rank_comments.json", 'r+')
        json_file.write(json.dumps(json_array.to_json()))
        json_file.close()


class RankList(json.JSONEncoder):
    def __init__(self, array):
        self.array = array

    def to_json(self):
        return json.dumps(self, default=lambda o: o.__dict__, sort_keys=True)


if __name__ == '__main__':
    from parser_csv import make_array
    array = make_array()
    model = RankComments(array)
    model.rank_comments()
    model.model_to_json()

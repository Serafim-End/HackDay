# -*- coding: utf-8 -*-
__author__ = 'nikita'

import csv
import json


class Comment(object):
    def __init__(self, comment_id, user_id, c_time, message):
        self.comment_id = comment_id
        self.user_id = user_id
        self.c_time = c_time
        self.message = message


class MovieCommentModel(json.JSONEncoder):
    def __init__(self, movie_id, movie_name):
        self.movie_id = movie_id
        self.picture = None
        self.movie_name = movie_name
        self.comments_list = []

    def default(self, o):
        return o.__dict__


class MCList(json.JSONEncoder):
    def __init__(self, array):
        self.array = array

    def to_json(self):
        return json.dumps(self, default=lambda o: o.__dict__, sort_keys=True)


class CommentModel(object):
    def __init__(self, comment_id, movie_id, movie_name, user_id, c_time, message):
        self.id = comment_id
        self.movie_id = movie_id
        self.movie_name = movie_name
        self.user_id = user_id
        self.c_time = c_time
        self.message = message


class CommentList(object):
    def __init__(self):
        self.comment_list = []

    def add_comment(self, other):
        self.comment_list.append(other)

    def serialise(self):
        pass

    def __str__(self):
        for comment in self.comment_list:
            print comment.movie_name
        return str()


def comments_parser():
    with open('comments.csv', 'r+') as csvfile:
        spam_reader = csv.reader(csvfile, delimiter='\t', quotechar='|')
        comment_list = CommentList()

        i = 0
        for row in spam_reader:
            if i > 0:
                comment_model = CommentModel(comment_id=row[0],
                                             movie_id=row[1],
                                             movie_name=row[2],
                                             user_id=row[3],
                                             c_time=row[4],
                                             message=row[5])

                comment_list.add_comment(comment_model)
            i += 1
        return comment_list


def parser2():
    array = comments_parser()
    comment_list = array.comment_list

    array = []
    array_stop_numbs = []

    couter = 0
    for i in comment_list:
        if couter not in array_stop_numbs:
            array_stop_numbs.append(couter)
            ad_couter = 0
            mc_model = MovieCommentModel(i.movie_id, i.movie_name)
            for j in comment_list:
                if ad_couter not in array_stop_numbs:
                    if i.movie_id == j.movie_id:
                        mc_model.comments_list.append(Comment(j.id, j.user_id, j.c_time, j.message))
                        array_stop_numbs.append(ad_couter)
                ad_couter += 1
            array.append(mc_model)
        couter += 1

    return array


def make_array():
    array = parser2()

    indexes = []
    for i in xrange(len(array)):
        if len(array[i].comments_list) == 0:
            indexes.append(i)

    devider = 0
    for i in indexes:
        array.remove(array[i - devider])
        devider += 1

    return array


def make_json_array():
    array = make_array()
    array = MCList(array)

    json_file = open("comments.json", 'r+')
    json_file.write(json.dumps(array.to_json()))
    json_file.close()


if __name__ == '__main__':
    make_json_array()
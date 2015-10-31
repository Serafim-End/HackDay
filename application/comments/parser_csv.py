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


# 11243	7495	Монстры на каникулах 2	43097	2015-10-29 23:51:42.574943+03	Фильм потрясающий. Подпортил впечатле
def parse_row(row):
    counter = 0
    comment_id = ""
    movie_id = ""
    first_symbol = "" \
                   ""
    for item in row:
        for element in item:
            if counter == 0:
                first_symbol = element

            if first_symbol == '1':
                first_left = 5
                first_right = 10
            else:
                first_left = 4
                first_right = 9

            if counter < first_left:
                comment_id += element
            elif first_left < counter < first_right:
                movie_id += element
            counter += 1

            if counter > first_right:
                if counter < 33:
                    element = item[counter] + item[counter + 1]\
                              + item[counter + 2] + item[counter + 3] + item[counter + 4]


def parser():
    with open('comments.csv', 'r+') as csvfile:
        spam_reader = csv.reader(csvfile, delimiter=' ', quotechar='|')
        comment_list = CommentList()

        i = 0
        for row in spam_reader:
            if len(row) > 1:
                # print "movieID: ", parse_row(row)
                # print

                row0 = row[0].decode(encoding='utf-8').split()
                c_time = ""
                movie_name = ""
                movie_id = ""
                user_id = ""
                comment_id = ""
                j = 0
                for item in row0:
                    if j == 0:
                        # print "comment id: ", item
                        comment_id = item
                    if j == 1:
                        # print "movie id", item
                        movie_id = item
                    if j == 2:
                        # print "movie name", item
                        movie_name = item
                    if j == 3:
                        # print "user id", item
                        user_id = item
                    if j == 4:
                        # print "c time", item
                        c_time += item
                    j += 1

                row1 = row[1].decode(encoding='utf-8').split(' ')
                message = ""
                j = 0
                for item in row1:
                    if j == 0:
                        c_time += ' ' + item
                    else:
                        message += row1[1]

                for item in row[2::]:
                    message += ' ' + item

                comment_model = CommentModel(comment_id=comment_id, movie_id=movie_id, movie_name=movie_name, user_id=user_id, c_time=c_time, message=message)
                comment_list.add_comment(comment_model)

    return comment_list


def parser2():
    array = parser()
    comment_list = array.comment_list

    array = []

    array_stop_numbs = []
    # array.append(movie_comment_model)

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


def main():
    array = parser2()

    indexes = []
    for i in xrange(len(array)):
        if len(array[i].comments_list) == 0:
            indexes.append(i)

    devider = 0
    for i in indexes:
        array.remove(array[i - devider])
        devider += 1

    array = MCList(array)

    json_file = open("comments.json", 'r+')
    json_file.write(json.dumps(array.to_json()))
    json_file.close()


if __name__ == '__main__':
    main()
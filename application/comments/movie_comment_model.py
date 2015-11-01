__author__ = 'nikita'
import json


class MovieCommentModel(json.JSONEncoder):
    def __init__(self, movie_id, movie_name):
        self.movie_id = movie_id
        self.picture = None
        self.movie_name = movie_name
        self.comments_list = []

    def default(self, o):
        return o.__dict__


class Comment(object):
    def __init__(self, comment_id, user_id, c_time, message):
        self.comment_id = comment_id
        self.user_id = user_id
        self.c_time = c_time
        self.message = message


class MCList(json.JSONEncoder):
    def __init__(self, array):
        self.array = array

    def to_json(self):
        return json.dumps(self, default=lambda o: o.__dict__, sort_keys=True)

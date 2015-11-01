__author__ = 'nikita'
import itertools
import json
from application.comments.parser_csv import *
from application.comments.detect_sentiment import *


class UserComment:
    def __init__(self):
        self.user_id = None
        self.comments_list = []

    @staticmethod
    def pick_out_all_comments():
        array_models = make_set()
        comments_list = []
        for model in array_models:
            temp_array = []
            for comment in model.comments_list:
                temp_array.append(CommentMovie(movie_id=model.movie_id, comment_id=comment.comment_id,
                                               user_id=comment.user_id, c_time=comment.c_time, message=comment.message))
            comments_list = comments_list + temp_array
        return comments_list

    @staticmethod
    def make_model():
        comments_list = UserComment.pick_out_all_comments()
        array_stop_numbs = []
        array = []
        counter = 0
        for i in comments_list:
            if counter not in array_stop_numbs:
                array_stop_numbs.append(counter)
                ad_counter = 0
                user_comment_model = UserComment()
                user_comment_model.user_id = i.user_id
                for j in comments_list:
                    if ad_counter not in array_stop_numbs:
                        if i.user_id == j.user_id:
                            user_comment_model.comments_list.append(CommentMovie(movie_id=j.movie_id,
                                                                                 comment_id=j.comment_id,
                                                                                 user_id=j.user_id,
                                                                                 c_time=j.c_time,
                                                                                 message=j.message))
                            array_stop_numbs.append(ad_counter)
                    ad_counter += 1
                array.append(user_comment_model)
            counter += 1
        return array

    def __str__(self):
        array = UserComment.make_model()
        print array
        return str()


class CommentMovie:
    def __init__(self, movie_id, comment_id, user_id, c_time, message):
        self.movie_id = movie_id
        self.comment_id = comment_id
        self.user_id = user_id
        self.c_time = c_time
        self.message = message


class RateModel:
    def __init__(self):
        self.json_movies = self.get_movies()
        self.comments_array = UserComment.make_model()

    @staticmethod
    def get_movies():
        with open('movies.json') as json_file:
            json_array = json_file.read()
            return json.loads(json_array)

    def sentiment_detect(self):
        sentiments_dictionary = {}
        i = 0
        for comment_model in self.comments_array:
            for comment in comment_model.comments_list:
                print "i: ", i, comment.message
                detect_sentiment = DetectSentiment(comment.message)
                sentiments_dictionary[comment.movie_id] = detect_sentiment.detect_sentiment()
                i += 1
        return sentiments_dictionary

    def dump_sentimental(self):
        dictionary = self.sentiment_detect()
        json_file = open("sentimental_comments.json", 'r+')
        json_file.write(json.dumps(dictionary))
        json_file.close()
        return dictionary

    @staticmethod
    def load_sentimental():
        with open('sentimental_comments.json', 'r') as sent_file:
            sent_json = sent_file.read()
            sentimental_dictionary = json.loads(sent_json)
            return sentimental_dictionary

    def make_model(self):
        rating_dictionary = {}
        sentimental_dictionary = RateModel.load_sentimental()
        # sentimental_dictionary = self.dump_sentimental()
        print sentimental_dictionary
        for comment_model in self.comments_array:
            for comment in comment_model.comments_list:
                for film in self.json_movies:
                    if int(comment.movie_id) == int(film["id"]):
                        if comment.movie_id in sentimental_dictionary:
                            multiplier, value = sentimental_dictionary[comment.movie_id][0]
                        else:
                            multiplier, value = 1, 1
                        multiplier = float(multiplier)
                        value = int(value)
                        if value == 1:
                            if film["genres"][0]["id"] not in rating_dictionary:
                                rating_dictionary[film["genres"][0]["id"]] = 0
                            rating_dictionary[film["genres"][0]["id"]] += (-1) * multiplier
                        else:
                            if film["genres"][0]["id"] not in rating_dictionary:
                                rating_dictionary[film["genres"][0]["id"]] = 0
                            rating_dictionary[film["genres"][0]["id"]] += 1 * multiplier
        return rating_dictionary

    def rank_genres(self):
        rating_dictionary = self.make_model()
        rating_dictionary = sorted([(str(value), str(key)) for (key, value) in rating_dictionary.items()], reverse=True)
        return rating_dictionary

    def choose_movies(self):
        rank_dictionary = self.rank_genres()
        running_json = RateModel.get_running()
        choose_movie = []
        for film in running_json:
            multiplier, genre_id = rank_dictionary[0]
            if film["genres"]:
                if film["genres"][0]["id"] == int(genre_id):
                    choose_movie.append(film)

        return choose_movie

    @staticmethod
    def make_rank_movies_json():
        model_rate = RateModel()
        array = model_rate.choose_movies()
        json_file = open("rank_film_running.json", 'r+')
        json_file.write(json.dumps(array))
        json_file.close()

    @staticmethod
    def get_running():
        with open('running.json') as json_file:
            json_array = json_file.read()
            return json.loads(json_array)

    @staticmethod
    def make_json():
        model = RateModel()
        dictionary = model.make_model()
        json_file = open("rank_film.json", 'r+')
        json_file.write(json.dumps(dictionary))
        json_file.close()

    def __str__(self):
        dictionary = self.make_model()
        print dictionary
        return str()

if __name__ == '__main__':
    # UserComment().__str__()
    # model = RateModel()
    # model.make_rank_film()
    # RateModel.make_json()
    RateModel.make_rank_movies_json()
    # model.__str__()

__author__ = 'nikita'
import json
from parser_csv import make_set
from rank_comments import RankComments, RankList


class MoviesPicture:
    def __init__(self, mc_models_array):
        self.mc_models_array = mc_models_array
        self.json_movies = self.get_movies()

    @staticmethod
    def get_movies():
        with open('movies.json', 'r') as json_file:
            json_array = json_file.read()
            return json.loads(json_array)

    def make_pictures(self):
        for mc_model in self.mc_models_array:
            for film in self.json_movies:
                if int(mc_model.movie_id) == int(film["id"]):
                    if film["images"]:
                        mc_model.picture = film["images"][0]["name"]

    def model_to_json(self):
        json_array = RankList(self.mc_models_array)
        json_file = open("rank_comments.json", 'r+')
        json_file.write(json.dumps(json_array.to_json()))
        json_file.close()


if __name__ == '__main__':
    array = make_set()
    model = RankComments(array)
    model.rank_comments()
    movie_addition = MoviesPicture(model.mc_array)
    movie_addition.make_pictures()
    movie_addition.model_to_json()

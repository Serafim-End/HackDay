__author__ = 'nikita'
import csv
import json


class Transactions:
    def __init__(self, user_id, c_time, movie_id, movie_name):
        self.user_id = user_id
        self.c_time = c_time
        self.movie_id = movie_id
        self.movie_name = movie_name


class TransactionsFilm:
    def __init__(self, c_time, movie_id, movie_name):
        self.c_time = c_time
        self.movie_id = movie_id
        self.movie_name = movie_name


class TransactionsModel:
    def __init__(self, user_id):
        self.user_id = user_id
        self.transaction_films = []

    def add_film(self, c_time, movie_id, movie_name):
        self.transaction_films.append(TransactionsFilm(c_time, movie_id, movie_name))

    @staticmethod
    def transactions_parser():
        transactions_array = []
        with open('transactions.csv', 'r+') as csv_file:
            spam_reader = csv.reader(csv_file, delimiter='\t', quotechar='|')
            i = 0
            for line in spam_reader:
                if i > 0:
                    transactions_array.append(Transactions(user_id=line[0], c_time=line[1],
                                                           movie_id=line[2], movie_name=line[3]))
                i += 1
        return transactions_array

    @staticmethod
    def make_model():
        transaction_array = TransactionsModel.transactions_parser()
        transaction_model_array = []

        array_stop_numbs = []
        counter = 0
        for i in transaction_array:
            if counter not in array_stop_numbs:
                array_stop_numbs.append(counter)
                model = TransactionsModel(i.user_id)
                ad_counter = 0
                for j in transaction_array:
                    if ad_counter not in array_stop_numbs:
                        if i.user_id == j.user_id:
                            model.add_film(c_time=j.c_time, movie_id=j.movie_id, movie_name=j.movie_name)
                            array_stop_numbs.append(ad_counter)
                    ad_counter += 1
                transaction_model_array.append(model)
            counter += 1
        return transaction_model_array

    @staticmethod
    def make_dict():
        transactions_model_array = TransactionsModel.make_model()
        dictionary_transactions = {item.user_id: len(item.transaction_films) for item in transactions_model_array}
        return dictionary_transactions

    @staticmethod
    def make_simple_json():
        dictionary = TransactionsModel.make_dict()
        json_file = open("transactions_simple.json", 'r+')
        json_file.write(json.dumps(dictionary))
        json_file.close()
        return json.dumps(dictionary)

    @staticmethod
    def make_json():
        array = TransactionsModel.make_model()
        json_array = JSList(array)
        json_file = open("transactions.json", 'r+')
        json_file.write(json.dumps(json_array.to_json()))
        json_file.close()


class JSList(json.JSONEncoder):
    def __init__(self, array):
        self.array = array

    def to_json(self):
        return json.dumps(self, default=lambda o: o.__dict__, sort_keys=True)


if __name__ == '__main__':
    TransactionsModel.make_json()
    TransactionsModel.make_simple_json()
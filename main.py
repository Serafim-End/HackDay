from flask import Flask
import json
import os
import application
app = Flask(__name__)


def root_dir():  # pragma: no cover
    return os.path.abspath(os.path.dirname(__file__))


@app.route('/comments/')
def comments():
    try:
        src = os.path.join(root_dir(), 'application/comments/comments.json')
        json_file = open(src).read()
        return json.loads(json_file)
    except IOError:
        return "Comments Error"


@app.route('/transactions/')
def transactions():
    try:
        src = os.path.join(root_dir(), 'application/comments/transactions.json')
        json_file = open(src).read()
        return json.loads(json_file)
    except IOError:
        return "Transactions Error"


@app.route('/rank_comments/')
def rank_comments():
    try:
        src = os.path.join(root_dir(), 'application/comments/rank_comments.json')
        json_file = open(src).read()
        return json.loads(json_file)
    except IOError:
        return "Rank comments Error"

if __name__ == '__main__':
    app.run()

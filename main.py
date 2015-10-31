from flask import Flask
import json
import os
import application
app = Flask(__name__)


def root_dir():  # pragma: no cover
    return os.path.abspath(os.path.dirname(__file__))

@app.route('/')
def comments():
    try:
        src = os.path.join(root_dir(), 'application/comments/comments.json')
        json_file =  open(src).read()
        return json.loads(json_file)
    except IOError:
        return "Hello Error"


if __name__ == '__main__':
    app.run()

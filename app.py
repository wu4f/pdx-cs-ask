"""
A simple guestbook flask app.
"""
import flask
import os
from llm import myllm
from index import Index
from query import Query
from callback import Callback
from logout import Logout

app = flask.Flask(__name__)       # our Flask app

app.secret_key = os.urandom(24)

app.add_url_rule('/',
                 view_func=Index.as_view('index'),
                 methods=["GET"])

app.add_url_rule('/callback',
                 view_func=Callback.as_view('callback'),
                 methods=["GET"])

app.add_url_rule('/query',
                 view_func=Query.as_view('query'),
                 methods=['GET', 'POST'])

app.add_url_rule('/logout',
                 view_func=Logout.as_view('logout'),
                 methods=["GET"])

if __name__ == '__main__':
    app.run(host='0.0.0.0', debug=True)

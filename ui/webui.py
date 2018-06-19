from flask import Flask, render_template
from util.request_handler import RequestHandler

app = Flask(__name__)


@app.route('/')
def home():
    rh = RequestHandler()
    sums = rh.get_all_summoners()
    um = rh.get_all_usermatches()
    rh.close()
    return render_template('home.html', summoners=sums, usermatches=um)


def launch():
    app.run()


if __name__ == '__main__':
    launch()

from flask import Flask, render_template
from util.request_handler import RequestHandler
import json

app = Flask(__name__)

configFile = '../conf/config.json'
configData = json.load(open(configFile))

apiEndpoint = configData["api"]["endpoint"]
apiKey = configData["api"]["key"]
#rh = RequestHandler(apiEndpoint, apiKey, '../riot.db')


@app.route('/')
def home():
    rh = RequestHandler(apiEndpoint, apiKey, '../riot.db')
    sums = rh.get_all_summoners()
    um = rh.get_all_usermatches()
    rh.close()
    return render_template('home.html', summoners=sums, usermatches=um)


def launch():
    app.run()


if __name__ == '__main__':
    launch()

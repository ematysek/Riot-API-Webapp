from flask import Flask, render_template, flash, redirect, url_for
from util.request_handler import RequestHandler

from conf.config import FlaskConfig
from ui.forms import SummonerSearchForm
app = Flask(__name__)


@app.route('/', methods=['GET', 'POST'])
def home():
    form = SummonerSearchForm()
    if form.validate_on_submit():
        flash("Searched for {}".format(form.summoner.data), 'success')
        return redirect(url_for('home'))
    rh = RequestHandler()
    sums = rh.get_all_summoners()
    um = rh.get_all_usermatches()
    rh.close()
    return render_template('home.html', summoners=sums, usermatches=um, form=form)


def launch():
    app.config['SECRET_KEY'] = FlaskConfig().secret_key
    app.run(host='0.0.0.0')


if __name__ == '__main__':
    launch()

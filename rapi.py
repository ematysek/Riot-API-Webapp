import logging
import logging.config
import os

from conf.config import load_config, get_logger_config, load_logger_config
from app.util.request_handler import RequestHandler
from app import create_app, db
from flask import render_template, redirect, url_for, flash
from app.forms import SummonerSearchForm
from app.flask_models import Summoner

app = create_app()

logging.config.dictConfig(load_logger_config())

app.logger.info("app created")
app.logger.info("debug: {}".format(app.debug))
app.logger.info("secret key: {}".format(app.secret_key))



@app.route('/', methods=['GET', 'POST'])
@app.route("/index", methods=['GET', 'POST'])
def index():
    form = SummonerSearchForm()
    if form.validate_on_submit():
        flash("Searched for {}".format(form.summoner.data), 'success')
        return redirect(url_for('search_name', summoner_name=form.summoner.data))
    return render_template('index.html', form=form)


@app.route('/summoner/name/<summoner_name>', methods=['GET', 'POST'])
def search_name(summoner_name):
    form = SummonerSearchForm()
    if form.validate_on_submit():
        flash("Searched for {}".format(form.summoner.data), 'success')
        return redirect(url_for('search_name', summoner_name=form.summoner.data))
    rh = RequestHandler(db, api_endpoint=os.environ.get('API_ENDPOINT'), api_key=os.environ.get('API_KEY'))
    sum = rh.insert_or_update_summoner(summoner_name)
    return render_template('summoner.html', summoner=sum, form=form)


@app.route("/test")
def test():
    form = SummonerSearchForm()
    if form.validate_on_submit():
        flash("Searched for {}".format(form.summoner.data), 'success')
        return redirect(url_for('search_name', summoner_name=form.summoner.data))
    app.logger.info(os.environ.get('API_ENDPOINT'))
    app.logger.info(os.environ.get('API_KEY'))
    rh = RequestHandler(db, api_endpoint=os.environ.get('API_ENDPOINT'), api_key=os.environ.get('API_KEY'))
    # rh.update_recent_usermatches(rh.get_accountid_by_name('colorless'))
    sums = rh.get_all_summoners()
    matches = rh.get_all_usermatches()
    app.logger.info(sums)
    return render_template('test.html', summoners=sums, matches=matches, form=form)


def main():
    # Create logs dir if it doesn't exist
    if not os.path.exists('logs/'):
        os.mkdir('logs/')

    load_config()

    logging.config.dictConfig(get_logger_config())

    # initialize logger
    logger = logging.getLogger(__name__)

    logger.info('Initializing RequestHandler')
    rh = RequestHandler()

    # Proof of concept
    #    rh.insert_or_update_summoner('wellthisisawkwrd')
    #    accid = rh.get_accountid_by_name('wellthisisawkwrd')
    #    rh.update_recent_usermatches(accid)

    # launch()


if __name__ == '__main__':
    main()

import logging
import os

from flask import render_template, redirect, url_for

from app import db
from app.main import bp
from app.main.forms import SummonerSearchForm
from app.util import RequestHandler

logger = logging.getLogger(__name__)


@bp.route('/', methods=['GET', 'POST'])
@bp.route("/index", methods=['GET', 'POST'])
def index():
    form = SummonerSearchForm()
    if form.validate_on_submit():
        # flash("Searched for {}".format(form.summoner.data), 'success')
        return redirect(url_for('main.search_name', summoner_name=form.summoner.data))
    return render_template('index.html', form=form)


@bp.route('/summoner/name/<summoner_name>', methods=['GET', 'POST'])
def search_name(summoner_name):
    form = SummonerSearchForm()
    if form.validate_on_submit():
        # flash("Searched for {}".format(form.summoner.data), 'success')
        return redirect(url_for('main.search_name', summoner_name=form.summoner.data))
    rh = RequestHandler(db, api_endpoint=os.environ.get('API_ENDPOINT'), api_key=os.environ.get('API_KEY'))
    # For now we will update all summoner information on search
    retrieved_sum = rh.insert_or_update_summoner(summoner_name)
    rh.update_recent_usermatches(retrieved_sum.accountid)
    rh.update_leagues(retrieved_sum.id)
    return render_template('summoner.html', summoner=retrieved_sum, form=form)


@bp.route("/test", methods=['GET', 'POST'])
def test():
    form = SummonerSearchForm()
    if form.validate_on_submit():
        # flash("Searched for {}".format(form.summoner.data), 'success')
        return redirect(url_for('main.search_name', summoner_name=form.summoner.data))
    logger.info(os.environ.get('API_ENDPOINT'))
    logger.info(os.environ.get('API_KEY'))
    rh = RequestHandler(db, api_endpoint=os.environ.get('API_ENDPOINT'), api_key=os.environ.get('API_KEY'))
    sums = rh.get_all_summoners()
    matches = rh.get_all_db_usermatches()
    leagues = rh.get_all_userleagues()
    return render_template('test.html', summoners=sums, matches=matches, leagues=leagues, form=form)

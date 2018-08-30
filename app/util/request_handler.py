import logging

from app.flask_models import Summoner, UserMatch
from app.wrappers import riot_request


class RequestHandler:
    def __init__(self, db, api_endpoint=None, api_key=None):
        self.logger = logging.getLogger(__name__)
        self.logger.info("Init RequestHandler")
        self.api_endpoint = api_endpoint
        self.api_key = api_key
        # Init RiotConnector
        self.rc = riot_request.RiotConnector(self.api_endpoint, self.api_key)

        # Init DB Session
        self.db = db

        self.logger.info(self)

    def __repr__(self):
        return "<RequestHandler(api_endpoint = {}, api_key = {})>".format(self.api_endpoint, self.api_key)

    def close(self):
        self.logger.info("session closed")
        self.db.session.close()

    def get_all_summoners(self):
        self.logger.info("returning all summoners")
        q = self.db.session.query(Summoner).all()
        self.logger.debug(q)
        return q

    def get_all_usermatches(self):
        self.logger.info("returning all usermatches")
        q = self.db.session.query(UserMatch).all()
        self.logger.debug(q)
        return q

    def get_or_create(self, model, **kwargs):
        self.logger.info("get or create on {}".format(model.__tablename__))
        item = self.db.session.query(model).filter_by(**kwargs).first()
        if item:
            self.logger.info("item exists: {}".format(item))
            return item
        else:
            self.logger.info("item does not exist, creating it now")
            item = model(**kwargs)
            self.logger.debug("created {}, adding item to db now".format(item))
            self.db.session.add(item)
            return item

    def get_accountid_by_name(self, name):
        self.logger.info("Getting accountid for {}".format(name))
        q = self.db.session.query(Summoner).filter(Summoner.name.ilike('%{}%'.format(name)))
        summoner = q.first()
        if summoner:
            self.logger.debug("exists: {}".format(summoner))
            return summoner.accountid
        else:
            self.logger.debug("Doesn't exist, calling insert_or_update_summoner")
            self.insert_or_update_summoner(name)
            return self.get_accountid_by_name(name)

    def insert_or_update_summoner(self, name):
        self.logger.info("insert or update summoner: {}".format(name))
        summoner_json = RequestHandler.lower_keys(self.rc.getSummoner(name))
        summoner = Summoner(**summoner_json)
        self.logger.debug("Summoner constructed: {}".format(summoner))
        self.db.session.merge(summoner)
        self.db.session.commit()
        return summoner

    def update_recent_usermatches(self, accountid):
        self.logger.info("Update recent usermatches for account id: {}".format(accountid))
        # Get recent matches from API
        matchlist_json = self.rc.getSummonerMatchList(accountid)
        self.logger.debug("Matchlist json: ".format(matchlist_json))
        for match in matchlist_json['matches']:
            match['accountid'] = accountid
            self.get_or_create(UserMatch, **RequestHandler.lower_keys(match))
        self.db.session.commit()

    @staticmethod
    def lower_keys(somejson):
        return {k.lower(): v for k, v in somejson.items()}

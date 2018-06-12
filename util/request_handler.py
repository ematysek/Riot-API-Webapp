from wrappers import riot_request
from model.models import *
from model import models
from sqlalchemy.orm import sessionmaker


class RequestHandler:
    def __init__(self, api_endpoint, api_key, db_file):
        self.api_endpoint = api_endpoint
        self.api_key = api_key
        self.db_file = db_file
        # Init RiotConnector
        self.rc = riot_request.RiotConnector(api_endpoint, api_key)

        # Init DB Session
        self.dbengine = models.db_connect(db_file)
        models.create_tables(self.dbengine)
        Session = sessionmaker(bind=self.dbengine)
        self.session = Session()

    def __repr__(self):
        return "<RequestHandler(api_endpoint = {}, api_key = {}, db_file = {})>".format(self.api_endpoint, self.api_key,
                                                                                        self.db_file)

    def get_or_create(self, model, **kwargs):
        item = self.session.query(model).filter_by(**kwargs).first()
        if item:
            return item
        else:
            item = model(**kwargs)
            self.session.add(item)
            return item

    def get_accountid_by_name(self, name):
        q = self.session.query(Summoner).filter(Summoner.name.ilike('%{}%'.format(name)))
        summoner = q.first()
        if summoner:
            return summoner.accountid
        else:
            self.insert_or_update_summoner(name)
            return self.get_accountid_by_name(name)

    def insert_or_update_summoner(self, name):
        summoner_json = RequestHandler.lower_keys(self.rc.getSummoner(name))
        summoner = Summoner(**summoner_json)
        self.session.merge(summoner)
        self.session.commit()

    def update_recent_usermatches(self, accountid):
        # Get recent matches from API
        matchlist_json = self.rc.getSummonerMatchList(accountid)
        for match in matchlist_json['matches']:
            match['accountid'] = accountid
            self.get_or_create(UserMatch, **RequestHandler.lower_keys(match))
        self.session.commit()

    @staticmethod
    def lower_keys(somejson):
        return {k.lower(): v for k, v in somejson.items()}

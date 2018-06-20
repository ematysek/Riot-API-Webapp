from sqlalchemy.orm import sessionmaker

from conf.config import DBConfig, APIConfig
from model import models
from model.models import *
from wrappers import riot_request

# It may be better to move this to package level __init__.py
Session = sessionmaker()
logger = logging.getLogger(__name__)


class RequestHandler:
    def __init__(self, api_endpoint=None, api_key=None, db_file=None):
        logger.info("Init RequestHandler")
        self.api_endpoint = api_endpoint or APIConfig().api_endpoint
        self.api_key = api_key or APIConfig().api_key
        self.db_file = db_file or DBConfig().db_file
        # Init RiotConnector
        self.rc = riot_request.RiotConnector(self.api_endpoint, self.api_key)

        # Init DB Session
        self.dbengine = models.db_connect(self.db_file)
        models.create_tables(self.dbengine)
        Session.configure(bind=self.dbengine)
        self.session = Session()
        logger.info(self)

    def __repr__(self):
        return "<RequestHandler(api_endpoint = {}, api_key = {}, db_file = {})>".format(self.api_endpoint, self.api_key,
                                                                                        self.db_file)

    def close(self):
        logger.info("session closed")
        self.session.close()

    def get_all_summoners(self):
        logger.info("returning all summoners")
        q = self.session.query(Summoner).all()
        logger.debug(q)
        return q

    def get_all_usermatches(self):
        logger.info("returning all usermatches")
        q = self.session.query(UserMatch).all()
        logger.debug(q)
        return q

    def get_or_create(self, model, **kwargs):
        logger.debug("get or create on {}".format(model.__tablename__))
        item = self.session.query(model).filter_by(**kwargs).first()
        if item:
            logger.debug("item exists: {}".format(item))
            return item
        else:
            logger.debug("item does not exist, creating it now")
            item = model(**kwargs)
            logger.debug("created {}, adding item to db now".format(item))
            self.session.add(item)
            return item

    def get_accountid_by_name(self, name):
        logger.info("Getting accountid for {}".format(name))
        q = self.session.query(Summoner).filter(Summoner.name.ilike('%{}%'.format(name)))
        summoner = q.first()
        if summoner:
            logger.debug("exists: {}".format(summoner))
            return summoner.accountid
        else:
            logger.debug("Doesn't exist, calling insert_or_update_summoner")
            self.insert_or_update_summoner(name)
            return self.get_accountid_by_name(name)

    def insert_or_update_summoner(self, name):
        logger.info("insert or update summoner: {}".format(name))
        summoner_json = RequestHandler.lower_keys(self.rc.getSummoner(name))
        summoner = Summoner(**summoner_json)
        logger.debug("Summoner constructed: {}".format(summoner))
        self.session.merge(summoner)
        self.session.commit()

    def update_recent_usermatches(self, accountid):
        logger.info("Update recent usermatches for account id: {}".format(accountid))
        # Get recent matches from API
        matchlist_json = self.rc.getSummonerMatchList(accountid)
        logger.debug("Matchlist json: ".format(matchlist_json))
        for match in matchlist_json['matches']:
            match['accountid'] = accountid
            self.get_or_create(UserMatch, **RequestHandler.lower_keys(match))
        self.session.commit()

    @staticmethod
    def lower_keys(somejson):
        return {k.lower(): v for k, v in somejson.items()}

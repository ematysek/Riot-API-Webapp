import logging
from typing import Optional

from app.flask_models import Summoner, UserMatch, UserLeague
from app.wrappers import RiotConnector


class RequestHandler:
    def __init__(self, db, api_endpoint=None, api_key=None):
        self.logger = logging.getLogger(__name__)
        self.logger.info("Init RequestHandler")
        self.api_endpoint = api_endpoint
        self.api_key = api_key
        # Init RiotConnector
        self.rc = RiotConnector(self.api_endpoint, self.api_key)

        # Init DB Session
        self.db = db

        self.logger.info(self)

    def __repr__(self):
        return "<RequestHandler(api_endpoint = {}, api_key = {})>".format(self.api_endpoint, self.api_key)

    def close(self):
        self.logger.info("session closed")
        self.db.session.close()

    def get_all_summoners(self):
        """
        Get all Summoners currently in the DB.
        :rtype: List[Summoner]
        :return: List of all summoners in the DB
        """
        self.logger.info("returning all summoners")
        q = self.db.session.query(Summoner).all()
        self.logger.debug(q)
        return q

    def get_all_usermatches(self):
        """
        Get all UserMatches currently in the DB.
        :return: List of all UserMatch objs in the DB
        """
        self.logger.info("returning all usermatches")
        q = self.db.session.query(UserMatch).all()
        self.logger.debug(q)
        return q

    def get_all_userleagues(self):
        """
        Get all UserLeagues currently in the DB.
        :return: List of all UserLeague objs in the DB
        """
        self.logger.info("Returning all userleagues")
        q = UserLeague.query.all()
        self.logger.debug(q)
        return q

    def get_or_create(self, model, **kwargs):
        """
        If an object matching the kwargs provided exists, then return that object.
        Otherwise, create the object and insert it into the DB.

        Useful for tables with static data.
        :param model: DB Model you want to create
        :param kwargs: kwargs needed to create that Model
        :return: Created Model object
        """
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

    def get_summoner_by_name(self, name: str) -> Optional[Summoner]:
        """
        Get the Summoner object by specified name.
        If the Summoner does not exist in the DB, then we call `insert_or_update_summoner'.

        This method is useful because Summoner attributes summonerid and accountid don't change, so in functions that
        just need these attributes we do not need to make an API call if the summoner exists in the DB.

        :param name: name of summoner to return
        :return: Summoner model object or None if the summoner was not found in the DB and there was an issue retrieving
                  it from the API
        """
        self.logger.info("Getting Summoner: {}".format(name))
        # Check db first
        q = self.db.session.query(Summoner).filter(Summoner.name.ilike('%{}%'.format(name)))
        summoner = q.first()
        if summoner:
            self.logger.info("Summoner found in db: {}".format(summoner))
            return summoner
        else:
            self.logger.info("Summoner not found in db: {}".format(summoner))
            return self.insert_or_update_summoner(name)

    def insert_or_update_summoner(self, name: str) -> Optional[Summoner]:
        """
        Insert or update the Summoner with the given name by querying the API for the most recent Summoner data.
        If the Summoner does not exist in summoners table then we insert, otherwise update the existing data.
        :param name: Name of the Summoner to update
        :return: Summoner object or none if we got an unexpected response from the API
        """
        self.logger.info("insert or update summoner: {}".format(name))
        summoner_json = self.rc.getSummoner(name)
        if not summoner_json:
            self.logger.warning("Summoner JSON not returned by RiotConnector for name: {}".format(name))
            return None
        summoner_json = RequestHandler.lower_keys(summoner_json)
        summoner = Summoner(**summoner_json)
        self.logger.debug("Summoner constructed: {}".format(summoner))
        self.db.session.merge(summoner)
        self.db.session.commit()
        return summoner

    def update_leagues(self, summonerid: int):
        """
        Get most recent leagues info from API for summonerid and update user_leagues table accordingly
        :param summonerid: summonerid for the Summoner we want to grab updated league info for
        """
        self.logger.info("Update leagues info for summonerid: {}".format(summonerid))
        # Get leagues data from API
        leagues_json = self.rc.get_summoner_leagues_by_summoner_id(summonerid)
        if not leagues_json:
            self.logger.warning("Leagues JSON not returned by RiotCeonnector for summonerid: {}".format(summonerid))
            return
        # leagues_json = RequestHandler.lower_keys(leagues_json)
        self.logger.debug("Leagues json for summonerid {}: {}".format(summonerid, leagues_json))
        for league_dict in leagues_json:
            league_dict['summonerid'] = summonerid
            # If an entry exists for this summonerid and queuetype, then update it, otherwise add new entry
            existing = UserLeague.query.filter_by(summonerid=summonerid, queuetype=league_dict['queueType']).first()
            if existing:
                self.logger.info("Existing league info found for summoner id: {}, queue: {}".format(summonerid,
                                                                                                    league_dict[
                                                                                                        'queueType']))
                self.logger.debug("Updating with values: {}".format(RequestHandler.lower_keys(league_dict)))
                for k, v in RequestHandler.lower_keys(league_dict).items():
                    setattr(existing, k, v)
            else:
                self.db.session.add(UserLeague(**RequestHandler.lower_keys(league_dict)))
        self.db.session.commit()

    def update_recent_usermatches(self, accountid: int):
        """
        Get 100 most recent matches and insert them into the DB if they don't exist already.
        :param accountid: accountid for the Summoner we want to grab updated user match info for
        """
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

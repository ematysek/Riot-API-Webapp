import logging
import time

import requests


class RiotConnector:
    def __init__(self, api_endpoint, api_key):
        self.logger = logging.getLogger(__name__)
        self.api_endpoint = api_endpoint
        self.api_key = api_key
        self.logger.info('RiotConnector constructed: {}'.format(self))

    def __repr__(self):
        return "<RiotConnector(api_endpoint = {}, api_key = {})>".format(self.api_endpoint, self.api_key)

    def getSummoner(self, name):
        self.logger.info('getsummoner called')
        payload = {'api_key': self.api_key}
        start = time.time()
        r = requests.get(self.api_endpoint + '/lol/summoner/v3/summoners/by-name/' + str(name), params=payload)
        time_taken = time.time() - start
        self.logger.info("get_summoner {} time taken: {}".format(name, time_taken))
        self.logger.info('url used: %s', r.url)
        self.logger.info("response code: {}".format(r.status_code))
        if not r.status_code == 200:
            return None
        return r.json()

    def getSummonerMatchList(self, accountid):
        self.logger.info('getSummonerMatchList called')
        payload = {'api_key': self.api_key}
        start = time.time()
        response = requests.get(self.api_endpoint + '/lol/match/v3/matchlists/by-account/' + str(accountid),
                                params=payload)
        time_taken = time.time() - start
        self.logger.info("getSummonerMatchList {} time taken: {}".format(accountid, time_taken))
        self.logger.info('Response URL: %s', response.url)
        self.logger.info("response code: {}".format(response.status_code))
        return response.json()

    def getSummonerMmrBySummonerId(self, summonerid):
        self.logger.info('getSummonerMmrBySummonerId called')
        payload = {'api_key': self.api_key}
        start = time.time()
        response = requests.get(self.api_endpoint + '/lol/league/v3/mmr-af/by-summoner/' + str(summonerid),
                                params=payload)
        time_taken = time.time() - start
        self.logger.info("getSummonerMmrBySummonerId {} time taken: {}".format(summonerid, time_taken))
        self.logger.info('Response URL: %s', response.url)
        self.logger.info("response code: {}".format(response.status_code))
        return response.json()

    def get_summoner_leagues_by_summoner_id(self, summonerid):
        self.logger.info("Getting leagues for summonerid: {}".format(summonerid))
        payload = {'api_key': self.api_key}
        start = time.time()
        response = requests.get("{}/lol/league/v3/positions/by-summoner/{}".format(self.api_endpoint, summonerid),
                                params=payload)
        time_taken = time.time() - start
        self.logger.info("get_summoner_leagues_by_summoner_id {} time taken: {}".format(summonerid, time_taken))
        self.logger.info("Response URL: {}".format(response.url))
        self.logger.info("Response code: {}".format(response.status_code))
        if not response.status_code == 200:
            return None
        return response.json()

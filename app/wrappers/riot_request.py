import logging

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
        r = requests.get(self.api_endpoint + '/lol/summoner/v3/summoners/by-name/' + str(name), params=payload)
        self.logger.info('url used: %s', r.url)
        self.logger.info("response code: {}".format(r.status_code))
        return r.json()

    def getSummonerMatchList(self, accountid):
        self.logger.info('getSummonerMatchList called')
        payload = {'api_key': self.api_key}
        response = requests.get(self.api_endpoint + '/lol/match/v3/matchlists/by-account/' + str(accountid),
                                params=payload)
        self.logger.info('Response URL: %s', response.url)
        self.logger.info("response code: {}".format(response.status_code))
        return response.json()

    def getSummonerMmrBySummonerId(self, summonerid):
        self.logger.info('getSummonerMmrBySummonerId called')
        payload = {'api_key': self.api_key}
        response = requests.get(self.api_endpoint + '/lol/league/v3/mmr-af/by-summoner/' + str(summonerid),
                                params=payload)
        self.logger.info('Response URL: %s', response.url)
        self.logger.info("response code: {}".format(response.status_code))
        return response.json()

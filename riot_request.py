import requests
import logging

logger = logging.getLogger('app.riot_request')


class RiotConnector:
    def __init__(self, api_endpoint, api_key):
        self.api_endpoint = api_endpoint
        self.api_key = api_key
        logger.info('RiotConnector constructed: {}'.format(self))
        logger.info('api_endpoint: %s', api_endpoint)
        logger.info('api_key: %s', api_key)

    def __repr__(self):
        return "<RiotConnector(api_endpoint = {}, api_key = {})>".format(self.api_endpoint, self.api_key)

    def getSummoner(self, name):
        logger.info('getsummoner called')
        # logging.basicConfig(level=logging.DEBUG)
        payload = {'api_key': self.api_key}
        r = requests.get(self.api_endpoint + '/lol/summoner/v3/summoners/by-name/' + str(name), params=payload)
        logger.info('url used: %s', r.url)
        return r.json()

    def getSummonerMatchList(self, accountid):
        logger.info('getSummonerMatchList called')
        payload = {'api_key': self.api_key}
        response = requests.get(self.api_endpoint + '/lol/match/v3/matchlists/by-account/' + str(accountid),
                                params=payload)
        logger.info('Response URL: %s', response.url)
        return response.json()

    def getSummonerMmrBySummonerId(self, summonerid):
        logger.info('getSummonerMmrBySummonerId called')
        payload = {'api_key': self.api_key}
        response = requests.get(self.api_endpoint + '/lol/league/v3/mmr-af/by-summoner/' + str(summonerid),
                                params=payload)
        logger.info('Rsponse URL: %s', response.url)
        return response.json()

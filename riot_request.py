import requests
import logging

logger = logging.getLogger('app.riot_request')


class RiotConnector:
    def __init__(self, apiEndpoint, apiKey):
        self.apiEndpoint = apiEndpoint
        self.apiKey = apiKey
        logger.info('riotconnector constructed')
        logger.info('apiEndpoint: %s', apiEndpoint)
        logger.info('apiKey: %s', apiKey)

    def getSummoner(self, name):
        logger.info('getsummoner called')
        # logging.basicConfig(level=logging.DEBUG)
        payload = {'api_key': self.apiKey}
        r = requests.get(self.apiEndpoint + '/lol/summoner/v3/summoners/by-name/' + str(name), params=payload)
        logger.info('url used: %s', r.url)
        return r.json()

    def getSummonerMatchList(self, accountid):
        logger.info('getSummonerMatchList called')
        payload = {'api_key': self.apiKey}
        response = requests.get(self.apiEndpoint + '/lol/match/v3/matchlists/by-account/' + str(accountid),
                                params=payload)
        logger.info('Response URL: %s', response.url)
        return response.json()

    def getSummonerMmrBySummonerId(self, summonerid):
        logger.info('getSummonerMmrBySummonerId called')
        payload = {'api_key': self.apiKey}
        response = requests.get(self.apiEndpoint + '/lol/league/v3/mmr-af/by-summoner/' + str(summonerid),
                                params=payload)
        logger.info('Rsponse URL: %s', response.url)
        return response.json()

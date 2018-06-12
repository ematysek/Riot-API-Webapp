# This file is deprecated
import mysql.connector as mariadb
import logging

logger = logging.getLogger('app.db_request')


class DBConnector:

    def __init__(self, user, password, database):
        logger.info('DBConnector constructed')
        logger.info('user: %s', user)
        logger.info('database: %s', database)
        self.mariadb_connection = mariadb.connect(user=user, password=password, database=database)
        self.cursor = self.mariadb_connection.cursor()

    # TODO rename id parameter to be more descriptive
    def insertSummoner(self, id, accountid, name, profileiconid, revisiondate, summonerlevel):
        logger.info('Attempting to insert summoner - ' + name)
        query = "INSERT users VALUES(" + id + "," + accountid + ",'" + name + "'," + profileiconid + "," + revisiondate + "," + summonerlevel + ");"
        logger.info('execute query: %s', query)
        # self.cursor.execute("INSERT users VALUES(" + id + "," + accountid + ",'" + name + "'," + profileiconid + "," + revisiondate + "," + summonerlevel + ");")
        self.cursor.execute(query)
        # result = self.cursor.fetchall()
        # for row in result:
        #	print(row)
        self.mariadb_connection.commit()
        logger.info('commit')
        return

    def insertSummonerMatchesJSON(self, accountid, matchesJSON):
        logger.info('insertSummonerMatchesJSON called for accountid %s', accountid)
        matchesArray = matchesJSON['matches']
        for match in matchesArray:
            query = "INSERT user_matches VALUES({0}, '{lane}', {gameId}, {champion}, '{platformId}', {timestamp}, {queue}, '{role}', {season})".format(
                accountid, **match)
            logger.debug('executing query: %s', query)
            self.cursor.execute(query)
        logger.info('commit')
        self.mariadb_connection.commit()
        return

    def getAllUsers(self):
        query = "SELECT * FROM users;"
        logger.info('return all rows from users table using query: %s', query)
        self.cursor.execute(query)
        result = self.cursor.fetchall()
        for row in result:
            logger.debug(row)
        # each row of result is a tuple
        return result

    def getSummoner(self, name):
        query = "SELECT * FROM users WHERE name = '" + name + "'"
        logger.info('attempting to get summoner ' + name + ' using: %s', query)
        self.cursor.execute(query)
        result = self.cursor.fetchall()
        for row in result:
            logger.debug(row)
        return result

    def getSummonerInfo(self, name, col):
        query = "SELECT " + col + " FROM users WHERE name = '" + name + "'"
        logger.info('Get %s for summoner %s using: %s', col, name, query)
        self.cursor.execute(query)
        result = self.cursor.fetchall()
        for row in result:
            logger.debug(row)
        return result

    def getSummonerAccountId(self, name):
        """Returns the accountID for the corresponding name as a string from the DB"""
        query = "SELECT accountid FROM users WHERE name ='" + name + "'"
        logger.info('Get accountid for summoner %s using: %s', name, query)
        self.cursor.execute(query)
        result = self.cursor.fetchall()
        for row in result:
            logger.debug(row)
        return result[0][0]

    def insertSummonerMmr(self, summonerId, tier, name, analysis, mmr):
        logger.info('insertSummonerMmr called for summoner id %s', summonerId)
        query = "INSERT users VALUES(" + summonerId + ",'" + tier + "','" + name + "','" + analysis + "'," + mmr + ");"
        logger.info('executing query: %s', query)
        self.cursor.execute(query)
        self.mariadb_connection.commit()
        logger.info('commit')
        return

    def close(self):
        logger.info('Closing DB connection')
        self.mariadb_connection.close()
        return

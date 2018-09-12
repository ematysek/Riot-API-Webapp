from app import db


class Summoner(db.Model):
    # TODO probably need to implement a searchable_name column since League does not care about capatalization or whitespace
    __tablename__ = 'summoners'

    id = db.Column(db.Integer, primary_key=True, nullable=False)  # summonerid
    accountid = db.Column(db.Integer, unique=True, nullable=False)
    name = db.Column(db.String, index=True)
    profileiconid = db.Column(db.Integer)
    revisiondate = db.Column(db.TIMESTAMP)
    summonerlevel = db.Column(db.Integer)
    last_updated = db.Column(db.TIMESTAMP, server_default=db.func.now(), onupdate=db.func.now())

    matches = db.relationship("UserMatch", back_populates="summoner")
    leagues = db.relationship("UserLeague", back_populates="summoner")

    def __repr__(self):
        return "<Summoner(id={}, accountid={}, name={}, profileiconid={}, revisiondate={}, summonerlevel={})>" \
            .format(self.id, self.accountid, self.name, self.profileiconid, self.revisiondate,
                    self.summonerlevel)


class UserMatch(db.Model):
    __tablename__ = 'user_matches'

    id = db.Column(db.Integer, primary_key=True)
    accountid = db.Column(db.Integer, db.ForeignKey('summoners.accountid'), index=True)
    gameid = db.Column(db.BigInteger, db.ForeignKey('matches.gameid'), index=True)
    lane = db.Column(db.String)
    champion = db.Column(db.Integer)
    platformid = db.Column(db.String)
    timestamp = db.Column(db.TIMESTAMP)
    queue = db.Column(db.Integer)
    role = db.Column(db.String)
    season = db.Column(db.Integer)

    summoner = db.relationship("Summoner", back_populates="matches")
    match = db.relationship("Match", back_populates="user_matches")

    def __repr__(self):
        return "<UserMatch(accountid={}, lane={}, gameid={}, champion={}, platformid={}, timestamp={}, queue={}," \
               "role={}, season={})>".format(self.accountid, self.lane, self.gameid, self.champion, self.platformid,
                                             self.timestamp, self.queue, self.role, self.season)


class UserLeague(db.Model):
    __tablename__ = "user_leagues"

    id = db.Column(db.Integer, primary_key=True)
    summonerid = db.Column(db.Integer, db.ForeignKey('summoners.id'), index=True)
    queuetype = db.Column(db.String)
    wins = db.Column(db.Integer)
    losses = db.Column(db.Integer)
    rank = db.Column(db.String)
    tier = db.Column(db.String)
    leaguepoints = db.Column(db.Integer)
    hotstreak = db.Column(db.Boolean)
    veteran = db.Column(db.Boolean)
    playerorteamid = db.Column(db.Integer)
    leaguename = db.Column(db.String)
    playerorteamname = db.Column(db.String)
    inactive = db.Column(db.Boolean)
    freshblood = db.Column(db.Boolean)
    leagueid = db.Column(db.String)

    summoner = db.relationship("Summoner", back_populates="leagues")

    def __repr__(self):
        return "<UserLeague(summonerid={}, queuetype={}, wins={}, losses={}, rank={}, teir={}, leaguepoint={}, " \
               "hotstreak={}, veteran={}, playerorteamid={}, leaguename={}, playerorteamname={}, inactive={}, " \
               "freshblood={}, leagueid={})>".format(self.summonerid, self.queuetype, self.wins, self.losses, self.rank,
                                                     self.tier, self.leaguepoints, self.hotstreak, self.veteran,
                                                     self.playerorteamid, self.leaguename, self.playerorteamname,
                                                     self.inactive, self.freshblood, self.leagueid)


class Match(db.Model):
    __tablename__ = "matches"

    gameid = db.Column(db.BigInteger, primary_key=True)
    seasonid = db.Column(db.Integer)
    queueid = db.Column(db.Integer)
    gameversion = db.Column(db.String)
    gameduration = db.Column(db.Integer)
    gamecreation = db.Column(db.TIMESTAMP)

    user_matches = db.relationship("UserMatch", back_populates="match")

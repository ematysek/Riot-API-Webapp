from app import db


class Summoner(db.Model):
    __tablename__ = 'summoners'

    id = db.Column(db.Integer, primary_key=True, nullable=False)  # summonerid
    accountid = db.Column(db.Integer, primary_key=True, nullable=False)
    name = db.Column(db.String, index=True)
    profileiconid = db.Column(db.Integer)
    revisiondate = db.Column(db.Integer)
    summonerlevel = db.Column(db.Integer)

    matches = db.relationship("UserMatch", back_populates="summoner")

    def __repr__(self):
        return "<Summoner(id={}, accountid={}, name={}, profileiconid={}, revisiondate={}, summonerlevel={})>" \
            .format(self.id, self.accountid, self.name, self.profileiconid, self.revisiondate,
                    self.summonerlevel)


class UserMatch(db.Model):
    __tablename__ = 'user_matches'

    id = db.Column(db.Integer, primary_key=True)
    accountid = db.Column(db.Integer, db.ForeignKey('summoners.accountid'))
    lane = db.Column(db.String)
    gameid = db.Column(db.Integer)
    champion = db.Column(db.Integer)
    platformid = db.Column(db.String)
    timestamp = db.Column(db.Integer)
    queue = db.Column(db.Integer)
    role = db.Column(db.String)
    season = db.Column(db.Integer)

    summoner = db.relationship("Summoner", back_populates="matches")

    def __repr__(self):
        return "<UserMatch(accountid={}, lane={}, gameid={}, champion={}, platformid={}, timestamp={}, queue={}," \
               "role={}, season={})>".format(self.accountid, self.lane, self.gameid, self.champion, self.platformid,
                                             self.timestamp, self.queue, self.role, self.season)

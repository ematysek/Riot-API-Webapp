from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship

Base = declarative_base()


def db_connect(db_file):
    # TODO move db to config file
    return create_engine('sqlite:///{}'.format(db_file))


def create_tables(engine):
    Base.metadata.create_all(engine)


class Summoner(Base):
    __tablename__ = 'summoners'

    id = Column(Integer, primary_key=True, nullable=False)  # summonerid
    accountid = Column(Integer, primary_key=True, nullable=False)
    name = Column(String)
    profileiconid = Column(Integer)
    revisiondate = Column(Integer)
    summonerlevel = Column(Integer)

    matches = relationship("UserMatch", back_populates="summoner")

    def __repr__(self):
        return "<Summoner(id={}, accountid={}, name={}, profileiconid={}, revisiondate={}, summonerlevel={})>" \
            .format(self.id, self.accountid, self.name, self.profileiconid, self.revisiondate,
                    self.summonerlevel)


class UserMatch(Base):
    __tablename__ = 'user_matches'

    id = Column(Integer, primary_key=True)
    accountid = Column(Integer, ForeignKey('summoners.accountid'))
    lane = Column(String)
    gameid = Column(Integer)
    champion = Column(Integer)
    platformid = Column(String)
    timestamp = Column(Integer)
    queue = Column(Integer)
    role = Column(String)
    season = Column(Integer)

    summoner = relationship("Summoner", back_populates="matches")

    def __repr__(self):
        return "<UserMatch(accountid={}, lane={}, gameid={}, champion={}, platformid={}, timestamp={}, queue={}," \
               "role={}, season={})>".format(self.accountid, self.lane, self.gameid, self.champion, self.platformid,
                                             self.timestamp, self.queue, self.role, self.season)

#!./venv/bin/python3

from sqlalchemy import Column, Integer, String, Float, DateTime
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import create_engine

Base = declarative_base()

class Sentiment_ent(Base):
    __tablename__ = 'sentiments'
    Id = Column(Integer, primary_key = True, nullable = False)
    Time = Column(DateTime)
    Candidate = Column(String)
    Count = Column(Integer)
    Sentiment = Column(Float)

    def __str__(self):
        return '%d:\t%s\t%s\t%d\t%.1f' % (self.Id, str(self.Time),
                                          self.Candidate, self.Count,
                                          self.Sentiment)

engine = create_engine('sqlite:///election.sqlite')
Base.metadata.create_all(engine)

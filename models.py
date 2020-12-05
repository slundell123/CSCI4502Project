from sqlalchemy import Column, Float, ForeignKey, Integer, String
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship

Base = declarative_base()

# this file is where we model Python classes after our db tables


class Review(Base):
    __tablename__ = "reviews"
    reviewid = Column(Integer, primary_key=True)
    title = Column(String)
    artist = Column(String)
    url = Column(String)
    score = Column(Float)
    best_new_music = Column(Integer)
    author = Column(String)
    author_type = Column(String)
    pub_date = Column(String)
    pub_weekday = Column(Integer)
    pub_month = Column(Integer)
    pub_year = Column(Integer)

    def __repr__(self):
        return f"<Review(id={self.reviewid}, title='{self.title}'), artist='{self.artist}', score={self.score}>"


class Content(Base):
    __tablename__ = "content"
    reviewid = Column(Integer, primary_key=True)
    content = Column(String)
    sentiment = Column(Integer)  # 0 = negative, 1 = positive

    def __repr__(self):
        return f"<Content(id={self.reviewid})>"

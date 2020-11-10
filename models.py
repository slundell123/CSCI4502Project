from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Integer, String, Float

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


class Genre(Base):
    __tablename__ = "genres"
    reviewid = Column(Integer, primary_key=True)
    genre = Column(String)

    def __repr__(self):
        return f"<Genre(id={self.reviewid}, genre='{self.genre}')"

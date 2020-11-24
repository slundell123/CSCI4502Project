import logging
import os
import numpy as np
import matplotlib.pylab as plt

from dotenv import load_dotenv
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.sql import func

from models import Review
from models import Genre

# enviornment variables setup
load_dotenv()
PSQL_CONNECTION_STRING = os.getenv("PSQL_CONNECTION_STRING")
# logging setup. See sqlalchemy.log to view generated sql statements
handler = logging.FileHandler("sqlalchemy.log")
handler.setLevel(logging.INFO)
logger = logging.getLogger("sqlalchemy")
logger.addHandler(handler)
logger.setLevel(logging.DEBUG)

if __name__ == "__main__":
    engine = create_engine(PSQL_CONNECTION_STRING, echo=False)
    Session = sessionmaker(bind=engine)
    session = Session()

    # query get average score of ratings for each year
    averageScores = session.query(func.avg(Review.score), Review.pub_year).group_by(Review.pub_year).all()

    # query get average score of ratings for each year
    bestNewMusicScores = session.query(Review.score).filter(Review.best_new_music == 1).all()
    bestNewMusicOrNotScores = (
        session.query(Review.best_new_music, func.array_agg(Review.score)).group_by(Review.best_new_music).all()
    )
    # Join query for Genre and Review to see reviews by genre
    averageReviewsScoreByGenre = (
        session.query(Genre.genre, func.avg(Review.score))
        .filter(Genre.genre != None, Review.best_new_music == 1)
        .join(Review, Genre.reviewid == Review.reviewid)
        .group_by(Genre.genre)
        .all()
    )

    # Lists of scores by genre
    allScoresByGenre = (
        session.query(Genre.genre, func.array_agg(Review.score))
        .filter(Genre.genre != None)
        .join(Review, Genre.reviewid == Review.reviewid)
        .group_by(Genre.genre)
        .all()
    )

    for i in allScoresByGenre:
        bestMusic = np.random.choice(i[1], size=len(bestNewMusicOrNotScores[1][1]))
        print("Genre: ", i[0])
        corrCoef = np.corrcoef(bestMusic, bestNewMusicOrNotScores[1][1])
        print("Correlation coef, best new music: ", corrCoef[0][1])
        notBestMusic = np.random.choice(i[1], size=len(bestNewMusicOrNotScores[1][1]))
        corrCoefNotBest = np.corrcoef(notBestMusic, bestNewMusicOrNotScores[1][1])
        print("Correlation coef, not best new music: ", corrCoefNotBest[0][1])

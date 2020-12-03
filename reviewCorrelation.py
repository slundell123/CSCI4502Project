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


def getCorrelationCoef(setA, setB, numTests):
    corrCoef = 0
    for i in range(numTests):
        bestMusic = np.random.choice(setA, size=len(setB))
        corrCoef += np.corrcoef(bestMusic, setB)[0][1]
    return corrCoef / numTests


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

    # query get best new music scores are scores for somgs that weren't best new music
    bestNewMusicScores = session.query(Review.score).filter(Review.best_new_music == 1).all()
    bestNewMusicOrNotScores = (
        session.query(Review.best_new_music, func.array_agg(Review.score)).group_by(Review.best_new_music).all()
    )
    bestNewMusicByYear = (
        session.query(Review.pub_year, func.array_agg(Review.score))
        .group_by(Review.pub_year)
        .filter(Review.best_new_music == 1)
        .all()
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

    # Lists of scores by year
    allScoresByYear = session.query(Review.pub_year, func.array_agg(Review.score)).group_by(Review.pub_year).all()

    # query get average score of ratings for each author type
    averageScoresByAuthorType = (
        session.query(Review.author_type, func.array_agg(Review.score))
        .group_by(Review.author_type)
        .filter(Review.author_type != None)
        .all()
    )
    for i in averageScoresByAuthorType:
        print("Author Type: ", i[0])
        print("bestNewMusicScores vs ", i[0], ": ", getCorrelationCoef(i[1], bestNewMusicOrNotScores[1][1], 1000))
        print("NotBestNewMusic vs ", i[0], ": ", getCorrelationCoef(i[1], bestNewMusicOrNotScores[0][1], 1000))
        print("---")
"""
    for i in allScoresByGenre:
        print("Genre: ", i[0])
        print("bestNewMusicScores vs ", i[0], ": ", getCorrelationCoef(i[1], bestNewMusicOrNotScores[1][1], 1000))
        print("NotBestNewMusic vs ", i[0], ": ", getCorrelationCoef(i[1], bestNewMusicOrNotScores[0][1], 1000))
        print("---")



    for i in allScoresByYear:
        scoresForYear = []
        for j in bestNewMusicByYear:
            if j[0] == i[0]:
                scoresForYear = j
        if scoresForYear == []:
            continue
        print("Year: ", i[0])
        print(
            "bestNewMusicScores in ",
            scoresForYear[0],
            " vs ",
            i[0],
            " scores: ",
            getCorrelationCoef(i[1], scoresForYear[1], 1000),
        )
        print("---")
    """

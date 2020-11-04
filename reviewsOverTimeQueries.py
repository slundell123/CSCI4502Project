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
    averageBestNewMusicScores = (
        session.query(func.avg(Review.score), Review.pub_year)
        .filter(Review.best_new_music == 1)
        .group_by(Review.pub_year)
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

    # Graphing score averages
    fig1, (ax1, ax2) = plt.subplots(1, 2)
    fig2, (ax3, ax4) = plt.subplots(1, 2)

    averageScores = sorted(averageScores, key=lambda x: (-x[1], x[0]))
    scores = [i[0] for i in averageScores]
    years = [i[1] for i in averageScores]
    ax1.plot(years, scores)
    ax1.set_xticks(years)
    ax1.set_title("Music Score Average by Year")
    ax1.set_ylabel("Average Score")
    ax1.set_xlabel("Year")

    averageBestNewMusicScores = sorted(averageBestNewMusicScores, key=lambda x: (-x[1], x[0]))
    bestMusicScores = [i[0] for i in averageBestNewMusicScores]
    bestMusicYears = [i[1] for i in averageBestNewMusicScores]
    ax2.plot(bestMusicYears, bestMusicScores)
    ax2.set_xticks(bestMusicYears)
    ax2.set_title("Best New Music Score Average by Year")
    ax2.set_ylabel("Average Score")
    ax2.set_xlabel("Year")

    genreScores = [i[1] for i in averageReviewsScoreByGenre]
    genre = [i[0] for i in averageReviewsScoreByGenre]
    ax3.plot(genre, genreScores, "o")
    ax3.set_xticks(genre)
    ax3.set_title("Average Best New Music Score by Genre")
    ax3.set_ylabel("Average Score")
    ax3.set_xlabel("Genre")
    round_genreScores = [round(num, 3) for num in genreScores]
    for xy in zip(genre, round_genreScores):
        ax3.annotate("(%s, %s)" % xy, xy=xy, textcoords="data", rotation=-5)

    allGenreScores = [i[1] for i in allScoresByGenre]
    genreName = [i[0] for i in allScoresByGenre]
    ax4.boxplot(allGenreScores)
    ax4.set_xticklabels(genreName)
    ax4.set_title("Scores by Genre")
    ax4.set_ylabel("Score")
    ax4.set_xlabel("Genre")

    fig1.set_size_inches(15, 5, forward=True)
    fig2.set_size_inches(15, 5, forward=True)
    plt.setp(ax1.xaxis.get_majorticklabels(), rotation=45)
    plt.setp(ax2.xaxis.get_majorticklabels(), rotation=45)
    plt.setp(ax3.xaxis.get_majorticklabels(), rotation=45)
    plt.setp(ax4.xaxis.get_majorticklabels(), rotation=45)

    plt.show()

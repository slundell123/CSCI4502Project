import logging
import os
import numpy as np
import matplotlib.pylab as plt
import json

from dotenv import load_dotenv
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.sql import func
from models import Review, Genre

# enviornment variables setup
load_dotenv()
PSQL_CONNECTION_STRING = os.getenv("PSQL_CONNECTION_STRING")
# logging setup. See sqlalchemy.log to view generated sql statements
handler = logging.FileHandler("sqlalchemy.log")
handler.setLevel(logging.INFO)
logger = logging.getLogger("sqlalchemy")
logger.addHandler(handler)
logger.setLevel(logging.DEBUG)

# Generates a box plot for best new music scores
def bestNewPlot():
    bestList = []
    for Review in session.query(Review).filter(Review.best_new_music == 1 and Review.pub_year > 2010).limit(100).all():
         bestList.append(Review.score)
    fig1, ax1 = plt.subplots()
    ax1.set_title('Best New Music Scores')
    ax1.boxplot(bestList, showmeans=True)
    plt.show()

# Generates a box plot for not best new music scores
def notBestNewPlot():
    notBestList = []
    for Review in session.query(Review).filter(Review.best_new_music == 0 and Review.pub_year > 2010).limit(100).all():
        notBestList.append(Review.score)
    fig1, ax1 = plt.subplots()
    ax1.set_title('Not Best New Music Scores')
    ax1.boxplot(bestList, showmeans=True)
    plt.show()

def genre():
    # print(session.query(Genre).filter(Genre.genre == "electronic").select(Genre.reviewid).limit(100).all())
    BNMCount = (
        session.query(Genre.genre, func.count(Review.score))
        .filter(Genre.genre != None)
        .join(Review, Genre.reviewid == Review.reviewid)
        .group_by(Genre.genre)
        .all()
    )
    print(BNMCount)

    electronicBNM = (
        session.query(Genre.genre, func.count(Review.best_new_music))
        .filter(Genre.genre == "electronic", Review.best_new_music == 1)
        .join(Review, Genre.reviewid == Review.reviewid)
        .group_by(Genre.genre)
        .all()
    )
    print(electronicBNM)

    jazzBNM = (
        session.query(Genre.genre, func.count(Review.best_new_music))
        .filter(Genre.genre == "jazz", Review.best_new_music == 1)
        .join(Review, Genre.reviewid == Review.reviewid)
        .group_by(Genre.genre)
        .all()
    )
    print(jazzBNM)

    fcBNM = (
        session.query(Genre.genre, func.count(Review.best_new_music))
        .filter(Genre.genre == "folk/country", Review.best_new_music == 1)
        .join(Review, Genre.reviewid == Review.reviewid)
        .group_by(Genre.genre)
        .all()
    )
    print(fcBNM)

    poprbBNM = (
        session.query(Genre.genre, func.count(Review.best_new_music))
        .filter(Genre.genre == "pop/r&b", Review.best_new_music == 1)
        .join(Review, Genre.reviewid == Review.reviewid)
        .group_by(Genre.genre)
        .all()
    )
    print(poprbBNM)

    rapBNM = (
        session.query(Genre.genre, func.count(Review.best_new_music))
        .filter(Genre.genre == "rap", Review.best_new_music == 1)
        .join(Review, Genre.reviewid == Review.reviewid)
        .group_by(Genre.genre)
        .all()
    )
    print(rapBNM)

    rockBNM = (
        session.query(Genre.genre, func.count(Review.best_new_music))
        .filter(Genre.genre == "rock", Review.best_new_music == 1)
        .join(Review, Genre.reviewid == Review.reviewid)
        .group_by(Genre.genre)
        .all()
    )
    print(rockBNM)

    globalBNM = (
        session.query(Genre.genre, func.count(Review.best_new_music))
        .filter(Genre.genre == "global", Review.best_new_music == 1)
        .join(Review, Genre.reviewid == Review.reviewid)
        .group_by(Genre.genre)
        .all()
    )
    print(globalBNM)

    experimentalBNM = (
        session.query(Genre.genre, func.count(Review.best_new_music))
        .filter(Genre.genre == "experimental", Review.best_new_music == 1)
        .join(Review, Genre.reviewid == Review.reviewid)
        .group_by(Genre.genre)
        .all()
    )
    print(experimentalBNM)

    metalBNM = (
        session.query(Genre.genre, func.count(Review.best_new_music))
        .filter(Genre.genre == "metal", Review.best_new_music == 1)
        .join(Review, Genre.reviewid == Review.reviewid)
        .group_by(Genre.genre)
        .all()
    )
    print(metalBNM)

def author():
    averageContributor = (
        session.query(func.avg(Review.score), Review.author_type)
        .filter(Review.author_type != None)
        .group_by(Review.author_type)
        .all()
    )
    averageContributor = sorted(averageContributor, key=lambda x: (x[1], -x[0]))
    scores = [i[0] for i in averageContributor]
    author = [i[1] for i in averageContributor]
    author_pos = [i for i, _ in enumerate(author)]
    plt.bar(author_pos, scores, color='green')
    plt.xlabel("Author Type")
    plt.ylabel("Average Score")
    plt.title("Average Scores by Author Type")
    plt.xticks(author_pos, author, size=6)
    plt.show()



if __name__ == "__main__":
    engine = create_engine(PSQL_CONNECTION_STRING, echo=False)
    Session = sessionmaker(bind=engine)
    session = Session()

    # bestNewPlot()
    # notBestNewPlot()
    # genre()
    author()

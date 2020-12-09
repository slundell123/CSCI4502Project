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

    # query get average score of ratings for each author type
    averageScores = (
        session.query(Review.author_type, func.avg(Review.score))
        .group_by(Review.author_type)
        .filter(Review.author_type != None)
        .all()
    )

    print(averageScores)
    fig1, ax1 = plt.subplots(1, 1)

    averageScores = sorted(averageScores, key=lambda x: (-x[1], x[0]))
    scores = [i[0] for i in averageScores]
    authorType = [i[1] for i in averageScores]
    ax1.plot(scores, authorType, "o")
    ax1.set_xticks(scores)
    ax1.set_title("Music Score Average by Author type")
    ax1.set_xlabel("Average Score")
    ax1.set_ylabel("AuthorType")
    plt.setp(ax1.xaxis.get_majorticklabels(), rotation=45)

    plt.show()

import logging
import os
import numpy as np
import matplotlib.pylab as plt

from dotenv import load_dotenv
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.sql import func

from models import Review

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

    fig, ax = plt.subplots()

    averageScores = sorted(averageScores, key=lambda x: (-x[1], x[0]))
    print(averageScores)
    scores = [i[0] for i in averageScores]
    years = [i[1] for i in averageScores]
    ax.plot(years, scores)
    ax.set_xticks(years)
    plt.show()

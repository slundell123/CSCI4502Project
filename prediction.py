import logging
import os

from dotenv import load_dotenv
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

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

"""
Prediction Plan

What factors am I looking at?
    - best new music
    - review length
        - split between short, medium, and long
            - 18392 reviews
            - avg. length = 4057.166
            - short is  len <= 3000
            - medium is 3000 < len <= 4000
            - long is len > 4000
    - review sentiment
        - use a 3rd party library for this
    - genre ?

How to make decision?
    - instead of trying to predict the numeric score precisely, place into range classes
        - 0-2, 2-4, 4-6, 6-8, 8-10
    - do a gain analysis on each of the categories
    - classify based on decision tree constructed from the gain analysis

"""

if __name__ == "__main__":
    engine = create_engine(PSQL_CONNECTION_STRING, echo=False)
    Session = sessionmaker(bind=engine)
    session = Session()

    # example query to print out top ten results from best new music category
    print(session.query(Review).filter(Review.best_new_music == 1).limit(10).all())

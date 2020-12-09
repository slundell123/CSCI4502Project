import logging
import os
import random

from dotenv import load_dotenv
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.sql.expression import func

from models import Content, Review

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
Summary of Gain Analysis:
    Best New Music Gain: 0.8349388729057268
    Length of Review Gain: 0.3579853202455314
    Sentiment Gain: 0.3767884869740059

Decision Tree:
    1. Split by Best New Music
    2. Split by Review Sentiment
    3. Split by Length of Review
        - 3001+ is long
        - 3000- is short

    After filtering on these conditions, take a majority vote and classify review as such

"""


engine = create_engine(PSQL_CONNECTION_STRING, echo=False)
Session = sessionmaker(bind=engine)
session = Session()


def classify(bnm, sentiment, length):
    short = True if length < 3000 else False
    get_length_q = {True: func.length(Content.content) <= 3000, False: func.length(Content.content) > 3000}
    bad_count = (
        session.query(Content)
        .join(Review, Review.reviewid == Content.reviewid)
        .filter(get_length_q[short], Review.best_new_music == bnm, Content.sentiment == sentiment, Review.score <= 3)
        .count()
    )
    mid_count = (
        session.query(Content)
        .join(Review, Review.reviewid == Content.reviewid)
        .filter(
            get_length_q[short],
            Review.best_new_music == bnm,
            Content.sentiment == sentiment,
            Review.score > 3,
            Review.score <= 7,
        )
        .count()
    )
    good_count = (
        session.query(Content)
        .join(Review, Review.reviewid == Content.reviewid)
        .filter(get_length_q[short], Review.best_new_music == bnm, Content.sentiment == sentiment, Review.score > 7)
        .count()
    )
    klass = max(bad_count, mid_count, good_count)
    if klass == bad_count:
        return "Bad (0-3)"
    elif klass == mid_count:
        return "Mid (4-7)"
    else:
        return "Good (8-10)"


# grab a random review and attempt to classify it
reviews = [x for x in session.query(Content).all()]
test_content = random.choice(reviews)
test_review = session.query(Review).filter(Review.reviewid == test_content.reviewid).first()
print(f"Classifying album {test_review.title} by {test_review.artist}...")
bnm = test_review.best_new_music
sentiment = test_content.sentiment
length = len(test_content.content)
print(f"Classified as: {classify(bnm, sentiment, length)}\nActually: {test_review.score}")

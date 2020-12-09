import logging
import math
import os

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


def info(nums):
    nsum = sum(nums)
    results = []
    for x in nums:
        results.append(-x / nsum * math.log(x / nsum) / math.log(2) if x != 0 else 0)
    return sum(results)


def infoOld(x, y):
    nsum = x + y
    x_expr = -x / nsum * math.log(x / nsum) / math.log(2) if x != 0 else 0
    y_expr = -y / nsum * math.log(y / nsum) / math.log(2) if y != 0 else 0
    return x_expr + y_expr


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
        - 0-3, 4-7, 8-10
    - do a gain analysis on each of the categories
    - classify based on decision tree constructed from the gain analysis

"""

if __name__ == "__main__":
    engine = create_engine(PSQL_CONNECTION_STRING, echo=False)
    Session = sessionmaker(bind=engine)
    session = Session()
    # classifier = get_classifier()

    # get total information
    bad_reviews = session.query(Review).filter(Review.score <= 3)
    bad_reviews_content = (
        session.query(Content).join(Review, Review.reviewid == Content.reviewid).filter(Review.score <= 3)
    )
    mid_reviews = session.query(Review).filter(Review.score > 3, Review.score <= 7)
    mid_reviews_content = (
        session.query(Content)
        .join(Review, Review.reviewid == Content.reviewid)
        .filter(Review.score > 3, Review.score <= 7)
    )
    good_reviews = session.query(Review).filter(Review.score > 7)
    good_reviews_content = (
        session.query(Content).join(Review, Review.reviewid == Content.reviewid).filter(Review.score > 7)
    )
    all_reviews = session.query(Review)
    total_information = info([bad_reviews.count(), mid_reviews.count(), good_reviews.count()])

    # get gain for best new music
    bnm_information = info(
        [
            bad_reviews.filter(Review.best_new_music == 1).count(),
            mid_reviews.filter(Review.best_new_music == 1).count(),
            good_reviews.filter(Review.best_new_music == 1).count(),
        ]
    )
    bnm_information = (
        bad_reviews.count()
        / all_reviews.count()
        * info(
            [
                bad_reviews.filter(Review.best_new_music == 1).count(),
                bad_reviews.filter(Review.best_new_music == 0).count(),
            ]
        )
        + mid_reviews.count()
        / all_reviews.count()
        * info(
            [
                mid_reviews.filter(Review.best_new_music == 1).count(),
                mid_reviews.filter(Review.best_new_music == 0).count(),
            ]
        )
        + good_reviews.count()
        / all_reviews.count()
        * info(
            [
                good_reviews.filter(Review.best_new_music == 1).count(),
                good_reviews.filter(Review.best_new_music == 0).count(),
            ]
        )
    )

    bnm_gain = total_information - bnm_information
    # get gain for review length?
    review_length_information = (
        bad_reviews.count()
        / all_reviews.count()
        * info(
            [
                bad_reviews_content.filter(func.length(Content.content) <= 3000).count(),  # short
                bad_reviews_content.filter(func.length(Content.content) > 3000).count(),  # long
            ]
        )
        + mid_reviews.count()
        / all_reviews.count()
        * info(
            [
                mid_reviews_content.filter(func.length(Content.content) <= 3000).count(),  # short
                mid_reviews_content.filter(func.length(Content.content) > 3000).count(),  # long
            ]
        )
        + good_reviews.count()
        / all_reviews.count()
        * info(
            [
                good_reviews_content.filter(func.length(Content.content) <= 3000).count(),  # short
                good_reviews_content.filter(func.length(Content.content) > 3000).count(),  # long
            ]
        )
    )
    length_gain = total_information - review_length_information

    # get gain for sentiment
    sentiment_information = (
        bad_reviews.count()
        / all_reviews.count()
        * info(
            [
                bad_reviews_content.filter(Content.sentiment == 1).count(),  # positive
                bad_reviews_content.filter(Content.sentiment != 1).count(),  # negative
            ]
        )
        + mid_reviews.count()
        / all_reviews.count()
        * info(
            [
                mid_reviews_content.filter(Content.sentiment == 1).count(),  # positive
                mid_reviews_content.filter(Content.sentiment != 1).count(),  # negative
            ]
        )
        + good_reviews.count()
        / all_reviews.count()
        * info(
            [
                good_reviews_content.filter(Content.sentiment == 1).count(),  # positive
                good_reviews_content.filter(Content.sentiment != 1).count(),  # negative
            ]
        )
    )
    sentiment_gain = total_information - sentiment_information

    print(f"bnm_gain: {bnm_gain}, length_gain: {length_gain}, sentiment_gain: {sentiment_gain}")
    """
    Final #'s
    Best New Music Gain: 0.8349388729057268
    Length of Review Gain: 0.3579853202455314
    Sentiment Gain: 0.3767884869740059

    So, for decision tree, first branch on BNM, then the sentiment, then the length of review

    """

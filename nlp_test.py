import random
import re
import string

import nltk
from nltk import FreqDist, NaiveBayesClassifier, classify
from nltk.corpus import stopwords, twitter_samples
from nltk.stem.wordnet import WordNetLemmatizer
from nltk.tag import pos_tag
from nltk.tokenize import word_tokenize

from models import Content, Review
from queries import get_session

"""
This code has been based on
https://www.digitalocean.com/community/tutorials/how-to-perform-sentiment-analysis-in-python-3-using-the-natural-language-toolkit-nltk

"""

# get db session
session = get_session()


def remove_noise(tokens, stop_words=()):

    cleaned_tokens = []

    for token, tag in pos_tag(tokens):
        token = re.sub("http[s]?://(?:[a-zA-Z]|[0-9]|[$-_@.&+#]|[!*\(\),]|" "(?:%[0-9a-fA-F][0-9a-fA-F]))+", "", token)
        token = re.sub("(@[A-Za-z0-9_]+)", "", token)

        if tag.startswith("NN"):
            pos = "n"
        elif tag.startswith("VB"):
            pos = "v"
        else:
            pos = "a"

        lemmatizer = WordNetLemmatizer()
        token = lemmatizer.lemmatize(token, pos)

        if len(token) > 0 and token not in string.punctuation and token.lower() not in stop_words:
            cleaned_tokens.append(token.lower())
    return cleaned_tokens


def get_all_words(cleaned_tokens_list):
    for tokens in cleaned_tokens_list:
        for token in tokens:
            yield token


def get_for_model(cleaned_tokens_list):
    for tokens in cleaned_tokens_list:
        yield dict([token, True] for token in tokens)


def get_classifier():
    # positive_tweets = twitter_samples.strings("positive_tweets.json")
    # negative_tweets = twitter_samples.strings("negative_tweets.json")
    # text = twitter_samples.strings("tweets.20150430-223406.json")
    # tokens = twitter_samples.tokenized("positive_tweets.json")[0]

    stop_words = stopwords.words("english")

    positive_reviewids = [
        x.reviewid for x in session.query(Review).filter(Review.score >= 5).order_by(Review.score.desc()).all()
    ]
    positive_reviews = []
    for id in random.sample(positive_reviewids, 50):
        positive_reviews.append(session.query(Content).filter(Content.reviewid == id).first().content)

    negative_reviewids = [
        x.reviewid for x in session.query(Review).filter(Review.score < 5).order_by(Review.score).all()
    ]
    negative_reviews = []
    for id in random.sample(negative_reviewids, 50):
        negative_reviews.append(session.query(Content).filter(Content.reviewid == id).first().content)

    # positive_tokens = twitter_samples.tokenized("positive_tweets.json")
    # negative_tokens = twitter_samples.tokenized("negative_tweets.json")
    positive_tokens = [nltk.word_tokenize(x) for x in positive_reviews]
    negative_tokens = [nltk.word_tokenize(x) for x in negative_reviews]

    positive_cleaned_tokens_list = []
    negative_cleaned_tokens_list = []

    for tokens in positive_tokens:
        positive_cleaned_tokens_list.append(remove_noise(tokens, stop_words))

    for tokens in negative_tokens:
        negative_cleaned_tokens_list.append(remove_noise(tokens, stop_words))

    # all_pos_words = get_all_words(positive_cleaned_tokens_list)

    # freq_dist_pos = FreqDist(all_pos_words)
    # print(freq_dist_pos.most_common(10))

    positive_tokens_for_model = get_for_model(positive_cleaned_tokens_list)
    negative_tokens_for_model = get_for_model(negative_cleaned_tokens_list)

    positive_dataset = [(word_dict, "Positive") for word_dict in positive_tokens_for_model]

    negative_dataset = [(word_dict, "Negative") for word_dict in negative_tokens_for_model]

    dataset = positive_dataset + negative_dataset

    random.shuffle(dataset)

    # train_data = dataset[:7000]
    # test_data = dataset[7000:]
    train_data = dataset

    return NaiveBayesClassifier.train(train_data)


def sentiment(classifier, text):

    # print(classifier.show_most_informative_features(10))

    # custom_tweet = "I ordered just once from TerribleCo, they screwed up, never used the app again."

    custom_tokens = remove_noise(word_tokenize(text))

    return classifier.classify(dict([token, True] for token in custom_tokens))


if __name__ == "__main__":
    sample_size = 10
    classifier = get_classifier()

    positive_reviewids = [x.reviewid for x in session.query(Review).filter(Review.score >= 5).all()]
    correct = 0
    accuracy_list = []
    for ii in range(100):
        test_ids = random.sample(positive_reviewids, sample_size)
        positive_reviews = []
        for id in test_ids:
            positive_reviews.append(session.query(Content).filter(Content.reviewid == id).first().content)
        for review in positive_reviews:
            if len(review) > 0:
                if sentiment(classifier, review) == "Positive":
                    correct += 1
        print(f"accuracy: {correct}/{sample_size}")
        accuracy_list.append(correct)
        correct = 0

    print(f"###### AVG ######\n{sum(accuracy_list)/len(accuracy_list)}/{sample_size}")

# CSCI4502Project

## About
In this project we analysed data from pitchfork, a music review site, between 1999 to 2017. We wanted to see if there was a bias in the music review system that the site used as well as if there was a way to predict a song's review score based off of the reviews text. We focused on the later part of the data's date range after our initial analysis of the data indicated that there might be a bias in later years.  We used correlation values to check for bias in the scores and found that there is no real correlation between the factors we checked and the scored. This lead up to conclude that the process by which pitchfork scores music has no real bias from review publication year, genre, or review author type. To predict the score from a review we used a sentiment analysis and it was able to classify reviews based on their text. This means that there are similar characteristic between what a review author writes about a song and the review score that the song receives. 

## Key  Findings
Based on our results from the code, we found there to be no bias in the review scores from the factors of song genre, review publication year, or review author type. We found this result to be interesting because we had initially assumed that there would be some kind of bias in the reviews given that people's music taste and opinions are very subjective. We think that there must be some kind of interval review score standardization or a rubric for scoring for there to be no correlation between the factors we looked at. 

We also found that it was possible to predict a song's score category with an average accuracy of ~60%. This is a very interesting result and proves that using sentiment analysis on the text of the review along with a decision tree can determine if a review is good, neutral, or bad. There are some things we could do to improve the accuracy, like changing the range in the bins for each category or doing more experimentation with more factors added to our decision tree. 

## Setup
Ensure python3 is installed
```bash
python --version
```
If using Mac/Linux, sometimes `python` refers to python 2 and `python3` is required. Use whatever gives you the correct version.

First, create and activate a python virtual environment. NOTE: after inital creation, just activate the existing environment
```bash
python -m venv <venv_name>
```
For windows,
```bash
.\<venv_name>\Scripts\activate
```
For Mac/Linux users, 
```bash
source <venv_name>/bin/activate
```
Second, install all requirements using the following command
```bash
pip install -r requirements.txt
```
To run example query I've set up
```bash
python queries.py
```

## Explanation of File Structure
`models.py`contains the python classes used to represent our database tables\
`queries.py` establishes the database connection and can be used to execute queries\
`requirements.txt` contains a list of the python packages neccessary to interact with our database\
`.vscode/` contains editor settings. While you're not required to use vscode, these settings will keep our formatting consistent\
`.env` contains environment variables neccessary to connect to the database. NOTE: this is .gitignore'd, and you'll have to add this file yourself. This is becuase we do not want our database information stored on github. PLEASE PLEASE be careful with this and do not commit my connection info to github :)

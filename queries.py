import logging
import os

from dotenv import load_dotenv
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

# enviornment variables setup
load_dotenv()
PSQL_CONNECTION_STRING = os.getenv("PSQL_CONNECTION_STRING")
# logging setup. See sqlalchemy.log to view generated sql statements
handler = logging.FileHandler("sqlalchemy.log")
handler.setLevel(logging.INFO)
logger = logging.getLogger("sqlalchemy")
logger.addHandler(handler)
logger.setLevel(logging.DEBUG)


def get_session():
    engine = create_engine(PSQL_CONNECTION_STRING, echo=False)
    Session = sessionmaker(bind=engine)
    return Session()

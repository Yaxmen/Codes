import os
import logging
from dotenv import load_dotenv
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base

load_dotenv()

DATABASE_TYPE = os.getenv("DATABASE_TYPE")
ENGINE = os.getenv("ENGINE")
DATABASE_USER = os.getenv("DATABASE_USER")
DATABASE_PASS = os.getenv("DATABASE_PASS")
DATABASE_HOST = os.getenv("DATABASE_HOST")
DATABASE_PORT = os.getenv("DATABASE_PORT")
DATABASE_NAME = os.getenv("DATABASE_NAME")

Base = declarative_base()
logger = logging.getLogger(__name__)


class DBConnectionHandler:

    def __init__(self) -> None:
        logger.info('Connecting to the database.')
        self.__connection_string = (
            f"{DATABASE_TYPE}+{ENGINE}://"
            f"{DATABASE_USER}:{DATABASE_PASS}@{DATABASE_HOST}:{DATABASE_PORT}/{DATABASE_NAME}"
        )
        self.__engine = self.__create_database_engine()
        self.session = None

    def __create_database_engine(self):
        logger.info('Configuring engine for communicating with database.')
        engine = create_engine(self.__connection_string)
        return engine

    def get_engine(self):
        return self.__engine

    def __enter__(self):
        logger.info('Starting a new session to the database.')
        session_make = sessionmaker(bind=self.__engine)
        self.session = session_make()
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        logger.info('FEnding new session to the database.')
        self.session.close()

    def check_db_structure(self):
        # Mapeando os modelos.
        logger.info('Table Structure according to models.')
        for tabel in Base.metadata.sorted_tables: print('Created Table: %s' % tabel)
        Base.metadata.bind = self.__engine
        Base.metadata.create_all(self.__engine)
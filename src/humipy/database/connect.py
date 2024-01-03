from dotenv import load_dotenv
from os import getenv
import sqlalchemy
from sqlalchemy import create_engine


def get_engine(dev: bool = False) -> sqlalchemy.engine.base.Engine:
    """
    This function initializes an engine. This engine functions as a connection 
    factory and connection pool.

    Returns:
        sqlalchemy.engine.base.Engine: a SQLAlchemy engine object.
    """
    if dev:
        return create_engine("sqlite+pysqlite:///:memory:")
    load_dotenv()

    db = getenv("DB_NAME")
    host = getenv("DB_HOST")
    port = getenv("DB_PORT")
    username = getenv("DB_USERNAME")
    password = getenv("DB_PASSWORD")

    return create_engine(
        f"postgresql+psycopg2://{username}:{password}@{host}:{port}/{db}"
    )
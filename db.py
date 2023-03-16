from sqlalchemy import create_engine
from sqlalchemy.orm import declarative_base
from sqlalchemy.orm import scoped_session, sessionmaker

from config import get_config

CONFIG = get_config()
ENGINE = create_engine(CONFIG.sqlalchemy_url)
DB_SESSION = scoped_session(sessionmaker(bind=ENGINE))

Base = declarative_base()
Base.query = DB_SESSION.query_property()

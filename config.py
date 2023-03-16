import os
from typing import NamedTuple

from dotenv import load_dotenv

if os.path.exists(os.path.join(os.path.dirname(__file__), '.env')):
    load_dotenv(os.path.join(os.path.dirname(__file__), '.env'))


class Config(NamedTuple):
    sqlalchemy_url: str


def get_config() -> Config:
    basedir = os.path.abspath(os.path.dirname(__file__))
    return Config(
        sqlalchemy_url='sqlite:///' + os.path.join(
            basedir,
            os.environ.get('DB_FILENAME', 'test_task_track.db'),
        ),
    )

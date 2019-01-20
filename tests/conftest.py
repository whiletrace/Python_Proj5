import pytest

from peewee import *
from app import create_app
TEST_DATABASE = SqliteDatabase(':memory:')
from models import User, Entry

MODELS = [User, Entry]


@pytest.fixture()
def test_database():
    TEST_DATABASE.bind(MODELS)
    TEST_DATABASE.connect()
    TEST_DATABASE.create_tables(MODELS, safe=True)

    yield TEST_DATABASE
    TEST_DATABASE.drop_tables(MODELS)
    TEST_DATABASE.close()


@pytest.fixture()
def app():
    app = create_app()
    app.testing = True
    test_client = app.test_client()
    ctx = app.app_context()
    ctx.push()

    yield test_client

    ctx.pop()

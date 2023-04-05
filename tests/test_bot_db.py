import pytest
from vk_bot.bot_db import VkDB


@pytest.fixture(scope='module')
def db():
    db = VkDB()
    db.create_db()
    yield db
    db.conn.close()


def test_add_client(db):
    result = db.add_client(1, 2, 'Alice')
    assert result == 'Пользователь добавлен в базу!'


def test_find_client_existing(db):
    db.add_client(1, 2, 'Alice')
    result = db.find_client(1, 2)
    assert result == (1, 2)


def test_find_client_nonexistent(db):
    db.add_client(1, 2, 'Alice')
    result = db.find_client(2, 1)
    assert result is None

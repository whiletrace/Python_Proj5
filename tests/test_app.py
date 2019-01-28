from datetime import datetime, timedelta

import models


def test_create_users(test_database):
    models.User.create_user(

        username='eddimall',
        password='password'
            )
    assert models.User.select().count() == 1
    assert models.User.get(models.User.username == 'eddimall')


def test_create_entry(test_database):
    models.User.create_user(
        username='eddimall',
        password='password')
    user = models.User.select().get()
    models.Entry.create_entry(
        user=user,
        title='shamrock',
        date=datetime.now(),
        time_spent=timedelta(seconds=234),
        knowledge_gained="oh you know that was kinda fun",
        resources=' so many books I would love to list'
    )
    assert models.Entry.select().count() == 1
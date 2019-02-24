import datetime

import models


def tag_utility(tag_data, journal_entry):
    tags = []
    for item in tag_data:
        tag = models.Tag.get_or_create_tags(
            name=item
        )
        tags.append(tag)
    models.JournalTags.create_relations(journal_entry, tags)


def entry_1():
    tag_data = ['python', 'web development', 'flask', 'parties']
    models.User.create_user(
        username='trace',
        password='password'
    )
    models.Entry.create_entry(
        user=1,
        title='a wonderful',
        date=datetime.datetime.now(),
        time_spent=datetime.timedelta(minutes=234),
        knowledge='I know things that only someone of my standing could know',
        resources='eggs and coffee\n lsd\n yayo'.splitlines()

    )
    journal_entry = models.Entry.get(title='a wonderful')
    tag_utility(tag_data, journal_entry)


def entry_2():
    tag_data = ['python', 'flask', 'database', 'web development']

    models.User.create_user(
        username='uncle',
        password='password'
    ),
    models.Entry.create_entry(
        user=2,
        title='life and bounty',
        date=datetime.datetime.now(),
        time_spent=datetime.timedelta(minutes=234),
        knowledge='yeah that first guy doesnt know squat',
        resources='eggs and coffee\n lsd\n yayo'.splitlines()

    )
    journal_entry = models.Entry.get(title='life and bounty')
    tag_utility(tag_data, journal_entry)
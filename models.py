from flask_bcrypt import generate_password_hash
from flask_login import UserMixin
from peewee import *

DATABASE = SqliteDatabase('journal')


class BaseModel(Model):
    class Meta:
        database = DATABASE


class User(UserMixin, BaseModel):
    username = CharField(max_length=50, unique=True)
    password = CharField(max_length=50, unique=True)

    @classmethod
    def create_user(cls, username, password):

        try:
            with DATABASE.transaction():
                cls.create(
                    username=username,
                    password=generate_password_hash(password)
                )
        except IntegrityError:
            raise ValueError('username and Password exists')


class Entry(BaseModel):
    user = ForeignKeyField(

        model=User,
        backref='entries'

    )

    title = CharField(max_length=75)
    date = DateField()
    time_spent = TimeField()
    knowledge_gained = TextField()
    resources = TextField()

    @classmethod
    def create_entry(cls, database, user, title, date, time_spent,
                     knowledge_gained, resources):
        """

        @type date: object
        """
        try:
            with database.transaction():
                cls.create(
                    user=user,
                    title=title,
                    date=date,
                    time_spent=time_spent,
                    knowledge_gained=knowledge_gained,
                    resources=resources,

                )
        except InternalError:
            raise DatabaseError('could not creat a entry: database failure')


class TAG(BaseModel):
    tag = CharField()


class JournalEntryTag(BaseModel):
    journal_entry = ForeignKeyField(Entry)
    tag = ForeignKeyField(TAG)


def initialize():
    DATABASE.connect()
    DATABASE.create_tables([User, Entry, TAG, JournalEntryTag], safe=True)
    DATABASE.close()

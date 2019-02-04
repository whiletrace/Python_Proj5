from flask_bcrypt import generate_password_hash
from flask_login import UserMixin
from peewee import *
from peewee import ForeignKeyField


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
            # import pdb;pdb.set_trace()
            with cls._meta.database.transaction():
                cls.create(
                    username=username,
                    password=generate_password_hash(password)
                )
        except IntegrityError:
            raise ValueError('username and Password exists')

    def get_entry(self):
        Entry.select().where(User == self)

class Tag(BaseModel):
    name = CharField(unique=True, null=True)

    @classmethod
    def get_or_create_tags(cls, name):
        try:
            with cls._meta.database.transaction():
                return cls.create(
                    name=name
                )
        except IntegrityError:
            tag = cls.get(name=name)
            return tag

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
    def create_entry(
            cls, user, title, date, time_spent,
            knowledge_gained, resources,
    ):

        try:
            with cls._meta.database.transaction():
                cls.create(
                    user=user,
                    title=title,
                    date=date,
                    time_spent=time_spent,
                    knowledge_gained=knowledge_gained,
                    resources=resources)
        except InternalError:
            raise DatabaseError('could not creat a entry: database failure')


class JournalTags(BaseModel):
    entry = ForeignKeyField(
        Entry
    )
    tag = ForeignKeyField(
        Tag
    )

    @classmethod
    def create_relations(cls, entry, tags):
        entries = []
        for tag in tags:
            entries.append(JournalTags(entry=entry, tag=tag))
        with cls._meta.database.atomic():
            JournalTags.bulk_create(entries)

def initialize():
    DATABASE.connect()
    DATABASE.create_tables([User, Tag, Entry, JournalTags], safe=True)
    DATABASE.close()

from flask_bcrypt import generate_password_hash
from flask_login import UserMixin
from peewee import *
from peewee import ForeignKeyField
from playhouse.fields import PickleField

DATABASE = SqliteDatabase('journal')


class BaseModel(Model):
    class Meta:
        database = DATABASE


class User(UserMixin, BaseModel):
    """
    Model class for Use
    attributes:username :str
    attributes:password: stt

    class methods: create_user

    """
    username = CharField(max_length=50, unique=True)
    password = CharField(max_length=50, unique=True)

    @classmethod
    def create_user(cls, username, password):
        """
        lassmethod for the instantiation of model.User obj


        @param username:
        @type username: str
        @param password:
        @type password: str
        """
        try:
            with cls._meta.database.transaction():
                cls.create(
                    username=username,
                    password=generate_password_hash(password)
                )
        except IntegrityError:
            raise ValueError('username and Password exists')


class Tag(BaseModel):
    """
    class handles definition and instantion of models.Tag obj
    classmethods: get_or_create_tags
    """
    name = CharField(unique=True)

    @classmethod
    def get_or_create_tags(cls, name):
        """
        classmethod handles logic for instantion of Tag obj

        if tag does not exist will instantiate
        new Tag if Tag exists will get
        corresponding tag and return TAG

        @param name: Tag attr
        @type name: str()
        @return: Tag
        @rtype: models.Tag obj
        """
        try:
            with cls._meta.database.transaction():
                return cls.create(
                    name=name
                )
        except IntegrityError:
            tag = cls.get(name=name)
            return tag


class Entry(BaseModel):
    """
    Class for definition and instantiation of Entry Obj

    classmethods create_entry

    """
    user = ForeignKeyField(

        model=User,
        backref='entries'
    )

    title = CharField(max_length=75)
    date = DateField(formats='%d/%m/%Y')
    time_spent = TimeField()
    knowledge = TextField()
    resources = PickleField()

    @classmethod
    def create_entry(
            cls, user, title, date, time_spent,
            knowledge, resources,
    ):
        """
        classmethod controls instantiation of models.Entry objects
        @param user: foreign key
        @type user: models.User
        @param title: Entry attr
        @type title: str
        @param date:Entry attr
        @type date: datetime.date
        @param time_spent: Entry attr
        @type time_spent: datetime.timedelta
        @param knowledge: Entry attr
        @type knowledge: str
        @param resources:Entry attr
        @type resources: List[str]
        """
        try:
            with cls._meta.database.transaction():
                cls.create(
                    user=user,
                    title=title,
                    date=date,
                    time_spent=time_spent,
                    knowledge=knowledge,
                    resources=resources
                )

        except InternalError:
            raise DatabaseError('could not create a entry: database failure')




class JournalTags(BaseModel):
    """
    class for definition and instantion of Journal_Tags

    JournalTags is a through model that handles many to many relationship
    between entry and tags


    """
    entry = ForeignKeyField(
        Entry
    )
    tag = ForeignKeyField(
        Tag
    )

    @classmethod
    def create_relations(cls, entry, tags):
        """

        handles logic to create many to many relationship between tags and entries
        @rtype: None
        @param entry: int()
        @type entry: models.Entry
        @param tags:int()
        @type tags: List[models.Tag]
        """
        entries = []
        for tag in tags:
            entries.append(JournalTags(entry=entry, tag=tag))
        with cls._meta.database.atomic():
            JournalTags.bulk_create(entries)

    @classmethod
    def break_relations(cls, tag, entry):
        """
        classmethod breaks relationship link between tags and entry in edit entries

        @param tag: tag_id:
        @type tag: int()
        @param entry: entry
        @type entry: int()
        """
        q = cls.delete().where((cls.tag == tag) & (cls.entry == entry))
        q.execute()


# database initialization
def initialize():
    DATABASE.connect()
    DATABASE.create_tables([User, Entry, Tag, JournalTags], safe=True),
    DATABASE.close()
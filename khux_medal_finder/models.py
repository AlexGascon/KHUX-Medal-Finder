import os
from peewee import *

db = PostgresqlDatabase(database=os.environ['DB_DATABASE'],
                        user=os.environ['DB_USERNAME'],
                        password=os.environ['DB_PASSWORD'],
                        host=os.environ['DB_HOST'],
                        port=os.environ['DB_PORT'],
                        autorollback=True)


class BaseModel(Model):
    """Abstract model that we'll use to make other models inherit DB settings"""
    class Meta:
        database = db


class Medal(BaseModel):
    cost = IntegerField()
    defence = IntegerField(null=True)
    direction = CharField()
    element = CharField()
    hits = IntegerField()
    image_link = TextField(null=True)
    medal_id = IntegerField(primary_key=True, index=True)
    multiplier_min = FloatField()
    multiplier_max = FloatField()
    name = TextField(index=True)
    notes = TextField(null=True)
    pullable = CharField(max_length=3, null=True)
    rarity = IntegerField(null=True)
    region = CharField(max_length=5, null=True)
    strength = IntegerField(null=True)
    targets = CharField(max_length=10)
    tier = IntegerField()
    type = CharField(max_length=10)
    voice_link = TextField(null=True)


class Comment(BaseModel):
    """Comment posted by a user on Reddit"""
    author = CharField()
    comment_id = CharField()
    text = TextField()
    timestamp = TimestampField()
    url = CharField(max_length=400)


class Reply(Comment):
    """Reply made by the bot to one Reddit comment. Though it could be modelled
    using Comment, this allows us to extend its functionality"""
    author = CharField(default=lambda: 'khux_medal_finder')
    original_comment = ForeignKeyField(Comment)
    success = BooleanField()
